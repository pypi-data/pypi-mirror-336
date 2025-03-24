from ..utils import show

import numpy as np
import pandas as pd


def create_overall_report(
    returns, today, benchmarkreturns=None, weights=None, benchmarkweights=None
):
    """create a generic report:

    Args:
        returns (pd.DataFrame): rows represent time series; columns are for scoped portfolios
        today ('str'): assumed T0 date in string with format 'yyyy-mm-dd'
        benchmarkreturns (pd.Series): return ts for benchmark portfolio
        weights (pd.DataFrame, optional): rows are weights and columns are portfolios. Defaults to None.
        benchmarkweights (pd.Series, optional): weightings for benchmark portfolio. Defaults to None.
    """
    print("=" * 128)
    print("-" * 44, "Portfolio Construction: Overall Report", "-" * 44)
    print("_" * 128)

    look_ahead_rets = returns[returns.index > today]
    show.performance_stats(look_ahead_rets)
    if weights is not None:
        show.asset_allocations(weights, benchmarkweights)
    show.returns_aggs(look_ahead_rets)
    show.rolling_characteristics(look_ahead_rets)
    show.profit_and_loss(returns, today, benchmarkreturns)

    print("_" * 128)


def create_asset_recommendation_report(correlations, assetrank, recommendedassets):
    """create asset recommendation report:

    Args:
        correlations (pd.DataFrame): correlation matrix
        assetrank (int): Number of tops that we would like to extract out
        recommendedassets (pd.DataFrame): assets with basic information on each
    """
    print("=" * 128)
    print("-" * 37, "Portfolio Construction: Asset Recommendation Report", "-" * 38)
    print("_" * 128)

    show.correlations(correlations, assetrank)
    recommendedassets.sort_values(by="Market Cap", ascending=False).plot(
        kind="bar", x="Symbol", y="Market Cap", figsize=(14, 6), logy=True
    )
    show.print_as_table(
        recommendedassets[["Symbol", "Name", "Country", "Market Cap", "Industry"]]
    )

    print("_" * 128)


def create_asset_selection_report(covstats, correlations):
    """Create report on selected assets:

    Args:
        covstats (pd.DataFrame): some basic statistics around covariances
        correlations (pd.DataFrame): covariance matrix
    """
    print("=" * 128)
    print("-" * 40, "Portfolio Construction: Selected Asset Report", "-" * 41)
    print("_" * 128)

    show.correlations(correlations, np.inf)
    # TODO: eigen values
    show.print_as_table(covstats)

    naive_eigs = covstats[covstats.index == "Eigen Values"]["Naive"][0]
    robust_eigs = covstats[covstats.index == "Eigen Values"]["Robust"][0]
    pd.DataFrame({"Naive": naive_eigs, "Robust": robust_eigs}).plot(figsize=(14, 6))

    print("_" * 128)
