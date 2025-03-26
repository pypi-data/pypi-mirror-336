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


def generate_lm_points(min_lm, max_lm):
    if min_lm >= max_lm:
        raise ValueError("min_lm must be less than max_lm")

    max_transformed = np.sqrt(max_lm) if max_lm > 0 else 0
    min_transformed = -np.sqrt(-min_lm) if min_lm < 0 else 0

    transformed_points = np.arange(min_transformed, max_transformed + 0.05, 0.05)
    lm_points = np.sign(transformed_points) * transformed_points ** 2

    lm_points = np.unique(np.round(lm_points, decimals=2))
    lm_points = sorted(lm_points)

    return lm_points


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

        if len(maturity_hist) < 10:
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

    return pdf_surface, cdf_surface, x_surface, moments
