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
from arch.univariate import GARCH, EGARCH


@catch_exception
def get_historical_data(currency, lookback_days, granularity, exchange_name):
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
    df_hist : pandas.DataFrame containing the historical price data with OHLCV columns.
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
    while True:
        from_ts = ohlcv[-1][0]
        new_ohlcv = exchange.fetch_ohlcv(symbol, granularity, since=from_ts, limit=1000)
        ohlcv.extend(new_ohlcv)
        if len(new_ohlcv) != 1000:
            break

    # Convert to DataFrame
    df_hist = pd.DataFrame(ohlcv, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df_hist['date'] = pd.to_datetime(df_hist['date'], unit='ms')
    df_hist.set_index('date', inplace=True)
    df_hist = df_hist.sort_index(ascending=True)

    print(f"Data fetched successfully: {len(df_hist)} rows from {df_hist.index[0]} to {df_hist.index[-1]}")

    return df_hist


@catch_exception
def parse_window_length(window_length, df_hist):
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
    if not window_length.endswith('d'):
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
def fit_volatility_model(log_returns, df_hist, model_type='garch', distribution='normal', window_length='30d',
                         n_fits=400):
    """
    Fit a volatility model (GARCH or EGARCH) to log returns.

    Args:
        log_returns: Array of log returns
        df_hist: DataFrame with historical price data
        model_type: Type of volatility model ('garch' or 'egarch')
        distribution: Distribution type ('normal', 'studentst', or 'skewstudent')
        window_length: Length of each window as a string (e.g., '30d')
        n_fits: Number of sliding windows

    Returns:
        Dict with model parameters and processes
    """
    # Parse window length
    window_points = parse_window_length(window_length, df_hist)

    if len(log_returns) < window_points + n_fits:
        raise VolyError(f"Not enough data points. Need at least {window_points + n_fits}, got {len(log_returns)}")

    # Adjust window sizes if necessary
    n_fits = min(n_fits, len(log_returns) // 3)
    window_points = min(window_points, len(log_returns) // 3)

    start = window_points + n_fits
    end = n_fits

    # Different number of parameters based on model type and distribution
    if model_type.lower() == 'garch':
        if distribution.lower() == 'normal':
            n_params = 4  # mu, omega, alpha, beta
        elif distribution.lower() == 'studentst':
            n_params = 5  # mu, omega, alpha, beta, nu
        else:  # skewstudent
            n_params = 6  # mu, omega, alpha, beta, nu, lambda (skew)
    else:  # egarch
        if distribution.lower() == 'normal':
            n_params = 5  # mu, omega, alpha, gamma, beta
        elif distribution.lower() == 'studentst':
            n_params = 6  # mu, omega, alpha, gamma, beta, nu
        else:  # skewstudent
            n_params = 7  # mu, omega, alpha, gamma, beta, nu, lambda (skew)

    parameters = np.zeros((n_fits, n_params))
    z_process = []

    logger.info(f"Fitting {model_type.upper()} model with {distribution} distribution using {n_fits} windows...")

    for i in range(n_fits):
        window = log_returns[end - i - 1:start - i - 1]
        data = window - np.mean(window)

        try:
            # Configure model based on type and distribution
            if model_type.lower() == 'garch':
                model = arch_model(data, vol='GARCH', p=1, q=1, dist=distribution.lower())
            else:  # egarch
                model = arch_model(data, vol='EGARCH', p=1, o=1, q=1, dist=distribution.lower())

            fit_result = model.fit(disp='off')

            # Extract parameters based on model type and distribution
            params_dict = fit_result.params.to_dict()

            if model_type.lower() == 'garch':
                mu = params_dict.get("mu", 0)
                omega = params_dict.get("omega", 0)
                alpha = params_dict.get("alpha[1]", 0)
                beta = params_dict.get("beta[1]", 0)

                if distribution.lower() == 'normal':
                    parameters[i, :] = [mu, omega, alpha, beta]
                elif distribution.lower() == 'studentst':
                    nu = params_dict.get("nu", 0)
                    parameters[i, :] = [mu, omega, alpha, beta, nu]
                else:  # skewstudent
                    nu = params_dict.get("nu", 0)
                    lam = params_dict.get("lambda", 0)
                    parameters[i, :] = [mu, omega, alpha, beta, nu, lam]
            else:  # egarch
                mu = params_dict.get("mu", 0)
                omega = params_dict.get("omega", 0)
                alpha = params_dict.get("alpha[1]", 0)
                gamma = params_dict.get("gamma[1]", 0)
                beta = params_dict.get("beta[1]", 0)

                if distribution.lower() == 'normal':
                    parameters[i, :] = [mu, omega, alpha, gamma, beta]
                elif distribution.lower() == 'studentst':
                    nu = params_dict.get("nu", 0)
                    parameters[i, :] = [mu, omega, alpha, gamma, beta, nu]
                else:  # skewstudent
                    nu = params_dict.get("nu", 0)
                    lam = params_dict.get("lambda", 0)
                    parameters[i, :] = [mu, omega, alpha, gamma, beta, nu, lam]

            # Get last innovation
            residuals = fit_result.resid
            conditional_vol = fit_result.conditional_volatility
            z_t = residuals[-1] / conditional_vol[-1]
            z_process.append(z_t)

        except Exception as e:
            logger.warning(f"Model fit failed for window {i}: {str(e)}")

    # Clean up any failed fits
    if len(z_process) < n_fits / 2:
        raise VolyError("Too many model fits failed. Check your data.")

    avg_params = np.mean(parameters, axis=0)
    std_params = np.std(parameters, axis=0)

    return {
        'parameters': parameters,
        'avg_params': avg_params,
        'std_params': std_params,
        'z_process': np.array(z_process),
        'model_type': model_type,
        'distribution': distribution,
        'param_names': get_param_names(model_type, distribution)
    }


def get_param_names(model_type, distribution):
    """Get parameter names based on model type and distribution."""
    if model_type.lower() == 'garch':
        if distribution.lower() == 'normal':
            return ['mu', 'omega', 'alpha', 'beta']
        elif distribution.lower() == 'studentst':
            return ['mu', 'omega', 'alpha', 'beta', 'nu']
        else:  # skewstudent
            return ['mu', 'omega', 'alpha', 'beta', 'nu', 'lambda']
    else:  # egarch
        if distribution.lower() == 'normal':
            return ['mu', 'omega', 'alpha', 'gamma', 'beta']
        elif distribution.lower() == 'studentst':
            return ['mu', 'omega', 'alpha', 'gamma', 'beta', 'nu']
        else:  # skewstudent
            return ['mu', 'omega', 'alpha', 'gamma', 'beta', 'nu', 'lambda']


@catch_exception
def simulate_volatility_paths(vol_model, horizon, simulations=5000, variate_parameters=True):
    """
    Simulate future paths using a fitted volatility model.

    Args:
        vol_model: Dict with volatility model parameters
        horizon: Number of steps to simulate
        simulations: Number of paths to simulate
        variate_parameters: Whether to vary parameters between simulations

    Returns:
        Array of simulated log returns
    """
    parameters = vol_model['parameters']
    z_process = vol_model['z_process']
    model_type = vol_model['model_type']
    distribution = vol_model['distribution']
    param_names = vol_model['param_names']

    # Use mean parameters as starting point
    pars = vol_model['avg_params'].copy()
    bounds = vol_model['std_params'].copy()

    # Log parameters
    param_str = ", ".join([f"{name}={par:.6f}" for name, par in zip(param_names, pars)])
    logger.info(f"{model_type.upper()} parameters: {param_str}")

    # Create KDE for innovations based on distribution
    if distribution.lower() == 'normal':
        # Use standard normal for normal distribution
        def sample_innovation(size=1):
            return np.random.normal(0, 1, size=size)
    else:
        # Use KDE for non-normal distributions to capture empirical distribution
        kde = stats.gaussian_kde(z_process, bw_method='silverman')  # original code doesn't include bw_method
        z_range = np.linspace(min(z_process), max(z_process), 1000)
        z_prob = kde(z_range)
        z_prob = z_prob / np.sum(z_prob)

        def sample_innovation(size=1):
            return np.random.choice(z_range, size=size, p=z_prob)

    # Simulate paths
    simulated_returns = np.zeros(simulations)

    for i in range(simulations):
        if (i + 1) % (simulations // 10) == 0:
            logger.info(f"Simulation progress: {i + 1}/{simulations}")

        # Optionally vary parameters
        if variate_parameters and (i + 1) % (simulations // 20) == 0:
            new_pars = []
            for j, (par, bound) in enumerate(zip(pars, bounds)):
                var = bound ** 2 / len(parameters)
                new_par = np.random.normal(par, var)
                # Ensure omega is positive, betas are between 0 and 1, etc.
                if j >= 1 and new_par <= 0:
                    new_par = 0.01
                new_pars.append(new_par)
            sim_pars = new_pars
        else:
            sim_pars = pars.copy()

        # Initialize variables based on model type
        if model_type.lower() == 'garch':
            if distribution.lower() == 'normal':
                mu, omega, alpha, beta = sim_pars
                sigma2 = omega / (1 - alpha - beta)
            elif distribution.lower() == 'studentst':
                mu, omega, alpha, beta, nu = sim_pars
                sigma2 = omega / (1 - alpha - beta)
            else:  # skewstudent
                mu, omega, alpha, beta, nu, lam = sim_pars
                sigma2 = omega / (1 - alpha - beta)
        else:  # egarch
            if distribution.lower() == 'normal':
                mu, omega, alpha, gamma, beta = sim_pars
                log_sigma2 = omega / (1 - beta)
                sigma2 = np.exp(log_sigma2)
            elif distribution.lower() == 'studentst':
                mu, omega, alpha, gamma, beta, nu = sim_pars
                log_sigma2 = omega / (1 - beta)
                sigma2 = np.exp(log_sigma2)
            else:  # skewstudent
                mu, omega, alpha, gamma, beta, nu, lam = sim_pars
                log_sigma2 = omega / (1 - beta)
                sigma2 = np.exp(log_sigma2)

        returns_sum = 0

        # Simulate path
        for _ in range(horizon):
            # Sample innovation
            z = sample_innovation()

            # Update volatility and returns based on model type
            if model_type.lower() == 'garch':
                # Calculate return
                e = z * np.sqrt(sigma2)
                returns_sum += e + mu

                # Update GARCH volatility
                sigma2 = omega + alpha * e ** 2 + beta * sigma2
            else:  # egarch
                # Calculate return
                e = z * np.sqrt(sigma2)
                returns_sum += e + mu

                # Update EGARCH volatility
                abs_z = abs(z)
                log_sigma2 = omega + beta * log_sigma2 + alpha * (abs_z - np.sqrt(2 / np.pi)) + gamma * z
                sigma2 = np.exp(log_sigma2)

        simulated_returns[i] = returns_sum

    return simulated_returns, mu * horizon


def get_hd_surface(model_results: pd.DataFrame,
                   df_hist: pd.DataFrame,
                   domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness',
                   method: str = 'arch_returns',
                   model_type: str = 'garch',
                   distribution: str = 'normal',
                   **kwargs) -> Dict[str, Any]:
    """
    Generate historical density surface from historical price data.

    Parameters:
        model_results: DataFrame with model parameters and maturities
        df_hist: DataFrame with historical price data
        domain_params: Tuple of (min, max, num_points) for x-domain
        return_domain: Domain for x-axis values ('log_moneyness', 'moneyness', 'returns', 'strikes')
        method: Method to use for HD estimation ('hist_returns' or 'arch_returns')
        model_type: Type of volatility model to use ('garch' or 'egarch')
        distribution: Distribution to use ('normal', 'studentst', or 'skewstudent')
        **kwargs: Additional parameters for specific methods:
            For volatility models ('garch'/'egarch' method):
                n_fits: Number of sliding windows (default: 400)
                simulations: Number of Monte Carlo simulations (default: 5000)
                window_length: Length of sliding windows as string (default: '30d')
                variate_parameters: Whether to vary parameters (default: True)
                bandwidth: KDE bandwidth (default: 'silverman')
            For 'hist_returns' method:
                bandwidth: KDE bandwidth (default: 'silverman')

    Returns:
        Dictionary containing pdf_surface, cdf_surface, x_surface, and moments
    """
    # Check if required columns are present
    required_columns = ['s', 't', 'r']
    missing_columns = [col for col in required_columns if col not in model_results.columns]
    if missing_columns:
        raise VolyError(f"Required columns missing in model_results: {missing_columns}")

    # Determine granularity from df_hist
    if len(df_hist) > 1:
        # Calculate minutes between consecutive timestamps
        minutes_diff = (df_hist.index[1] - df_hist.index[0]).total_seconds() / 60
        minutes_per_period = int(minutes_diff)
    else:
        raise VolyError("Cannot determine granularity from df_hist.")

    # Validate model_type and distribution
    valid_model_types = ['garch', 'egarch']
    valid_distributions = ['normal', 'studentst', 'skewstudent']

    if model_type.lower() not in valid_model_types:
        raise VolyError(f"Invalid model_type: {model_type}. Must be one of {valid_model_types}")

    if distribution.lower() not in valid_distributions:
        raise VolyError(f"Invalid distribution: {distribution}. Must be one of {valid_distributions}")

    # Get method-specific parameters
    if method == 'arch_returns':
        n_fits = kwargs.get('n_fits', 400)
        simulations = kwargs.get('simulations', 5000)
        window_length = kwargs.get('window_length', '30d')
        variate_parameters = kwargs.get('variate_parameters', True)
        bandwidth = kwargs.get('bandwidth', 'silverman')
        logger.info(
            f"Using {model_type.upper()} method with {distribution} distribution, {n_fits} fits, {simulations} simulations")
    elif method == 'hist_returns':
        bandwidth = kwargs.get('bandwidth', 'silverman')
        logger.info(f"Using returns-based KDE method with bandwidth {bandwidth}")
    else:
        raise VolyError(f"Unknown method: {method}. Use 'hist_returns', 'arch_returns'.")

    # Calculate log returns from price history
    log_returns = np.log(df_hist['close'] / df_hist['close'].shift(1)) * 100
    log_returns = log_returns.dropna().values

    # Fit volatility model once if using garch/egarch method
    vol_model = None
    if method == 'arch_returns':
        vol_model = fit_volatility_model(
            log_returns,
            df_hist,
            model_type=model_type,
            distribution=distribution,
            window_length=window_length,
            n_fits=n_fits
        )

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

        if method == 'hist_returns':
            # Standard returns-based method
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

        elif method == 'arch_returns':
            # Volatility model-based method
            if vol_model is None:
                logger.warning(f"Volatility model fitting failed, skipping maturity {i}")
                continue

            # Simulate paths with the volatility model
            horizon = max(1, int(tau_days_float))
            simulated_returns, simulated_mu = simulate_volatility_paths(
                vol_model,
                horizon,
                simulations,
                variate_parameters
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

            # Convert to moneyness domain
            simulated_moneyness = s / simulated_prices

            # Perform KDE to get PDF
            kde = stats.gaussian_kde(simulated_moneyness, bw_method=bandwidth)
            pdf_values = kde(M)

            # Include volatility model params in moments
            avg_params = vol_model['avg_params']
            param_names = vol_model['param_names']
            model_params = {name: value for name, value in zip(param_names, avg_params)}
            model_params['model_type'] = model_type
            model_params['distribution'] = distribution

            # Add persistence for GARCH-type models
            if model_type.lower() == 'garch':
                model_params['persistence'] = model_params.get('alpha', 0) + model_params.get('beta', 0)
        else:
            continue  # Skip this maturity if method is invalid

        # Ensure density integrates to 1
        dx = LM[1] - LM[0]
        total_area = np.sum(pdf_values * dx)
        if total_area <= 0:
            logger.warning(f"Invalid density (area <= 0) for maturity {i}, skipping.")
            continue

        pdf_values = pdf_values / total_area

        # Common processing for both methods

        # Transform densities to various domains
        if method == 'hist_returns':
            pdf_lm = pdf_values
            pdf_m = pdf_lm / M
            pdf_k = pdf_lm / K
            pdf_r = pdf_lm / (1 + R)
        else:  # volatility models
            pdf_m = pdf_values
            pdf_lm = pdf_m * M
            pdf_k = pdf_lm / K
            pdf_r = pdf_lm / (1 + R)

        # Calculate CDF
        cdf = np.cumsum(pdf_lm * dx)
        cdf = np.minimum(cdf / cdf[-1], 1.0)

        # Select appropriate domain and calculate moments
        if return_domain == 'log_moneyness':
            x = LM
            pdf = pdf_lm
            moments = get_all_moments(x, pdf, model_params if method == 'arch_returns' else None)
        elif return_domain == 'moneyness':
            x = M
            pdf = pdf_m
            moments = get_all_moments(x, pdf, model_params if method == 'arch_returns' else None)
        elif return_domain == 'returns':
            x = R
            pdf = pdf_r
            moments = get_all_moments(x, pdf, model_params if method == 'arch_returns' else None)
        elif return_domain == 'strikes':
            x = K
            pdf = pdf_k
            moments = get_all_moments(x, pdf, model_params if method == 'arch_returns' else None)
        else:
            raise VolyError(f"Unsupported return_domain: {return_domain}")

        # Store results
        pdf_surface[i] = pdf
        cdf_surface[i] = cdf
        x_surface[i] = x
        all_moments[i] = moments

    # Create DataFrame with moments
    moments = pd.DataFrame(all_moments).T

    logger.info(
        f"Historical density calculation complete using {method} method with {model_type} model and {distribution} distribution")

    return {
        'pdf_surface': pdf_surface,
        'cdf_surface': cdf_surface,
        'x_surface': x_surface,
        'moments': moments
    }
