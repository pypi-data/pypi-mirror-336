import logging
import numpy as np
from copy import deepcopy

from .portfolios.minvariance import MinVariancePortfolio
from .utils import math

logger = logging.getLogger(__name__)


def _folio_backtest(closes, portfolio):
    tickers = closes.columns
    returns = closes.copy()
    returns = returns / returns.iloc[0]
    returns["Portfolio"] = returns @ portfolio.weights
    return returns


def portfolio_optimise(portfolio, model, asofdate, periodstart, periodend, rfr=0):
    """TODO:
    - handle rfr
    - functional-like so that no arg is expected to have change in value
    - for portfolio, introduce inplace option

    Args:
        portfolio (_type_): _description_
        model (_type_): _description_
        asofdate (_type_): _description_
        periodstart (_type_): _description_
        periodend (_type_): _description_
        rfr (int, optional): _description_. Defaults to 0.

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    pfl_optimised = deepcopy(portfolio)
    if pfl_optimised.timeseries is None:
        timeseries = None
        for ticker in pfl_optimised.tickers:
            # TODO: retire yfanance
            ts = None
            # ts = access.via.yahoo.get_daily_ts_for_ticker(
            #     ticker, periodstart, periodend
            # )[["trading_date", "adj_close"]]
            if timeseries is None:
                timeseries = ts
            else:
                timeseries = timeseries.merge(ts, on="trading_date", how="inner")
        timeseries.set_index("trading_date", inplace=True)
        timeseries.columns = pfl_optimised.tickers
        pfl_optimised.timeseries = timeseries

    if pfl_optimised.weights is None:
        ticker_count = len(pfl_optimised.tickers)
        pfl_optimised.weights = [1.0 / ticker_count] * ticker_count

    # portfolio re-weighting
    hist_daily_rets = pfl_optimised.timeseries[
        pfl_optimised.timeseries.index < asofdate
    ].copy()
    hist_daily_rets = np.log(hist_daily_rets / hist_daily_rets.shift(1)).dropna()
    pfl_model = None
    if model == "MinVariance":
        pfl_model = MinVariancePortfolio(math.get_cov(hist_daily_rets))
    else:
        raise Exception(f"Defined portfolio model [{model}] not recognised")
    pfl_optimised.weights = pfl_model.get_weights()

    return pfl_optimised
