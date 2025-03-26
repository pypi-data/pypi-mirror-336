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
def get_hd_surface(model_results: pd.DataFrame,
                   df_hist: pd.DataFrame,
                   domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                   return_domain: str = 'log_moneyness') -> Tuple[
    Dict[str, np.ndarray], Dict[str, np.ndarray], Dict[str, np.ndarray], pd.DataFrame]:

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
        VolyError("Cannot determine granularity from df_hist.")
        return

    pdf_surface = {}
    cdf_surface = {}
    x_surface = {}
    all_moments = {}

    # Process each maturity
    for i in model_results.index:
        # Get parameters for this maturity
        s = model_results.loc[i, 's']
        r = model_results.loc[i, 'r']
        t = model_results.loc[i, 't']

        LM = get_domain(domain_params, s, r, None, t, 'log_moneyness')
        M = get_domain(domain_params, s, r, None, t, 'moneyness')
        R = get_domain(domain_params, s, r, None, t, 'returns')
        K = get_domain(domain_params, s, r, None, t, 'log_moneyness')

        # Filter historical data for this maturity's lookback period
        start_date = dt.datetime.now() - dt.timedelta(days=int(t * 365.25))
        maturity_hist = df_hist[df_hist.index >= start_date].copy()

        if len(maturity_hist) < 2:
            logger.warning(f"Not enough historical data for maturity {i}, skipping.")
            continue

        # Calculate the number of periods that match the time to expiry
        n_periods = int(t * 365.25 * 24 * 60 / minutes_per_period)

        # Compute returns and weights
        maturity_hist['returns'] = np.log(maturity_hist['close'] / maturity_hist['close'].shift(1)) * np.sqrt(n_periods)
        maturity_hist = maturity_hist.dropna()

        returns = maturity_hist['returns'].values

        if len(returns) < 10:
            logger.warning(f"Not enough valid returns for maturity {i}, skipping.")
            continue

        mu_scaled = returns.mean()
        sigma_scaled = returns.std()

        # Correct Girsanov adjustment to match the risk-neutral mean
        expected_risk_neutral_mean = (r - 0.5 * sigma_scaled ** 2) * np.sqrt(t)
        adjustment = mu_scaled - expected_risk_neutral_mean
        adj_returns = returns - adjustment  # Shift the mean to risk-neutral

        # Create HD and Normalize
        f = stats.gaussian_kde(adj_returns, bw_method='silverman')
        hd_lm = f(LM)
        hd_lm = np.maximum(hd_lm, 0)
        total_area = np.trapz(hd_lm, LM)
        if total_area > 0:
            pdf_lm = hd_lm / total_area
        else:
            logger.warning(f"Total area is zero for maturity {i}, skipping.")
            continue

        pdf_k = pdf_lm / K
        pdf_m = pdf_k * s
        pdf_r = pdf_lm / (1 + R)

        cdf = np.concatenate(([0], np.cumsum(pdf_lm[:-1] * np.diff(LM))))

        if return_domain == 'log_moneyness':
            x = LM
            pdf = pdf_lm
            moments = get_all_moments(x, pdf)
        elif return_domain == 'moneyness':
            x = M
            pdf = pdf_m
            moments = get_all_moments(x, pdf)
        elif return_domain == 'returns':
            x = R
            pdf = pdf_r
            moments = get_all_moments(x, pdf)
        elif return_domain == 'strikes':
            x = K
            pdf = pdf_k
            moments = get_all_moments(x, pdf)

        # Store results
        pdf_surface[i] = pdf
        cdf_surface[i] = cdf
        x_surface[i] = x
        all_moments[i] = moments

    # Create a DataFrame with moments using the same index as model_results
    moments = pd.DataFrame(all_moments).T

    return {
        'pdf_surface': pdf_surface,
        'cdf_surface': cdf_surface,
        'x_surface': x_surface,
        'moments': moments
    }


class GARCHModel:
    """
    GARCH(1,1) model for volatility modeling and simulation.

    Fits a GARCH(1,1) model to historical returns and simulates future paths
    for historical density estimation.
    """

    def __init__(self,
                 data: np.ndarray,
                 data_name: str,
                 n_fits: int = 400,
                 window_length: int = 365,
                 z_h: float = 0.1):
        """
        Initialize the GARCH model.

        Args:
            data: Array of log returns
            data_name: Identifier for the dataset
            n_fits: Number of sliding windows to use for parameter estimation
            window_length: Length of each sliding window
            z_h: Bandwidth factor for kernel density estimation of innovations
        """
        self.data = data
        self.data_name = data_name
        self.n_fits = n_fits
        self.window_length = window_length
        self.z_h = z_h

        # Parameters to be created during fitting and simulation
        self.parameters = None
        self.e_process = None
        self.z_process = None
        self.sigma2_process = None
        self.z_dens = None
        self.simulated_log_returns = None
        self.simulated_tau_mu = None

    def fit(self):
        """
        Fit GARCH(1,1) model to historical data using sliding windows.

        For each window, estimates parameters (ω, α, β) and extracts innovations.
        """

        if len(self.data) < self.window_length + self.n_fits:
            raise VolyError(
                f"Not enough data points. Need at least {self.window_length + self.n_fits}, got {len(self.data)}")

        start = self.window_length + self.n_fits
        end = self.n_fits

        parameters = np.zeros((self.n_fits, 4))
        z_process = []
        e_process = []
        sigma2_process = []

        logger.info(f"Fitting GARCH model with {self.n_fits} windows...")

        for i in range(self.n_fits):
            window = self.data[end - i - 1:start - i - 1]
            data = window - np.mean(window)

            model = arch_model(data, vol='GARCH', p=1, q=1)
            GARCH_fit = model.fit(disp='off')

            mu, omega, alpha, beta = [
                GARCH_fit.params["mu"],
                GARCH_fit.params["omega"],
                GARCH_fit.params["alpha[1]"],
                GARCH_fit.params["beta[1]"],
            ]
            parameters[i, :] = [mu, omega, alpha, beta]

            if i == 0:
                sigma2_tm1 = omega / (1 - alpha - beta)
            else:
                sigma2_tm1 = sigma2_process[-1]

            e_t = data.tolist()[-1]  # last observed log-return
            e_tm1 = data.tolist()[-2]  # previous observed log-return
            sigma2_t = omega + alpha * e_tm1 ** 2 + beta * sigma2_tm1
            z_t = e_t / np.sqrt(sigma2_t)

            e_process.append(e_t)
            z_process.append(z_t)
            sigma2_process.append(sigma2_t)

        self.parameters = parameters
        self.e_process = e_process
        self.z_process = z_process
        self.sigma2_process = sigma2_process

        # Kernel density estimation for innovations
        z_dens_x = np.linspace(min(self.z_process), max(self.z_process), 500)
        h_dyn = self.z_h * (np.max(z_process) - np.min(z_process))

        # Use scipy's gaussian_kde for innovation distribution
        kde = stats.gaussian_kde(np.array(z_process), bw_method=h_dyn)
        z_dens_y = kde(z_dens_x)

        self.z_dens = {"x": z_dens_x, "y": z_dens_y}

        logger.info("GARCH model fitting complete")

    def _GARCH_simulate(self, pars, horizon):
        """
        Simulate a single GARCH path to specified horizon.

        Args:
            pars: Tuple of (mu, omega, alpha, beta)
            horizon: Number of steps to simulate

        Returns:
            Tuple of (sigma2_process, e_process) of simulated values
        """
        mu, omega, alpha, beta = pars
        burnin = horizon * 2
        sigma2 = [omega / (1 - alpha - beta)]
        e = [self.data.tolist()[-1] - mu]  # last observed log-return mean adjusted

        # Convert density to probability weights
        weights = self.z_dens["y"] / np.sum(self.z_dens["y"])

        for _ in range(horizon + burnin):
            sigma2_tp1 = omega + alpha * e[-1] ** 2 + beta * sigma2[-1]
            # Sample from the estimated innovation distribution
            z_tp1 = np.random.choice(self.z_dens["x"], 1, p=weights)[0]
            e_tp1 = z_tp1 * np.sqrt(sigma2_tp1)
            sigma2.append(sigma2_tp1)
            e.append(e_tp1)

        return sigma2[-horizon:], e[-horizon:]

    def _variate_pars(self, pars, bounds):
        """
        Add variation to GARCH parameters for simulation uncertainty.

        Args:
            pars: Array of mean parameters [mu, omega, alpha, beta]
            bounds: Standard deviation bounds for parameters

        Returns:
            Array of slightly varied parameters
        """
        new_pars = []
        for i, (par, bound) in enumerate(zip(pars, bounds)):
            var = bound ** 2 / self.n_fits
            new_par = np.random.normal(par, var, 1)[0]
            if (new_par <= 0) and (i >= 1):
                new_par = 0.01
            new_pars.append(new_par)
        return new_pars

    def simulate_paths(self, horizon, simulations=5000, variate_parameters=True):
        """
        Simulate multiple GARCH paths using Monte Carlo.

        Args:
            horizon: Number of steps to simulate (days)
            simulations: Number of Monte Carlo simulations
            variate_parameters: Whether to add variation to GARCH parameters

        Returns:
            Tuple of (simulated_log_returns, simulated_tau_mu)
        """
        if self.parameters is None:
            self.fit()

        pars = np.mean(self.parameters, axis=0).tolist()  # [mu, omega, alpha, beta]
        bounds = np.std(self.parameters, axis=0).tolist()

        logger.info(f"Simulating {simulations} GARCH paths for {horizon} steps...")
        logger.info(f"GARCH parameters: mu={pars[0]:.6f}, omega={pars[1]:.6f}, alpha={pars[2]:.6f}, beta={pars[3]:.6f}")

        np.random.seed(42)  # For reproducibility

        new_pars = pars.copy()  # start with unchanged parameters
        simulated_log_returns = np.zeros(simulations)
        simulated_tau_mu = np.zeros(simulations)

        for i in range(simulations):
            if ((i + 1) % (simulations // 10) == 0):
                logger.info(f"Simulation progress: {i + 1}/{simulations}")

            if ((i + 1) % (simulations // 20) == 0) and variate_parameters:
                new_pars = self._variate_pars(pars, bounds)

            sigma2, e = self._GARCH_simulate(new_pars, horizon)
            simulated_log_returns[i] = np.sum(e)  # Sum log returns over horizon
            simulated_tau_mu[i] = horizon * pars[0]  # Total drift

        self.simulated_log_returns = simulated_log_returns
        self.simulated_tau_mu = simulated_tau_mu

        return simulated_log_returns, simulated_tau_mu


@catch_exception
def get_garch_hd_surface(model_results: pd.DataFrame,
                         df_hist: pd.DataFrame,
                         domain_params: Tuple[float, float, int] = (-1.5, 1.5, 1000),
                         return_domain: str = 'log_moneyness',
                         n_fits: int = 400,
                         simulations: int = 5000,
                         window_length: int = 365,
                         variate_parameters: bool = True,
                         bandwidth: float = 0.15) -> Dict[str, Any]:
    """
    Generate historical density surface using GARCH(1,1) model and Monte Carlo simulation.

    Parameters:
        model_results: DataFrame with model parameters and maturities
        df_hist: DataFrame with historical price data (must have 'close' column)
        domain_params: Tuple of (min, max, num_points) for x-domain
        return_domain: Domain for x-axis values ('log_moneyness', 'moneyness', 'returns', 'strikes')
        n_fits: Number of sliding windows for GARCH parameter estimation
        simulations: Number of Monte Carlo simulations
        window_length: Length of each sliding window for GARCH estimation
        variate_parameters: Whether to vary GARCH parameters between simulations
        bandwidth: Bandwidth for kernel density estimation of final density

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

    # Calculate log returns based on the determined granularity
    log_returns = np.log(df_hist['close'] / df_hist['close'].shift(1)) * 100
    log_returns = log_returns.dropna().values

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

        # Fix for very short-term maturities - use floating-point days
        tau_days_float = t * 365.25  # Exact number of days (as float)
        tau_day = max(1, int(tau_days_float))  # Ensure minimum of 1 day for simulation

        logger.info(f"Processing GARCH HD for maturity {i} (t={t:.4f} years, {tau_days_float:.2f} days)")

        # Calculate the number of periods that match the time to expiry
        n_periods = max(1, int(t * 365.25 * 24 * 60 / minutes_per_period))

        # Initialize GARCH model
        garch_model = GARCHModel(
            data=log_returns,
            data_name=str(i),
            n_fits=min(n_fits, len(log_returns) // 3),
            window_length=min(window_length, len(log_returns) // 3),
            z_h=0.1
        )

        # Simulate paths
        simulated_log_returns, simulated_tau_mu = garch_model.simulate_paths(
            horizon=tau_day,
            simulations=simulations,
            variate_parameters=variate_parameters
        )

        # Scale the simulated returns to match target time horizon
        # Use floating-point days to avoid division by zero
        scaling_factor = np.sqrt(n_periods / tau_days_float)
        scaled_log_returns = simulated_log_returns * scaling_factor

        # Risk-neutral adjustment (Girsanov transformation)
        # Calculate empirical mean and volatility of the scaled returns
        mu_scaled = scaled_log_returns.mean()
        sigma_scaled = scaled_log_returns.std()

        # Expected risk-neutral drift
        expected_risk_neutral_mean = (r - 0.5 * (sigma_scaled / 100) ** 2) * 100 * np.sqrt(t)

        # Calculate adjustment to shift physical to risk-neutral measure
        adjustment = mu_scaled - expected_risk_neutral_mean

        # Adjust the returns to the risk-neutral measure
        risk_neutral_log_returns = scaled_log_returns - adjustment

        # Convert to terminal prices using the risk-neutral returns
        simulated_prices = s * np.exp(risk_neutral_log_returns / 100)

        # Convert to moneyness domain
        simulated_moneyness = s / simulated_prices

        # Get x domain grid based on requested return_domain
        LM = np.linspace(domain_params[0], domain_params[1], domain_params[2])
        M = np.exp(LM)  # Moneyness
        R = M - 1  # Returns
        K = s / M  # Strike prices

        # Perform kernel density estimation in moneyness domain
        kde = stats.gaussian_kde(simulated_moneyness, bw_method=bandwidth)
        pdf_m = kde(M)

        # Ensure density integrates to 1
        dx = LM[1] - LM[0]
        total_area = np.sum(pdf_m * dx)
        pdf_m = pdf_m / total_area

        # Transform to other domains as needed
        pdf_lm = pdf_m * M  # Transform to log-moneyness domain
        pdf_k = pdf_lm / K  # Transform to strike domain
        pdf_r = pdf_lm / (1 + R)  # Transform to returns domain

        # Calculate CDF
        cdf = np.cumsum(pdf_lm) * dx
        cdf = np.minimum(cdf / cdf[-1], 1.0)  # Normalize and cap at 1.0

        # Select appropriate domain for return
        if return_domain == 'log_moneyness':
            x = LM
            pdf = pdf_lm
            moments = get_all_moments(x, pdf)
        elif return_domain == 'moneyness':
            x = M
            pdf = pdf_m
            moments = get_all_moments(x, pdf)
        elif return_domain == 'returns':
            x = R
            pdf = pdf_r
            moments = get_all_moments(x, pdf)
        elif return_domain == 'strikes':
            x = K
            pdf = pdf_k
            moments = get_all_moments(x, pdf)
        else:
            raise VolyError(f"Unsupported return_domain: {return_domain}")

        # Store results
        pdf_surface[i] = pdf
        cdf_surface[i] = cdf
        x_surface[i] = x
        all_moments[i] = moments

    # Create DataFrame with moments
    moments = pd.DataFrame(all_moments).T

    logger.info("GARCH historical density calculation complete")

    return {
        'pdf_surface': pdf_surface,
        'cdf_surface': cdf_surface,
        'x_surface': x_surface,
        'moments': moments
    }
