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
def fit_garch_model(log_returns, n_fits=400, window_length=365):
    """
    Fit a GARCH(1,1) model to log returns.

    Args:
        log_returns: Array of log returns
        n_fits: Number of sliding windows
        window_length: Length of each window

    Returns:
        Dict with GARCH parameters and processes
    """

    if len(log_returns) < window_length + n_fits:
        raise VolyError(f"Not enough data points. Need at least {window_length + n_fits}, got {len(log_returns)}")

    # Adjust window sizes if necessary
    n_fits = min(n_fits, len(log_returns) // 3)
    window_length = min(window_length, len(log_returns) // 3)

    start = window_length + n_fits
    end = n_fits

    parameters = np.zeros((n_fits, 4))  # [mu, omega, alpha, beta]
    z_process = []

    logger.info(f"Fitting GARCH model with {n_fits} windows...")

    for i in range(n_fits):
        window = log_returns[end - i - 1:start - i - 1]
        data = window - np.mean(window)

        model = arch_model(data, vol='GARCH', p=1, q=1)
        try:
            GARCH_fit = model.fit(disp='off')

            mu, omega, alpha, beta = [
                GARCH_fit.params["mu"],
                GARCH_fit.params["omega"],
                GARCH_fit.params["alpha[1]"],
                GARCH_fit.params["beta[1]"],
            ]
            parameters[i, :] = [mu, omega, alpha, beta]

            # Calculate sigma2 and innovations for last observation
            if i == 0:
                sigma2_tm1 = omega / (1 - alpha - beta)
            else:
                e_tm1 = data.tolist()[-2]
                sigma2_tm1 = omega + alpha * e_tm1 ** 2 + beta * sigma2_tm1

            e_t = data.tolist()[-1]
            sigma2_t = omega + alpha * data.tolist()[-2] ** 2 + beta * sigma2_tm1
            z_t = e_t / np.sqrt(sigma2_t)
            z_process.append(z_t)

        except Exception as e:
            logger.warning(f"GARCH fit failed for window {i}: {str(e)}")

    # Clean up any failed fits
    if len(z_process) < n_fits / 2:
        raise VolyError("Too many GARCH fits failed. Check your data.")

    avg_params = np.mean(parameters, axis=0)
    std_params = np.std(parameters, axis=0)

    return {
        'parameters': parameters,
        'avg_params': avg_params,
        'std_params': std_params,
        'z_process': np.array(z_process)
    }


@catch_exception
def simulate_garch_paths(garch_model, horizon, simulations=5000, variate_parameters=True):
    """
    Simulate future paths using a fitted GARCH model.

    Args:
        garch_model: Dict with GARCH model parameters
        horizon: Number of steps to simulate
        simulations: Number of paths to simulate
        variate_parameters: Whether to vary parameters between simulations

    Returns:
        Array of simulated log returns
    """
    parameters = garch_model['parameters']
    z_process = garch_model['z_process']

    # Use mean parameters as starting point
    pars = garch_model['avg_params'].copy()  # [mu, omega, alpha, beta]
    bounds = garch_model['std_params'].copy()

    mu, omega, alpha, beta = pars
    logger.info(f"GARCH parameters: mu={mu:.6f}, omega={omega:.6f}, alpha={alpha:.6f}, beta={beta:.6f}")

    # Create KDE for innovations
    kde = stats.gaussian_kde(z_process)
    z_range = np.linspace(min(z_process), max(z_process), 1000)
    z_prob = kde(z_range)
    z_prob = z_prob / np.sum(z_prob)

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
                if j >= 1 and new_par <= 0:  # Ensure omega, alpha, beta are positive
                    new_par = 0.01
                new_pars.append(new_par)
            mu, omega, alpha, beta = new_pars

        # Initial values
        sigma2 = omega / (1 - alpha - beta)
        returns_sum = 0

        # Simulate path
        for _ in range(horizon):
            # Sample from innovation distribution
            z = np.random.choice(z_range, p=z_prob)

            # Calculate return and update volatility
            e = z * np.sqrt(sigma2)
            returns_sum += e + mu
            sigma2 = omega + alpha * e ** 2 + beta * sigma2

        simulated_returns[i] = returns_sum

    return simulated_returns, mu * horizon


def get_hd_surface(model_results: pd.DataFrame,
                   df_hist: pd.DataFrame,
                   domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness',
                   method: str = 'garch',
                   **kwargs) -> Dict[str, Any]:
    """
    Generate historical density surface from historical price data.

    Parameters:
        model_results: DataFrame with model parameters and maturities
        df_hist: DataFrame with historical price data
        domain_params: Tuple of (min, max, num_points) for x-domain
        return_domain: Domain for x-axis values ('log_moneyness', 'moneyness', 'returns', 'strikes')
        method: Method to use for HD estimation ('hist_returns' or 'garch')
        **kwargs: Additional parameters for specific methods:
            For 'garch' method:
                n_fits: Number of sliding windows (default: 400)
                simulations: Number of Monte Carlo simulations (default: 5000)
                window_length: Length of sliding windows (default: 365)
                variate_parameters: Whether to vary GARCH parameters (default: True)
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

    # Get method-specific parameters
    if method == 'garch':
        n_fits = kwargs.get('n_fits', 400)
        simulations = kwargs.get('simulations', 5000)
        window_length = kwargs.get('window_length', 365)
        variate_parameters = kwargs.get('variate_parameters', True)
        bandwidth = kwargs.get('bandwidth', 'silverman')
        logger.info(f"Using GARCH method with {n_fits} fits, {simulations} simulations")
    elif method == 'hist_returns':
        bandwidth = kwargs.get('bandwidth', 'silverman')
        logger.info(f"Using returns-based KDE method with bandwidth {bandwidth}")
    else:
        raise VolyError(f"Unknown method: {method}. Use 'hist_returns' or 'garch'.")

    # Calculate log returns from price history
    log_returns = np.log(df_hist['close'] / df_hist['close'].shift(1)) * 100
    log_returns = log_returns.dropna().values

    # Fit GARCH model once if using garch method
    garch_model = None
    if method == 'garch':
        garch_model = fit_garch_model(log_returns, n_fits, window_length)

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
            # Standard returns-based method (your existing implementation)
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

        elif method == 'garch':
            # GARCH-based method
            if garch_model is None:
                logger.warning(f"GARCH model fitting failed, skipping maturity {i}")
                continue

            # Simulate paths with the GARCH model
            horizon = max(1, int(tau_days_float))
            simulated_returns, simulated_mu = simulate_garch_paths(
                garch_model,
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

            # Include GARCH params in moments
            avg_params = garch_model['avg_params']
            model_params = {
                'mu': avg_params[0],
                'omega': avg_params[1],
                'alpha': avg_params[2],
                'beta': avg_params[3],
                'persistence': avg_params[2] + avg_params[3]
            }
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
        else:  # 'garch'
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
            moments = get_all_moments(x, pdf, model_params if method == 'garch' else None)
        elif return_domain == 'moneyness':
            x = M
            pdf = pdf_m
            moments = get_all_moments(x, pdf, model_params if method == 'garch' else None)
        elif return_domain == 'returns':
            x = R
            pdf = pdf_r
            moments = get_all_moments(x, pdf, model_params if method == 'garch' else None)
        elif return_domain == 'strikes':
            x = K
            pdf = pdf_k
            moments = get_all_moments(x, pdf, model_params if method == 'garch' else None)
        else:
            raise VolyError(f"Unsupported return_domain: {return_domain}")

        # Store results
        pdf_surface[i] = pdf
        cdf_surface[i] = cdf
        x_surface[i] = x
        all_moments[i] = moments

    # Create DataFrame with moments
    moments = pd.DataFrame(all_moments).T

    logger.info(f"Historical density calculation complete using {method} method")

    return {
        'pdf_surface': pdf_surface,
        'cdf_surface': cdf_surface,
        'x_surface': x_surface,
        'moments': moments
    }
