"""
This module handles calculating historical densities from
time series of prices and converting them to implied volatility smiles.
"""

import ccxt
import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union, Any
from voly.utils.logger import logger, catch_exception
from voly.exceptions import VolyError
from voly.core.rnd import get_all_moments
from voly.formulas import iv, get_domain
from voly.models import SVIModel
from voly.core.fit import fit_model
from arch import arch_model


@catch_exception
def get_historical_data(currency: str,
                        lookback_days: str,
                        granularity: str,
                        exchange_name: str) -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a cryptocurrency.

    Parameters:
    ----------
    currency : str
        The cryptocurrency to fetch data for (e.g., 'BTC', 'ETH').
    lookback_days : str
        The lookback period in days, formatted as '90d', '30d', etc.
    granularity : str
        The time interval for data points (e.g., '15m', '1h', '1d').
    exchange_name : str
        The exchange to fetch data from (default: 'binance').

    Returns:
    -------
    pd.DataFrame: Historical price data with OHLCV columns.
    """
    try:
        # Get the exchange class from ccxt
        exchange_class = getattr(ccxt, exchange_name.lower())
        exchange = exchange_class({'enableRateLimit': True})
    except (AttributeError, TypeError):
        raise VolyError(f"Exchange '{exchange_name}' not found in ccxt. Please check the exchange name.")

    # Form the trading pair symbol
    symbol = currency + '/USDT'

    # Convert lookback_days to timestamp
    if lookback_days.endswith('d'):
        days_ago = int(lookback_days[:-1])
        date_start = (dt.datetime.now() - dt.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        raise VolyError("lookback_days should be in format '90d', '30d', etc.")

    from_ts = exchange.parse8601(date_start)
    ohlcv_list = []
    ohlcv = exchange.fetch_ohlcv(symbol, granularity, since=from_ts, limit=1000)
    ohlcv_list.append(ohlcv)

    # Fetch all available data within the lookback period
    while len(ohlcv) == 1000:
        from_ts = ohlcv[-1][0]
        new_ohlcv = exchange.fetch_ohlcv(symbol, granularity, since=from_ts, limit=1000)
        if len(new_ohlcv) <= 1:
            break
        ohlcv.extend(new_ohlcv[1:])  # Skip first element to avoid duplication
        if len(new_ohlcv) < 1000:
            break

    # Convert to DataFrame
    df_hist = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df_hist['date'] = pd.to_datetime(df_hist['date'], unit='ms')
    df_hist.set_index('date', inplace=True)
    df_hist = df_hist.sort_index(ascending=True)

    logger.info(f"Data fetched successfully: {len(df_hist)} rows from {df_hist.index[0]} to {df_hist.index[-1]}")

    return df_hist


@catch_exception
def parse_window_length(window_length: str, df_hist: pd.DataFrame) -> int:
    """
    Parse window length from string format (e.g., '7d', '30d') to number of data points.

    Parameters:
    -----------
    window_length : str
        Window length in days, formatted as '7d', '30d', etc.
    df_hist : pd.DataFrame
        Historical data DataFrame with datetime index.

    Returns:
    --------
    int
        Number of data points corresponding to the window length.
    """
    if not isinstance(window_length, str) or not window_length.endswith('d'):
        raise VolyError("window_length should be in format '7d', '30d', etc.")

    # Extract number of days
    days = int(window_length[:-1])

    # Calculate time delta between consecutive data points
    if len(df_hist) > 1:
        avg_delta = (df_hist.index[-1] - df_hist.index[0]) / (len(df_hist) - 1)
        # Convert to days and get points per day
        days_per_point = avg_delta.total_seconds() / (24 * 60 * 60)
        # Calculate number of points for the window
        n_points = int(days / days_per_point)
        return max(n_points, 10)  # Ensure at least 10 points
    else:
        raise VolyError("Not enough data points in df_hist to calculate granularity.")


@catch_exception
def fit_volatility_model(log_returns: np.ndarray,
                         df_hist: pd.DataFrame,
                         model_type: str = 'garch',
                         distribution: str = 'normal',
                         window_length: str = '30d',
                         n_fits: int = 400) -> Dict[str, Any]:
    """
    Fit a volatility model (GARCH or EGARCH) to log returns.

    Parameters:
    -----------
    log_returns : np.ndarray
        Array of log returns
    df_hist : pd.DataFrame
        DataFrame with historical price data
    model_type : str
        Type of volatility model ('garch' or 'egarch')
    distribution : str
        Distribution type ('normal', 'studentst', or 'skewstudent')
    window_length : str
        Length of each window as a string (e.g., '30d')
    n_fits : int
        Number of sliding windows

    Returns:
    --------
    Dict[str, Any]
        Dictionary with model parameters and processes
    """
    # Parse window length
    window_points = parse_window_length(window_length, df_hist)

    if len(log_returns) < window_points + n_fits:
        raise VolyError(f"Not enough data points. Need at least {window_points + n_fits}, got {len(log_returns)}")

    # Adjust window sizes if necessary to avoid over-fitting
    n_fits = min(n_fits, max(100, len(log_returns) // 3))
    window_points = min(window_points, max(20, len(log_returns) // 3))

    start = window_points + n_fits
    end = n_fits

    # Different number of parameters based on model type and distribution
    param_names = get_param_names(model_type, distribution)
    n_params = len(param_names)

    parameters = np.zeros((n_fits, n_params))
    z_process = []

    logger.info(
        f"Fitting {model_type.upper()} model with {distribution} distribution using {n_fits} windows of {window_length}...")

    for i in range(n_fits):
        if i % (n_fits // 10) == 0:
            logger.info(f"Fitting progress: {i}/{n_fits}")

        # Skip if we don't have enough data
        if end - i - 1 < 0 or start - i - 1 > len(log_returns):
            continue

        window = log_returns[end - i - 1:start - i - 1]

        # Skip windows that are too small or have invalid data
        if len(window) < 10 or np.isnan(window).any() or np.isinf(window).any():
            continue

        # Mean-center the data to improve numerical stability
        data = window - np.mean(window)

        try:
            # Configure model based on type and distribution
            if model_type.lower() == 'garch':
                model = arch_model(data, vol='GARCH', p=1, q=1, dist=distribution.lower())
            else:  # egarch
                model = arch_model(data, vol='EGARCH', p=1, o=1, q=1, dist=distribution.lower())

            fit_result = model.fit(disp='off', options={'maxiter': 1000})

            # Extract parameters based on model type and distribution
            params_dict = fit_result.params.to_dict()

            # Extract parameter values in correct order
            param_values = [params_dict.get(param, 0) for param in param_names]
            parameters[i, :] = param_values

            # Get last innovation (standardized residual)
            residuals = fit_result.resid
            conditional_vol = fit_result.conditional_volatility

            if len(residuals) > 0 and len(conditional_vol) > 0:
                z_t = residuals[-1] / conditional_vol[-1]
                if not np.isnan(z_t) and not np.isinf(z_t):
                    z_process.append(z_t)

        except Exception as e:
            logger.warning(f"Model fit failed for window {i}: {str(e)}")

    # Clean up any failed fits
    if len(z_process) < n_fits / 2:
        raise VolyError(f"Too many model fits failed ({len(z_process)}/{n_fits}). Check your data.")

    # Filter out rows with zeros (failed fits)
    valid_rows = ~np.all(parameters == 0, axis=1)
    parameters = parameters[valid_rows]

    # Calculate average parameters and standard deviations
    avg_params = np.mean(parameters, axis=0)
    std_params = np.std(parameters, axis=0)

    return {
        'model_type': model_type,
        'distribution': distribution,
        'parameters': parameters,
        'avg_params': avg_params,
        'std_params': std_params,
        'z_process': np.array(z_process),
        'param_names': param_names
    }


def get_param_names(model_type: str, distribution: str) -> List[str]:
    """
    Get parameter names based on model type and distribution.

    Parameters:
    -----------
    model_type : str
        Type of volatility model ('garch' or 'egarch')
    distribution : str
        Distribution type ('normal', 'studentst', or 'skewstudent')

    Returns:
    --------
    List[str]
        List of parameter names
    """
    if model_type.lower() == 'garch':
        if distribution.lower() == 'normal':
            return ['mu', 'omega', 'alpha[1]', 'beta[1]']
        elif distribution.lower() == 'studentst':
            return ['mu', 'omega', 'alpha[1]', 'beta[1]', 'nu']
        else:  # skewstudent
            return ['mu', 'omega', 'alpha[1]', 'beta[1]', 'nu', 'lambda']
    else:  # egarch
        if distribution.lower() == 'normal':
            return ['mu', 'omega', 'alpha[1]', 'gamma[1]', 'beta[1]']
        elif distribution.lower() == 'studentst':
            return ['mu', 'omega', 'alpha[1]', 'gamma[1]', 'beta[1]', 'nu']
        else:  # skewstudent
            return ['mu', 'omega', 'alpha[1]', 'gamma[1]', 'beta[1]', 'nu', 'lambda']


@catch_exception
def simulate_volatility_paths(vol_model: Dict[str, Any],
                              horizon: int,
                              simulations: int = 5000) -> Tuple[np.ndarray, float]:
    """
    Simulate future paths using a fitted volatility model.

    Parameters:
    -----------
    vol_model : Dict[str, Any]
        Dict with volatility model parameters
    horizon : int
        Number of steps to simulate
    simulations : int
        Number of paths to simulate

    Returns:
    --------
    Tuple[np.ndarray, float]
        Simulated returns and drift
    """
    parameters = vol_model['parameters']
    z_process = vol_model['z_process']
    model_type = vol_model['model_type']
    distribution = vol_model['distribution']
    param_names = vol_model['param_names']

    # Use mean parameters as starting point
    pars = vol_model['avg_params'].copy()
    bounds = vol_model['std_params'].copy()

    # Create dictionary for easier parameter access
    param_dict = {name: value for name, value in zip(param_names, pars)}

    # Log parameters in a structured way
    param_str = ", ".join([f"{name}={param_dict.get(name, 0):.6f}" for name in param_names])
    logger.info(f"{model_type.upper()} parameters: {param_str}")

    # Create sampling function based on distribution
    if distribution.lower() == 'normal':
        # Use standard normal for normal distribution
        def sample_innovation(size=1):
            return np.random.normal(0, 1, size=size)
    else:
        # Use KDE for non-normal distributions to capture empirical distribution
        kde = stats.gaussian_kde(z_process, bw_method='silverman')  # original code didnt have bw_method
        z_range = np.linspace(min(z_process), max(z_process), 1000)
        z_prob = kde(z_range)
        z_prob = z_prob / np.sum(z_prob)

        def sample_innovation(size=1):
            return np.random.choice(z_range, size=size, p=z_prob)

    # Simulate paths
    simulated_returns = np.zeros(simulations)
    mu = param_dict.get('mu', 0)

    for i in range(simulations):
        if (i + 1) % (simulations // 10) == 0:
            logger.info(f"Simulation progress: {i + 1}/{simulations}")

        # Optionally vary parameters between simulations
        if (i + 1) % (simulations // 20) == 0:
            # Create parameter variations based on their estimated distribution
            sim_params = {}
            for j, (name, par, bound) in enumerate(zip(param_names, pars, bounds)):
                var = bound ** 2 / max(len(parameters), 1)
                # Generate new parameter from normal distribution around the mean
                new_par = np.random.normal(par, np.sqrt(var))

                # Apply constraints to ensure valid parameters
                if name == 'omega':
                    new_par = max(new_par, 1e-6)  # Must be positive
                elif name in ['alpha[1]', 'beta[1]']:
                    new_par = max(min(new_par, 0.999), 0.001)  # Between 0 and 1
                elif name == 'nu':
                    new_par = max(new_par, 2.1)  # Degrees of freedom > 2

                sim_params[name] = new_par
        else:
            sim_params = param_dict.copy()

        # Initialize volatility based on model type
        if model_type.lower() == 'garch':
            omega = sim_params.get('omega', 0)
            alpha = sim_params.get('alpha[1]', 0)
            beta = sim_params.get('beta[1]', 0)

            # Initialize GARCH volatility (unconditional variance)
            sigma2 = omega / (1 - alpha - beta) if alpha + beta < 1 else omega / 0.99
        else:  # egarch
            omega = sim_params.get('omega', 0)
            beta = sim_params.get('beta[1]', 0)

            # Initialize EGARCH volatility
            log_sigma2 = omega / (1 - beta) if beta < 1 else omega / 0.99
            sigma2 = np.exp(log_sigma2)

        returns_sum = 0

        # Simulate path step by step
        for _ in range(horizon):
            # Sample a random innovation
            z = sample_innovation()

            # Update returns and volatility based on model type
            if model_type.lower() == 'garch':
                # Calculate return
                e = z * np.sqrt(sigma2)
                returns_sum += e + mu

                # Update GARCH volatility
                sigma2 = sim_params.get('omega', 0) + sim_params.get('alpha[1]', 0) * e ** 2 + sim_params.get('beta[1]',
                                                                                                              0) * sigma2
            else:  # egarch
                # Calculate return
                e = z * np.sqrt(sigma2)
                returns_sum += e + mu

                # Update EGARCH volatility
                abs_z = abs(z)
                gamma = sim_params.get('gamma[1]', 0)
                alpha = sim_params.get('alpha[1]', 0)
                beta = sim_params.get('beta[1]', 0)
                omega = sim_params.get('omega', 0)

                # EGARCH update equation
                log_sigma2 = omega + beta * log_sigma2 + alpha * (abs_z - np.sqrt(2 / np.pi)) + gamma * z
                sigma2 = np.exp(log_sigma2)

        simulated_returns[i] = returns_sum

    return simulated_returns, mu * horizon


def get_hd_surface(model_results: pd.DataFrame,
                   df_hist: pd.DataFrame,
                   domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness',
                   method: str = 'garch',
                   distribution: str = 'normal',
                   window_length: str = '30d',
                   n_fits: int = 400,
                   simulations: int = 5000,
                   bandwidth: str = 'silverman') -> Dict[str, Any]:
    """
    Generate historical density surface from historical price data.

    Parameters:
    -----------
    model_results : pd.DataFrame
        DataFrame with model parameters and maturities
    df_hist : pd.DataFrame
        DataFrame with historical price data
    domain_params : Tuple[float, float, int]
        Tuple of (min, max, num_points) for x-domain
    return_domain : str
        Domain for x-axis values ('log_moneyness', 'moneyness', 'returns', 'strikes')
    method : str
        Method to use for HD estimation:
        - 'garch': GARCH(1,1) model
        - 'egarch': EGARCH(1,1,1) model with asymmetry
        - 'basic': Simple histogram/KDE of historical returns
    distribution : str
        Distribution to use for volatility models ('normal', 'studentst', or 'skewstudent')
    window_length : str
        Length of sliding windows as string (e.g., '30d')
    n_fits : int
        Number of sliding windows for volatility model fitting
    simulations : int
        Number of Monte Carlo simulations for volatility models
    bandwidth : str
        KDE bandwidth method (default: 'silverman')

    Returns:
    --------
    Dict[str, Any]
        Dictionary containing pdf_surface, cdf_surface, x_surface, and moments
    """
    # Validate inputs
    required_columns = ['s', 't', 'r']
    missing_columns = [col for col in required_columns if col not in model_results.columns]
    if missing_columns:
        raise VolyError(f"Required columns missing in model_results: {missing_columns}")

    if len(df_hist) < 2:
        raise VolyError("Not enough data points in df_hist")

    # Determine granularity from df_hist
    minutes_diff = (df_hist.index[1] - df_hist.index[0]).total_seconds() / 60
    minutes_per_period = max(1, int(minutes_diff))

    # Validate method and model parameters
    valid_methods = ['garch', 'egarch', 'basic']
    valid_distributions = ['normal', 'studentst', 'skewstudent']

    method = method.lower()
    distribution = distribution.lower()

    if method not in valid_methods:
        raise VolyError(f"Invalid method: {method}. Must be one of {valid_methods}")

    if method in ['garch', 'egarch'] and distribution not in valid_distributions:
        raise VolyError(f"Invalid distribution: {distribution}. Must be one of {valid_distributions}")

    # Calculate log returns from price history
    log_returns = np.log(df_hist['close'] / df_hist['close'].shift(1)) * 100
    log_returns = log_returns.dropna().values

    # Fit volatility model if using GARCH or EGARCH
    vol_model = None
    if method in ['garch', 'egarch']:
        model_type = method  # Use method as model_type
        logger.info(
            f"Using {model_type.upper()} with {distribution} distribution, {n_fits} fits, {simulations} simulations")

        vol_model = fit_volatility_model(
            log_returns=log_returns,
            df_hist=df_hist,
            model_type=model_type,
            distribution=distribution,
            window_length=window_length,
            n_fits=n_fits
        )
    elif method == 'basic':
        logger.info(f"Using basic returns-based KDE method with bandwidth {bandwidth}")

    # Initialize result containers
    pdf_surface = {}
    cdf_surface = {}
    x_surface = {}
    all_moments = {}

    # Process each maturity
    for i in model_results.index:
        # Get parameters for this maturity
        s = model_results.loc[i, 's']  # Current spot price
        r = model_results.loc[i, 'r']  # Risk-free rate
        t = model_results.loc[i, 't']  # Time to maturity in years

        # Get domain grids
        LM = np.linspace(domain_params[0], domain_params[1], domain_params[2])
        M = np.exp(LM)  # Moneyness
        R = M - 1  # Returns
        K = s / M  # Strike prices

        # For time scaling calculations
        tau_days_float = t * 365.25  # Exact number of days
        n_periods = max(1, int(t * 365.25 * 24 * 60 / minutes_per_period))

        logger.info(f"Processing HD for maturity {i} (t={t:.4f} years, {tau_days_float:.2f} days)")

        if method == 'basic':
            # Simple returns-based method
            # Filter historical data for this maturity's lookback period
            start_date = pd.Timestamp.now() - pd.Timedelta(days=int(t * 365.25))
            maturity_hist = df_hist[df_hist.index >= start_date].copy()

            if len(maturity_hist) < 10:
                logger.warning(f"Not enough historical data for maturity {i}, skipping.")
                continue

            # Calculate scaled returns
            maturity_hist['log_returns'] = np.log(maturity_hist['close'] / maturity_hist['close'].shift(1)) * np.sqrt(
                n_periods)
            maturity_hist = maturity_hist.dropna()

            returns = maturity_hist['log_returns'].values
            if len(returns) < 2:
                logger.warning(f"Not enough valid returns for maturity {i}, skipping.")
                continue

            # Girsanov adjustment to shift to risk-neutral measure
            mu_scaled = returns.mean()
            sigma_scaled = returns.std()
            expected_risk_neutral_mean = (r - 0.5 * sigma_scaled ** 2) * np.sqrt(t)
            adjustment = mu_scaled - expected_risk_neutral_mean
            adj_returns = returns - adjustment

            # Create HD and normalize
            f = stats.gaussian_kde(adj_returns, bw_method=bandwidth)
            pdf_values = f(LM)

            # Transform according to return domain
            pdf_lm = pdf_values
            pdf_m = pdf_lm / M
            pdf_k = pdf_lm / K
            pdf_r = pdf_lm / (1 + R)

            # No model parameters to include
            model_params = None

        elif method in ['garch', 'egarch']:
            # Volatility model-based method
            if vol_model is None:
                logger.warning(f"Volatility model fitting failed, skipping maturity {i}")
                continue

            # Simulate paths with the volatility model
            horizon = max(1, int(tau_days_float))
            simulated_returns, simulated_mu = simulate_volatility_paths(
                vol_model,
                horizon,
                simulations
            )

            # Scale the simulated returns to match target time horizon
            scaling_factor = np.sqrt(n_periods / tau_days_float)
            scaled_returns = simulated_returns * scaling_factor

            # Risk-neutral adjustment
            mu_scaled = scaled_returns.mean()
            sigma_scaled = scaled_returns.std()
            expected_risk_neutral_mean = (r - 0.5 * (sigma_scaled / 100) ** 2) * 100 * np.sqrt(t)
            adjustment = mu_scaled - expected_risk_neutral_mean
            risk_neutral_returns = scaled_returns - adjustment

            # Convert to terminal prices
            simulated_prices = s * np.exp(risk_neutral_returns / 100)

            # Convert to moneyness domain (x-domain)
            simulated_moneyness = s / simulated_prices

            # Perform KDE to get PDF
            kde = stats.gaussian_kde(simulated_moneyness, bw_method=bandwidth)
            pdf_values = kde(M)

            # Transform according to return domain
            pdf_m = pdf_values
            pdf_lm = pdf_m * M
            pdf_k = pdf_lm / K
            pdf_r = pdf_lm / (1 + R)

            # Include volatility model params in moments
            avg_params = vol_model['avg_params']
            param_names = vol_model['param_names']
            model_params = {name.replace('[1]', ''): value for name, value in zip(param_names, avg_params)}
            model_params['model_type'] = method
            model_params['distribution'] = distribution

            # Add persistence for GARCH models
            if method == 'garch':
                model_params['persistence'] = model_params.get('alpha', 0) + model_params.get('beta', 0)
        else:
            continue  # Skip if invalid method

        # Ensure density integrates to 1
        dx = LM[1] - LM[0]
        total_area = np.sum(pdf_values * dx)
        if total_area <= 0:
            logger.warning(f"Invalid density (area <= 0) for maturity {i}, skipping.")
            continue

        pdf_values = pdf_values / total_area

        # Calculate CDF
        cdf = np.cumsum(pdf_lm * dx)
        cdf = np.minimum(cdf / cdf[-1], 1.0)  # Ensure CDF is between 0 and 1

        # Select appropriate domain and calculate moments
        if return_domain == 'log_moneyness':
            x = LM
            pdf = pdf_lm
            moments = get_all_moments(x, pdf, model_params)
        elif return_domain == 'moneyness':
            x = M
            pdf = pdf_m
            moments = get_all_moments(x, pdf, model_params)
        elif return_domain == 'returns':
            x = R
            pdf = pdf_r
            moments = get_all_moments(x, pdf, model_params)
        elif return_domain == 'strikes':
            x = K
            pdf = pdf_k
            moments = get_all_moments(x, pdf, model_params)
        else:
            raise VolyError(f"Unsupported return_domain: {return_domain}")

        # Store results
        pdf_surface[i] = pdf
        cdf_surface[i] = cdf
        x_surface[i] = x
        all_moments[i] = moments

    # Check if we have any valid results
    if not pdf_surface:
        raise VolyError("No valid densities could be calculated. Check your input data.")

    # Create DataFrame with moments
    moments = pd.DataFrame(all_moments).T

    logger.info(f"Historical density calculation complete using {method} method")

    return {
        'pdf_surface': pdf_surface,
        'cdf_surface': cdf_surface,
        'x_surface': x_surface,
        'moments': moments
    }
