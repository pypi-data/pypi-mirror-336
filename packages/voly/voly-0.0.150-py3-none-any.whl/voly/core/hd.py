"""
This module handles calculating historical densities from
time series of prices and converting them to implied volatility smiles.
"""

import ccxt
import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union, Any, Callable
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
    -----------
    currency : str
        The cryptocurrency to fetch data for (e.g., 'BTC', 'ETH')
    lookback_days : str
        The lookback period in days, formatted as '90d', '30d', etc.
    granularity : str
        The time interval for data points (e.g., '15m', '1h', '1d')
    exchange_name : str
        The exchange to fetch data from (default: 'binance')

    Returns:
    --------
    pd.DataFrame
        Historical price data with OHLCV columns and datetime index
    """
    # Validate inputs
    if not lookback_days.endswith('d'):
        raise VolyError("lookback_days should be in format '90d', '30d', etc.")

    try:
        # Get the exchange class from ccxt
        exchange_class = getattr(ccxt, exchange_name.lower())
        exchange = exchange_class({'enableRateLimit': True})
    except (AttributeError, TypeError):
        raise VolyError(f"Exchange '{exchange_name}' not found in ccxt. Please check the exchange name.")

    # Form the trading pair symbol
    symbol = f"{currency}/USDT"

    # Convert lookback_days to timestamp
    days_ago = int(lookback_days[:-1])
    date_start = (dt.datetime.now() - dt.timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
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

    logger.info(f"Data fetched successfully: {len(df_hist)} rows from {df_hist.index[0]} to {df_hist.index[-1]}")

    return df_hist


@catch_exception
def parse_window_length(window_length: str, df_hist: pd.DataFrame) -> int:
    """
    Convert window length string (e.g., '30d') to number of data points.

    Parameters:
    -----------
    window_length : str
        Window length in days, formatted as '7d', '30d', etc.
    df_hist : pd.DataFrame
        Historical data DataFrame with datetime index

    Returns:
    --------
    int
        Number of data points corresponding to the window length
    """
    # Validate inputs
    if not isinstance(window_length, str) or not window_length.endswith('d'):
        raise VolyError("window_length should be in format '7d', '30d', etc.")

    if len(df_hist) < 2:
        raise VolyError("Historical data must contain at least 2 points to calculate granularity")

    # Extract number of days
    days = int(window_length[:-1])

    # Calculate average time delta between data points
    avg_delta = (df_hist.index[-1] - df_hist.index[0]).total_seconds() / (len(df_hist) - 1)

    # Convert to days and calculate points per window
    days_per_point = avg_delta / (24 * 60 * 60)
    n_points = int(days / days_per_point)

    # Ensure minimum number of points
    return max(n_points, 10)


def get_param_names(model_type: str, distribution: str) -> List[str]:
    """
    Get parameter names for a volatility model and distribution.

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
    # GARCH(1,1) parameters
    if model_type.lower() == 'garch':
        if distribution.lower() == 'normal':
            return ['mu', 'omega', 'alpha[1]', 'beta[1]']
        elif distribution.lower() == 'studentst':
            return ['mu', 'omega', 'alpha[1]', 'beta[1]', 'nu']
        elif distribution.lower() == 'skewstudent':
            return ['mu', 'omega', 'alpha[1]', 'beta[1]', 'nu', 'lambda']

    # EGARCH(1,1,1) parameters
    elif model_type.lower() == 'egarch':
        if distribution.lower() == 'normal':
            return ['mu', 'omega', 'alpha[1]', 'gamma[1]', 'beta[1]']
        elif distribution.lower() == 'studentst':
            return ['mu', 'omega', 'alpha[1]', 'gamma[1]', 'beta[1]', 'nu']
        elif distribution.lower() == 'skewstudent':
            return ['mu', 'omega', 'alpha[1]', 'gamma[1]', 'beta[1]', 'nu', 'lambda']

    raise VolyError(f"Invalid model_type '{model_type}' or distribution '{distribution}'")


@catch_exception
def fit_volatility_model(log_returns: np.ndarray,
                         df_hist: pd.DataFrame,
                         model_type: str = 'garch',
                         distribution: str = 'normal',
                         window_length: str = '30d',
                         n_fits: int = 400) -> Dict[str, Any]:
    """
    Fit a volatility model (GARCH or EGARCH) to historical returns.

    Parameters:
    -----------
    log_returns : np.ndarray
        Array of log returns (percent)
    df_hist : pd.DataFrame
        Historical price data
    model_type : str
        Type of volatility model ('garch' or 'egarch')
    distribution : str
        Distribution type ('normal', 'studentst', or 'skewstudent')
    window_length : str
        Length of sliding window in days (e.g., '30d')
    n_fits : int
        Number of sliding windows to fit

    Returns:
    --------
    Dict[str, Any]
        Dictionary with model parameters and fitting results
    """
    # Parse window length
    window_points = parse_window_length(window_length, df_hist)

    # Validate data
    if len(log_returns) < window_points + n_fits:
        raise VolyError(f"Not enough data points. Need at least {window_points + n_fits}, got {len(log_returns)}")

    # Adjust window sizes to avoid overfitting
    n_fits = min(n_fits, max(100, len(log_returns) // 3))
    window_points = min(window_points, max(20, len(log_returns) // 3))

    # Calculate start and end indices for sliding windows
    start_idx = window_points + n_fits
    end_idx = n_fits

    # Get parameter names for the model
    param_names = get_param_names(model_type, distribution)
    n_params = len(param_names)

    # Initialize arrays for parameters and innovations
    parameters = np.zeros((n_fits, n_params))
    z_process = []

    logger.info(f"Fitting {model_type.upper()} model with {distribution} distribution "
                f"using {n_fits} windows of {window_length}")

    # Fit models with sliding windows
    for i in range(n_fits):
        # Log progress
        if i % (n_fits // 10) == 0:
            logger.info(f"Fitting progress: {i}/{n_fits}")

        # Check if we have enough data for this window
        if end_idx - i - 1 < 0 or start_idx - i - 1 > len(log_returns):
            continue

        # Extract window data
        window = log_returns[end_idx - i - 1:start_idx - i - 1]

        # Skip invalid windows
        if len(window) < 10 or np.isnan(window).any() or np.isinf(window).any():
            continue

        # Mean-center the data for numerical stability
        data = window - np.mean(window)

        try:
            # Configure and fit model
            if model_type.lower() == 'garch':
                model = arch_model(data, vol='GARCH', p=1, q=1, dist=distribution.lower())
            else:  # egarch
                model = arch_model(data, vol='EGARCH', p=1, o=1, q=1, dist=distribution.lower())

            # Fit with optimization settings
            fit_result = model.fit(disp='off', options={'maxiter': 1000})

            # Extract parameters
            params_dict = fit_result.params.to_dict()
            param_values = [params_dict.get(param, 0) for param in param_names]
            parameters[i, :] = param_values

            # Extract standardized residuals (innovations)
            residuals = fit_result.resid
            conditional_vol = fit_result.conditional_volatility

            if len(residuals) > 0 and len(conditional_vol) > 0:
                z_t = residuals[-1] / conditional_vol[-1]
                if not np.isnan(z_t) and not np.isinf(z_t):
                    z_process.append(z_t)

        except Exception as e:
            logger.warning(f"Model fit failed for window {i}: {str(e)}")

    # Check if we have enough successful fits
    if len(z_process) < n_fits / 2:
        raise VolyError(f"Too many model fits failed ({len(z_process)}/{n_fits}). Check your data.")

    # Remove failed fits
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


@catch_exception
def create_innovation_sampler(vol_model: Dict[str, Any]) -> Callable:
    """
    Create a function to sample innovations based on the volatility model.

    Parameters:
    -----------
    vol_model : Dict[str, Any]
        Volatility model information from fit_volatility_model()

    Returns:
    --------
    Callable
        Function that returns random innovations when called
    """
    distribution = vol_model['distribution']
    z_process = vol_model['z_process']

    if distribution.lower() == 'normal':
        # Use standard normal for normal distribution
        def sample_innovation(size=1):
            return np.random.normal(0, 1, size=size)
    else:
        # Use KDE for non-normal distributions to capture empirical distribution
        kde = stats.gaussian_kde(z_process, bw_method='silverman')
        z_range = np.linspace(min(z_process), max(z_process), 1000)
        z_prob = kde(z_range)
        z_prob = z_prob / np.sum(z_prob)

        def sample_innovation(size=1):
            return np.random.choice(z_range, size=size, p=z_prob)

    return sample_innovation


@catch_exception
def generate_volatility_paths(vol_model: Dict[str, Any],
                              horizon: int,
                              simulations: int = 5000) -> Tuple[np.ndarray, float]:
    """
    Simulate future price paths using a fitted volatility model.

    Parameters:
    -----------
    vol_model : Dict[str, Any]
        Volatility model information from fit_volatility_model()
    horizon : int
        Number of time steps to simulate
    simulations : int
        Number of paths to simulate

    Returns:
    --------
    Tuple[np.ndarray, float]
        Array of simulated returns and the drift term
    """
    # Extract model information
    parameters = vol_model['parameters']
    model_type = vol_model['model_type']
    distribution = vol_model['distribution']
    param_names = vol_model['param_names']

    # Get mean parameters
    pars = vol_model['avg_params'].copy()
    bounds = vol_model['std_params'].copy()

    # Create parameter dictionary for easier access
    param_dict = {name: value for name, value in zip(param_names, pars)}

    # Log parameters
    param_str = ", ".join([f"{name}={param_dict.get(name, 0):.6f}" for name in param_names])
    logger.info(f"{model_type.upper()} parameters: {param_str}")

    # Create innovation sampler
    sample_innovation = create_innovation_sampler(vol_model)

    # Initialize results array
    simulated_returns = np.zeros(simulations)
    mu = param_dict.get('mu', 0)

    logger.info(f"Simulating {simulations} paths for horizon {horizon}")

    # Simulate paths
    for i in range(simulations):
        # Log progress
        if (i + 1) % (simulations // 10) == 0:
            logger.info(f"Simulation progress: {i + 1}/{simulations}")

        # Vary parameters periodically for robustness
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
            # Extract GARCH parameters
            omega = sim_params.get('omega', 0)
            alpha = sim_params.get('alpha[1]', 0)
            beta = sim_params.get('beta[1]', 0)

            # Initialize with unconditional variance
            persistence = alpha + beta
            sigma2 = omega / (1 - persistence) if persistence < 1 else omega / 0.99

        else:  # egarch
            # Extract EGARCH parameters
            omega = sim_params.get('omega', 0)
            beta = sim_params.get('beta[1]', 0)

            # Initialize log variance
            log_sigma2 = omega / (1 - beta) if beta < 1 else omega / 0.99
            sigma2 = np.exp(log_sigma2)

        # Initialize return sum
        returns_sum = 0

        # Simulate path
        for _ in range(horizon):
            # Sample innovation
            z = sample_innovation()

            # Update returns and volatility based on model type
            if model_type.lower() == 'garch':
                # Calculate return
                e = z * np.sqrt(sigma2)
                returns_sum += e + mu

                # Update GARCH volatility
                sigma2 = (sim_params.get('omega', 0) +
                          sim_params.get('alpha[1]', 0) * e ** 2 +
                          sim_params.get('beta[1]', 0) * sigma2)

            else:  # egarch
                # Calculate return
                e = z * np.sqrt(sigma2)
                returns_sum += e + mu

                # Extract EGARCH parameters
                gamma = sim_params.get('gamma[1]', 0)
                alpha = sim_params.get('alpha[1]', 0)
                beta = sim_params.get('beta[1]', 0)
                omega = sim_params.get('omega', 0)

                # Update EGARCH volatility
                abs_z = abs(z)
                log_sigma2 = omega + beta * log_sigma2 + alpha * (abs_z - np.sqrt(2 / np.pi)) + gamma * z
                sigma2 = np.exp(log_sigma2)

        # Store final return
        simulated_returns[i] = returns_sum

    return simulated_returns, mu * horizon


@catch_exception
def prepare_domains(domain_params: Tuple[float, float, int],
                    s: float,
                    return_domain: str) -> Dict[str, np.ndarray]:
    """
    Prepare domain arrays for different representations.

    Parameters:
    -----------
    domain_params : Tuple[float, float, int]
        (min_log_moneyness, max_log_moneyness, num_points)
    s : float
        Spot price
    return_domain : str
        Domain for results

    Returns:
    --------
    Dict[str, np.ndarray]
        Dictionary of domain arrays
    """
    # Create log-moneyness grid
    LM = np.linspace(domain_params[0], domain_params[1], domain_params[2])

    # Calculate other domains
    M = np.exp(LM)  # Moneyness
    R = M - 1  # Returns
    K = s / M  # Strike prices

    # Calculate grid spacing
    dx = LM[1] - LM[0]

    return {
        'log_moneyness': LM,
        'moneyness': M,
        'returns': R,
        'strikes': K,
        'dx': dx
    }


@catch_exception
def calculate_basic_density(df_hist: pd.DataFrame,
                            t: float,
                            r: float,
                            n_periods: int,
                            domains: Dict[str, np.ndarray],
                            bandwidth: str = 'silverman') -> Dict[str, np.ndarray]:
    """
    Calculate historical density using KDE of historical returns.

    Parameters:
    -----------
    df_hist : pd.DataFrame
        Historical price data
    t : float
        Time to maturity in years
    r : float
        Risk-free rate
    n_periods : int
        Number of periods to scale returns
    domains : Dict[str, np.ndarray]
        Domain arrays
    bandwidth : str
        KDE bandwidth method

    Returns:
    --------
    Dict[str, np.ndarray]
        Dictionary of PDFs in different domains
    """
    # Extract domains
    LM = domains['log_moneyness']
    M = domains['moneyness']
    R = domains['returns']
    K = domains['strikes']
    dx = domains['dx']

    # Filter historical data for the maturity's lookback period - use exact time to expiry
    lookback_days = t * 365.25  # Exact number of days to expiry
    start_date = pd.Timestamp.now() - pd.Timedelta(days=lookback_days)
    maturity_hist = df_hist[df_hist.index >= start_date].copy()

    # Better diagnostics for debugging
    if len(maturity_hist) < 2:
        raise VolyError(f"Not enough historical data for maturity (t={t:.4f})")

    # Calculate scaled returns
    maturity_hist['log_returns'] = np.log(maturity_hist['close'] / maturity_hist['close'].shift(1)) * np.sqrt(n_periods)
    maturity_hist = maturity_hist.dropna()
    returns = maturity_hist['log_returns'].values

    if len(returns) < 2:
        raise VolyError(f"Not enough valid returns for maturity (t={t:.4f})")

    # Girsanov adjustment to shift to risk-neutral measure
    mu_scaled = returns.mean()
    sigma_scaled = returns.std()
    expected_risk_neutral_mean = (r - 0.5 * sigma_scaled ** 2) * np.sqrt(t)
    adjustment = mu_scaled - expected_risk_neutral_mean
    adj_returns = returns - adjustment

    # Create PDF with KDE
    kde = stats.gaussian_kde(adj_returns, bw_method=bandwidth)
    pdf_lm = kde(LM)

    # Normalize the PDF
    pdf_lm = pdf_lm / np.trapz(pdf_lm, LM)

    # Transform to other domains
    pdf_m = pdf_lm / M
    pdf_k = pdf_lm / K
    pdf_r = pdf_lm / (1 + R)

    # Calculate CDF
    cdf = np.cumsum(pdf_lm * dx)
    cdf = cdf / cdf[-1]

    return {
        'log_moneyness': pdf_lm,
        'moneyness': pdf_m,
        'returns': pdf_r,
        'strikes': pdf_k,
        'cdf': cdf
    }


@catch_exception
def calculate_volatility_density(vol_model: Dict[str, Any],
                                 s: float,
                                 t: float,
                                 r: float,
                                 n_periods: int,
                                 tau_days: float,
                                 domains: Dict[str, np.ndarray],
                                 simulations: int = 5000,
                                 bandwidth: str = 'silverman') -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
    """
    Calculate historical density using volatility model simulation.

    Parameters:
    -----------
    vol_model : Dict[str, Any]
        Volatility model from fit_volatility_model()
    s : float
        Spot price
    t : float
        Time to maturity in years
    r : float
        Risk-free rate
    n_periods : int
        Number of periods to scale returns
    tau_days : float
        Days to maturity
    domains : Dict[str, np.ndarray]
        Domain arrays
    simulations : int
        Number of Monte Carlo simulations
    bandwidth : str
        KDE bandwidth method

    Returns:
    --------
    Tuple[Dict[str, np.ndarray], Dict[str, Any]]
        Dictionary of PDFs in different domains and model parameters
    """
    # Extract domains
    LM = domains['log_moneyness']
    M = domains['moneyness']
    R = domains['returns']
    K = domains['strikes']
    dx = domains['dx']

    # Simulate paths with the volatility model
    horizon = max(1, int(tau_days))
    simulated_returns, simulated_mu = generate_volatility_paths(
        vol_model,
        horizon,
        simulations
    )

    # Scale the simulated returns to match target time horizon
    scaling_factor = np.sqrt(n_periods / tau_days)
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

    # Calculate PDF with KDE
    kde = stats.gaussian_kde(simulated_moneyness, bw_method=bandwidth)
    pdf_m = kde(M)

    # Normalize the PDF
    pdf_m = pdf_m / np.trapz(pdf_m, M)

    # Transform to other domains
    pdf_lm = pdf_m * M
    pdf_k = pdf_lm / K
    pdf_r = pdf_lm / (1 + R)

    # Calculate CDF
    cdf = np.cumsum(pdf_lm * dx)
    cdf = cdf / cdf[-1]

    # Prepare model parameters for moments
    avg_params = vol_model['avg_params']
    param_names = vol_model['param_names']
    model_params = {name.replace('[1]', ''): value for name, value in zip(param_names, avg_params)}
    model_params['model_type'] = vol_model['model_type']
    model_params['distribution'] = vol_model['distribution']

    # Add persistence for GARCH models
    if vol_model['model_type'] == 'garch':
        model_params['persistence'] = model_params.get('alpha', 0) + model_params.get('beta', 0)

    return {
        'log_moneyness': pdf_lm,
        'moneyness': pdf_m,
        'returns': pdf_r,
        'strikes': pdf_k,
        'cdf': cdf
    }, model_params


@catch_exception
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
        (min_log_moneyness, max_log_moneyness, num_points)
    return_domain : str
        Domain for results ('log_moneyness', 'moneyness', 'returns', 'strikes')
    method : str
        Method for HD estimation ('garch', 'egarch', 'basic')
    distribution : str
        Distribution for volatility models ('normal', 'studentst', 'skewstudent')
    window_length : str
        Length of sliding windows for model fitting (e.g., '30d')
    n_fits : int
        Number of sliding windows for model fitting
    simulations : int
        Number of Monte Carlo simulations
    bandwidth : str
        KDE bandwidth method

    Returns:
    --------
    Dict[str, Any]
        Dictionary with pdf_surface, cdf_surface, x_surface, and moments
    """
    # Validate inputs
    required_columns = ['s', 't', 'r']
    missing_columns = [col for col in required_columns if col not in model_results.columns]
    if missing_columns:
        raise VolyError(f"Required columns missing in model_results: {missing_columns}")

    if len(df_hist) < 2:
        raise VolyError("Not enough data points in df_hist")

    # Determine granularity from data
    minutes_diff = (df_hist.index[1] - df_hist.index[0]).total_seconds() / 60
    minutes_per_period = max(1, int(minutes_diff))

    # Validate method and distribution
    valid_methods = ['garch', 'egarch', 'basic']
    valid_distributions = ['normal', 'studentst', 'skewstudent']

    method = method.lower()
    distribution = distribution.lower()

    if method not in valid_methods:
        raise VolyError(f"Invalid method: {method}. Must be one of {valid_methods}")

    if method in ['garch', 'egarch'] and distribution not in valid_distributions:
        raise VolyError(f"Invalid distribution: {distribution}. Must be one of {valid_distributions}")

    # Validate return domain
    valid_domains = ['log_moneyness', 'moneyness', 'returns', 'strikes']
    if return_domain not in valid_domains:
        raise VolyError(f"Invalid return_domain: {return_domain}. Must be one of {valid_domains}")

    # Calculate log returns
    log_returns = np.log(df_hist['close'] / df_hist['close'].shift(1)) * 100
    log_returns = log_returns.dropna().values

    # Fit volatility model if needed
    vol_model = None
    if method in ['garch', 'egarch']:
        model_type = method
        logger.info(f"Using {model_type.upper()} with {distribution} distribution")

        vol_model = fit_volatility_model(
            log_returns=log_returns,
            df_hist=df_hist,
            model_type=model_type,
            distribution=distribution,
            window_length=window_length,
            n_fits=n_fits
        )

    # Initialize result containers
    pdf_surface = {}
    cdf_surface = {}
    x_surface = {}
    all_moments = {}

    # Process each maturity
    for i in model_results.index:
        try:
            # Get parameters for this maturity
            s = model_results.loc[i, 's']  # Spot price
            r = model_results.loc[i, 'r']  # Risk-free rate
            t = model_results.loc[i, 't']  # Time to maturity in years

            # Calculate time scaling parameters
            tau_days = t * 365.25  # Days to expiry
            n_periods = max(1, int(tau_days * 24 * 60 / minutes_per_period))  # Number of periods

            logger.info(f"Processing HD for maturity {i} (t={t:.4f} years, {tau_days:.2f} days)")

            # Prepare domains
            domains = prepare_domains(domain_params, s, return_domain)

            # Calculate density based on method
            if method == 'basic':
                pdfs = calculate_basic_density(
                    df_hist=df_hist,
                    t=t,
                    r=r,
                    n_periods=n_periods,
                    domains=domains,
                    bandwidth=bandwidth
                )
                model_params = None

            else:  # 'garch' or 'egarch'
                if vol_model is None:
                    logger.warning(f"Volatility model fitting failed, skipping maturity {i}")
                    continue

                pdfs, model_params = calculate_volatility_density(
                    vol_model=vol_model,
                    s=s,
                    t=t,
                    r=r,
                    n_periods=n_periods,
                    tau_days=tau_days,
                    domains=domains,
                    simulations=simulations,
                    bandwidth=bandwidth
                )

            # Get domain arrays for output
            if return_domain == 'log_moneyness':
                x = domains['log_moneyness']
                pdf = pdfs['log_moneyness']
            elif return_domain == 'moneyness':
                x = domains['moneyness']
                pdf = pdfs['moneyness']
            elif return_domain == 'returns':
                x = domains['returns']
                pdf = pdfs['returns']
            elif return_domain == 'strikes':
                x = domains['strikes']
                pdf = pdfs['strikes']

            # Calculate statistical moments
            moments = get_all_moments(x, pdf, model_params)

            # Store results
            pdf_surface[i] = pdf
            cdf_surface[i] = pdfs['cdf']
            x_surface[i] = x
            all_moments[i] = moments

        except Exception as e:
            logger.warning(f"Failed to calculate HD for maturity {i}: {str(e)}")

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
