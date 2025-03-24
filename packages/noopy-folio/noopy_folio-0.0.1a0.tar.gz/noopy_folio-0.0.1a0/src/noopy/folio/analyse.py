"""
The module provides users with high-level usage of the library and it's
implemented to :
- conduct standard anlaysis from asset recommendations, portfolio buildup
  to performance analysis;
- with options to specify:
    - pool of assets
    - "historical" period as well as "future period"
    - market data and hence portfolio update frequency
"""

from .dataaccessor import marketdata
from .portfolios.blacklitterman import BlackLittermanPortfolio
from .portfolios.longonly import LongOnlyPortfolio
from .portfolios.minvariance import MinVariancePortfolio
from .portfolios.riskbudgeting import RiskBudgetingPortfolio
from .utils import math
from .reporting import reports
from . import portfolios

import numpy as np
import pandas as pd
import datetime as dt


def asset_recommendations(today, lookbackdays, frequency, assetrank, symbols=None):
    """Asset recommendations:
    Extract out assets as recommendation from a large asset pool.
    This is mainly based on correlations.

    Args:
        today (str): assumed T0 date in string with format 'yyyy-mm-dd'
        lookbackdays (int): calendar days to date back from today
        frequency (str): available ones - 1D, 1W, 1M, 3M and 1Y
        assetrank (int): number of tops from correlation pairs
        symbols (array-like, optional): a list of valid symbols. Defaults to None.

    Returns:
        pd.DataFrame: recommended assets with related attributes.
    """

    # Get all assets candidates when None
    asset_info = marketdata.get_asset_info()
    if symbols is None:
        symbols = list(asset_info.Symbol)

    hist_end = dt.datetime.strptime(today, "%Y-%m-%d")
    hist_start = hist_end - dt.timedelta(days=lookbackdays)

    # covariance of equilibrium excess returns
    rfr = marketdata.get_md_rfr(hist_start, hist_end, frequency=frequency)
    asset_close = marketdata.get_md_observable(
        symbols, "Adj Close", hist_start, hist_end, frequency=frequency
    )

    # Remove assets that contain too few historical data
    asset_close_count = asset_close.count()
    close_row_count = asset_close.shape[0]
    for index, value in asset_close_count.items():
        if value < close_row_count:
            asset_close.drop(columns=index, inplace=True)

    asset_returns = np.log(asset_close / asset_close.shift(1)).dropna()
    asset_returns_and_rfr = asset_returns.join(rfr).fillna(method="backfill")
    excess_returns = asset_returns_and_rfr.subtract(
        asset_returns_and_rfr["RFR"], axis="index"
    ).iloc[:, :-1]

    correlations = excess_returns.corr()
    smalls, zeros, bigs = math.correlation_rankings(correlations, assetrank)
    recommended_assets = set(np.array([i[0] for i in zeros]).flatten())
    print(f"{len(recommended_assets)} assets are recommended:")
    print(recommended_assets)

    excess_returns = excess_returns[recommended_assets]
    correlations = excess_returns.corr()

    recommended_assets = asset_info[asset_info.Symbol.isin(recommended_assets)]
    reports.create_asset_recommendation_report(
        correlations, assetrank, recommended_assets
    )
    return recommended_assets


def asset_selections(symbols, today, lookbackdays, frequency):
    """Asset selections:
    Conduct some deep analysis of selected assets, which should be normally from
    preliminary recommendation exercise.

    Args:
        symbols (array-like): a list of valid symbols
        today (str): assumed T0 date in string with format 'yyyy-mm-dd'
        lookbackdays (int): calendar days to date back from today
        frequency (str): available ones - 1D, 1W, 1M, 3M and 1Y

    Returns:
        pd.DataFrame: covariance related stats among selected assets.
    """

    hist_end = dt.datetime.strptime(today, "%Y-%m-%d")
    hist_start = hist_end - dt.timedelta(days=lookbackdays)

    # covariance of equilibrium excess returns
    rfr = marketdata.get_md_rfr(hist_start, hist_end, frequency=frequency)
    asset_close = marketdata.get_md_observable(
        symbols, "Adj Close", hist_start, hist_end, frequency=frequency
    )

    # Remove assets that contain too few historical data
    asset_close_count = asset_close.count()
    close_row_count = asset_close.shape[0]
    for index, value in asset_close_count.items():
        if value < close_row_count:
            asset_close.drop(columns=index, inplace=True)

    asset_returns = np.log(asset_close / asset_close.shift(1)).dropna()
    asset_returns_and_rfr = asset_returns.join(rfr).fillna(method="backfill")
    excess_returns = asset_returns_and_rfr.subtract(
        asset_returns_and_rfr["RFR"], axis="index"
    ).iloc[:, :-1]

    naive_name = "Naive"
    naive_cov = math.get_cov(excess_returns, robust=False)
    naive_cov_eigs = sorted(np.linalg.eig(naive_cov)[0], reverse=True)
    naive_cov_det = np.linalg.det(naive_cov)
    naive_cov_inv = np.linalg.inv(naive_cov)
    naive_cov_inv_det = np.linalg.det(naive_cov_inv)
    naive_series = pd.Series(
        {
            "Eigen Values": naive_cov_eigs,
            "$\lambda_{max}/\lambda_{min}$": abs(
                naive_cov_eigs[-1] / naive_cov_eigs[0]
            ),
            "Determinant": naive_cov_det,
            "Inv Determinant": naive_cov_inv_det,
        },
        name=naive_name,
    )

    robust_name = "Robust"
    robust_cov = math.get_cov(excess_returns, robust=True)
    robust_cov_eigs = sorted(np.linalg.eig(robust_cov)[0], reverse=True)
    robust_cov_det = np.linalg.det(robust_cov)
    robust_cov_inv = np.linalg.inv(robust_cov)
    robust_cov_inv_det = np.linalg.det(robust_cov_inv)
    robust_series = pd.Series(
        {
            "Eigen Values": robust_cov_eigs,
            "$\lambda_{max}/\lambda_{min}$": abs(
                robust_cov_eigs[-1] / robust_cov_eigs[0]
            ),
            "Determinant": robust_cov_det,
            "Inv Determinant": robust_cov_inv_det,
        },
        name=robust_name,
    )

    cov_stats = pd.DataFrame([naive_series, robust_series]).T
    reports.create_asset_selection_report(cov_stats, excess_returns.corr())

    cov_stats = cov_stats.append(
        pd.Series({"Naive": naive_cov, "Robust": robust_cov}, name="Cov. Matrix")
    )
    return cov_stats


def naive_robust_cov_difference(
    symbols,
    equilweights,
    today,
    lookbackdays,
    lookaheaddays,
    views,
    frequency,
    riskaversion,
):
    """Naive vs robust covariance estimates:
    Check difference between using naive and robust convariance methods.

    Args:
        symbols (array-like): a list of valid symbols
        equilweights (array-like): weighting vector for equilibrium portfolio
        today (str): assumed T0 date in string with format 'yyyy-mm-dd'
        lookbackdays (int): calendar days to date back from today
        lookaheaddays (int): calendar days to date forward from today
        views (pd.DataFrame): including info on P and Q, e.g:
            pd.DataFrame({'view1': [1, 0, 0.01], 'view2': [0, 1, -0.05]}, index=['s1', 's2', 'Q'])
        frequency (str): available ones - 1D, 1W, 1M, 3M and 1Y
        riskaversion (float): risk aversion to define investor's appetite

    Returns:
        None: N/A
    """

    comparison = _PortfolioComparison(
        symbols, equilweights, today, lookbackdays, lookaheaddays, frequency
    )

    P = views.values[:-1].T
    Q = views.values[-1].reshape(-1, 1)
    excess_returns = comparison.ins_excess_returns_
    equil_weights = comparison.equil_weights_

    def get_pfl_weights(robust):
        equil_cov = math.get_cov(excess_returns, robust)
        pfl = BlackLittermanPortfolio(
            equil_cov,
            equil_weights.values.reshape(-1, 1),
            P,
            Q,
            riskaversion=riskaversion,
        )
        if riskaversion is None:
            print(
                f"Implied risk aversion (robust?->{robust}): ", pfl.get_risk_aversion()
            )
        return pfl.get_weights(version="v1")

    pfl_name = "BL with Naive Covariances"
    pfl_weights = get_pfl_weights(False)
    pfl_weights = pd.Series(
        pfl_weights.reshape(-1),
        index=equil_weights.index,
        name="BL with Naive Covariances",
    )
    comparison.append_pfl(pfl_weights)

    pfl_name = "BL with Robust Covariances"
    pfl_weights = get_pfl_weights(True)
    pfl_weights = pd.Series(
        pfl_weights.reshape(-1),
        index=equil_weights.index,
        name="BL with Robust Covariances",
    )
    comparison.append_pfl(pfl_weights)

    comparison.create_report()


def blacklitterman_riskaversion(
    symbols,
    equilweights,
    today,
    lookbackdays,
    lookaheaddays,
    views,
    frequency,
    riskaversions,
):
    """Analyse impacts from risk aversions:

    Args:
        symbols (array-like): a list of valid symbols
        equilweights (array-like): weighting vector for equilibrium portfolio
        today (str): assumed T0 date in string with format 'yyyy-mm-dd'
        lookbackdays (int): calendar days to date back from today
        lookaheaddays (int): calendar days to date forward from today
        views (pd.DataFrame): including info on P and Q, e.g:
            pd.DataFrame({'view1': [1, 0, 0.01], 'view2': [0, 1, -0.05]}, index=['s1', 's2', 'Q'])
        frequency (str): available ones - 1D, 1W, 1M, 3M and 1Y
        riskaversion (float): risk aversion to define investor's appetite

    Returns:
        None: N/A
    """

    comparison = _PortfolioComparison(
        symbols, equilweights, today, lookbackdays, lookaheaddays, frequency
    )

    P = views.values[:-1].T
    Q = views.values[-1].reshape(-1, 1)
    excess_returns = comparison.ins_excess_returns_
    equil_weights = comparison.equil_weights_

    equil_cov = math.get_cov(excess_returns)

    for ra in riskaversions:
        pfl = BlackLittermanPortfolio(
            equil_cov, equil_weights.values.reshape(-1, 1), P, Q, ra
        )
        pfl_name = rf"BL Portfolio $\lambda$={ra}"
        pfl_weights = pfl.get_weights(version="v1")
        pfl_weights = pd.Series(pfl_weights.reshape(-1), index=symbols, name=pfl_name)
        comparison.append_pfl(pfl_weights)

    comparison.create_report()


def blacklitterman_with_constraints(
    symbols,
    equilweights,
    today,
    lookbackdays,
    lookaheaddays,
    views,
    frequency,
    riskaversion,
):
    """Analyse impacts from different constraints:

    Args:
        symbols (array-like): a list of valid symbols
        equilweights (array-like): weighting vector for equilibrium portfolio
        today (str): assumed T0 date in string with format 'yyyy-mm-dd'
        lookbackdays (int): calendar days to date back from today
        lookaheaddays (int): calendar days to date forward from today
        views (pd.DataFrame): including info on P and Q, e.g:
            pd.DataFrame({'view1': [1, 0, 0.01], 'view2': [0, 1, -0.05]}, index=['s1', 's2', 'Q'])
        frequency (str): available ones - 1D, 1W, 1M, 3M and 1Y
        riskaversion (float): risk aversion to define investor's appetite

    Returns:
        None: N/A
    """

    comparison = _PortfolioComparison(
        symbols, equilweights, today, lookbackdays, lookaheaddays, frequency
    )

    P = views.values[:-1].T
    Q = views.values[-1].reshape(-1, 1)
    excess_returns = comparison.ins_excess_returns_
    equil_weights = comparison.equil_weights_

    equil_cov = math.get_cov(excess_returns)
    pfl = BlackLittermanPortfolio(
        equil_cov, equil_weights.values.reshape(-1, 1), P, Q, riskaversion=riskaversion
    )

    pfl_name = "BL Portfolio: Unconstrained"
    pfl_weights = pfl.get_weights(version="v1")
    pfl_weights = pd.Series(pfl_weights.reshape(-1), index=symbols, name=pfl_name)
    comparison.append_pfl(pfl_weights)

    pfl_name = "BL Portfolio: Equal Weights"
    pfl_weights = [1.0 / len(symbols)] * len(symbols)
    pfl_weights = pd.Series(pfl_weights, index=symbols, name=pfl_name)
    comparison.append_pfl(pfl_weights)

    pfl_name = "BL Portfolio: Min Variance"
    pfl_weights = MinVariancePortfolio(pfl.get_covariances()).get_weights()
    pfl_weights = pd.Series(pfl_weights.reshape(-1), index=symbols, name=pfl_name)
    comparison.append_pfl(pfl_weights)

    budget = 1.5  # can borrow 50% of balance at maximum

    pfl_name = "BL Portfolio: Long Only"
    pfl_weights = LongOnlyPortfolio(
        pfl.get_covariances(), pfl.get_returns(), budget
    ).get_weights()
    pfl_weights = pd.Series(pfl_weights.reshape(-1), index=symbols, name=pfl_name)
    comparison.append_pfl(pfl_weights)

    pfl_name = "BL Portfolio: ERC"
    symbol_count = len(symbols)
    risk_budgets = np.array([1.0 / symbol_count] * symbol_count).reshape(-1, 1)
    pfl_weights = RiskBudgetingPortfolio(
        pfl.get_covariances(), pfl.get_returns(), budget, riskbudgets=risk_budgets
    ).get_weights()
    pfl_weights = pd.Series(pfl_weights.reshape(-1), index=symbols, name=pfl_name)
    comparison.append_pfl(pfl_weights)

    comparison.create_report()


class _PortfolioComparison(object):
    """Class for store and comapring a number of portfolios:

    Args:
        object ([type]): N/A
    """

    def __init__(
        self, symbols, equilweights, today, lookbackdays, lookaheaddays, frequency
    ):
        """Constructor to initialise equilibrium portfolio plus:
        - excess returns
        - market returns for internal usage

        Args:
            symbols (array-like): a list of valid symbols
            equilweights (array-like): weighting vector for equilibrium portfolio
            today (str): assumed T0 date in string with format 'yyyy-mm-dd'
            lookbackdays (int): calendar days to date back from today
            lookaheaddays (int): calendar days to date forward from today
            frequency (str): available ones - 1D, 1W, 1M, 3M and 1Y
        """

        today = dt.datetime.strptime(today, "%Y-%m-%d")
        hist_date = today - dt.timedelta(days=lookbackdays)
        future_date = today + dt.timedelta(days=lookaheaddays)
        rfr = marketdata.get_md_rfr(hist_date, future_date, frequency=frequency)
        asset_close = marketdata.get_md_observable(symbols, frequency=frequency)
        asset_close = asset_close[
            (asset_close.index >= hist_date) & (asset_close.index <= future_date)
        ]
        asset_returns = np.log(asset_close / asset_close.shift(1)).dropna()
        asset_returns_and_rfr = asset_returns.join(rfr).fillna(method="backfill")
        excess_returns = asset_returns_and_rfr.subtract(
            asset_returns_and_rfr["RFR"], axis="index"
        ).iloc[:, :-1]
        ins_excess_returns = excess_returns[excess_returns.index <= today]

        equil_name = "Equilibrium Portfolio"
        equil_weights = pd.Series(equilweights.ravel(), symbols, name=equil_name)
        equil_weights = equil_weights / equil_weights.sum()
        equil_returns = (
            asset_returns_and_rfr @ portfolios.balance_weights_with_cash(equil_weights)
        ).iloc[:, 0]
        equil_returns.name = equil_name

        self._today = today
        self._asset_returns_and_rfr = asset_returns_and_rfr
        self._weights = equil_weights.to_frame()
        self._returns = equil_returns.to_frame()
        self._equil_name = equil_name

        self.ins_excess_returns_ = ins_excess_returns
        self.equil_weights_ = equil_weights
        self.equil_returns_ = equil_returns

    def append_pfl(self, pflweights):
        """Append a portfolio represented by allocation

        Args:
            pflweights (array-like): weighting vector for appended portfolio

        Returns:
            _PortfolioComparison: the same instance
        """

        pfl_returns = (
            self._asset_returns_and_rfr
            @ portfolios.balance_weights_with_cash(pflweights)
        ).iloc[:, 0]
        pfl_returns.name = pflweights.name
        self._weights = self._weights.join(pflweights)
        self._returns = self._returns.join(pfl_returns)
        return self

    def create_report(self):
        """Create report"""

        return reports.create_overall_report(
            self._returns,
            today=self._today,
            benchmarkreturns=self._returns[self._equil_name],
            weights=self._weights,
            benchmarkweights=self._weights[self._equil_name],
        )
