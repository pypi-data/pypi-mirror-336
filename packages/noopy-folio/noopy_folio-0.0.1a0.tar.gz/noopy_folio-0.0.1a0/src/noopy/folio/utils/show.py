import seaborn as sns
import pandas as pd
from tabulate import tabulate
import numpy as np
from scipy.stats import norm
from . import math

import matplotlib.pyplot as plt

plt.style.use("fivethirtyeight")


def performance_stats(returns, riskfreerate=0):
    """Plot performance statistics:
    Check some standard characteristics of included portfolios, each of which
    represented by a return time series.

    Args:
        returns (pd.DataFrame): rows represent time series; columns are for scoped portfolios
        riskfreerate (float, optional): a static risk free rate. Defaults to 0.

    Returns:
        pd.DataFrame: Basic stats included, where rows are chracteristics and columns are portfolios
    """
    mean = returns.mean()
    volatility = returns.std()
    sharpe_ratio = (mean - riskfreerate) / volatility
    cumsum = returns.cumsum().apply(np.exp)
    minmum = returns.min()
    maximum = returns.max()
    cumsum_min = cumsum.min()
    cumsum_max = cumsum.max()
    max_drawdown = (cumsum_max - cumsum_min) / cumsum_max
    stats = {
        "Start Date": returns.index.min().strftime("%Y-%m-%d"),
        "End Date": returns.index.max().strftime("%Y-%m-%d"),
        "Count of Returns": returns.count(),
        "Count of NaN Returns": returns.isna().sum(),
        "Min of Returns": minmum.round(4),
        "Max of Returns": maximum.round(4),
        "Mean of Returns": mean.round(4),
        "Volatility of Returns": volatility.round(4),
        "Kurtosis of Returns": returns.kurtosis().round(4),
        "Skew of Returns": returns.skew().round(4),
        "Cumulative Returns": cumsum.max().round(4),
        "Sharpe Ratio": sharpe_ratio.round(4),
        "Max Drawdown": max_drawdown.round(4),
        "Value at Risk (95%)": returns.quantile(0.05).round(4),
    }
    stats = pd.DataFrame(stats).T
    print("Table: Portfolio Performance Statistics")
    print_as_table(stats)
    return stats


def asset_allocations(weights, benchmarkweights):
    """Plot asset allocation:
    Compare asset allocations among portfolios.

    Args:
        weights (pd.DataFrame): rows are weights and columns are portfolios
        benchmarkweights (pd.Series): weightings for benchmark portfolio
    """
    weights_with_bk = (
        weights
        if benchmarkweights.name in weights.columns
        else weights.join(benchmarkweights)
    )
    plt.figure()
    (weights_with_bk * 100).T.plot(kind="barh", stacked=True, figsize=(14, 6))
    plt.xlabel("Weights (%)"), plt.ylabel("Portfolios")
    plt.title("Comparison of Asset Allocation among Portfolios")
    plt.show()
    return


def returns_aggs(returns):
    """Plot some aggregated stats derived from returns, including:
    - return KDE
    - return candle box

    Args:
        returns (pd.DataFrame): rows represent time series; columns are for scoped portfolios
    """
    returns_ptg = returns * 100
    plt.figure()
    returns_ptg.plot(kind="kde", figsize=(14, 6), linewidth=0.8, alpha=0.7)
    plt.xlabel("Returns (%)"), plt.ylabel("Probability")
    plt.title("Return Distribution (KDE)")
    plt.show()

    plt.figure()
    returns_ptg.plot(kind="box", figsize=(14, 6))
    plt.xlabel("Portfolios"), plt.ylabel("Returns (%)")
    plt.title("Return Distribution (Box)")
    plt.show()


def rolling_characteristics(returns, riskfreerate=0):
    """Plot rollable characteristics derived from returns, including:
    - raw return ts
    - volatility ts
    - SR ts

    Args:
        returns (pd.DataFrame): rows represent time series; columns are for scoped portfolios
        riskfreerate (float, optional): a static risk free rate. Defaults to 0.
    """
    returns_ptg = returns * 100
    plt.figure()
    returns_ptg.plot(figsize=(14, 6), linewidth=0.8, alpha=0.7)
    plt.xlabel("Date"), plt.ylabel("Returns (%)")
    plt.title("Return Time Series")
    plt.show()

    plt.figure()
    returns_ptg.rolling(10).std().plot(figsize=(14, 6), linewidth=0.8, alpha=0.7)
    plt.xlabel("Date"), plt.ylabel("Volatility (%)")
    plt.title("Rolling Volatility (window=10)")

    plt.figure()
    sharpe_ratio = (
        returns_ptg.rolling(10).mean() - riskfreerate
    ) / returns_ptg.rolling(10).std()
    sharpe_ratio.plot(figsize=(14, 6), linewidth=0.8, alpha=0.7)
    plt.xlabel("Date"), plt.ylabel("Sharpe Ratio (%)")
    plt.title("Rolling Sharpe Ratio (window=10)")
    plt.show()


def profit_and_loss(returns, today, benchmarkreturns=None):
    """Plot P&L in time:
    - P&L
    - Drawdowns

    Args:
        returns (pd.DataFrame): rows represent time series; columns are for scoped portfolios
        today ('str'): assumed T0 date in string with format 'yyyy-mm-dd'
        benchmarkreturns (pd.Series): return ts for benchmark portfolio

    Raises:
        ValueError: expect at least 2 portfolios are included in returns at the moment.
    """
    returns_with_bk = (
        returns
        if benchmarkreturns.name in returns.columns
        else returns.join(benchmarkreturns)
    )
    returns_with_bk = returns_with_bk[returns_with_bk.index > today]
    nrows = returns_with_bk.shape[0]
    for i in range(nrows):
        if returns_with_bk.index[i] <= pd.to_datetime(today):
            returns_with_bk.iloc[i, :-1] = returns_with_bk.iloc[i, -1]

    pnl = returns_with_bk.cumsum().apply(np.exp) * 100.0
    pnl.iloc[0, :] = 100.0
    pnl.plot(linewidth=1, figsize=(14, 6))

    pfl_count = pnl.shape[1]
    row_count = int(np.ceil(pfl_count / 2.0))
    fig, axes = plt.subplots(row_count, 2, sharex=True, sharey=True)
    fig.tight_layout(h_pad=2)
    axes.reshape(row_count, 2)
    drawdown_table_data = pd.DataFrame()
    overall_worst_count = -np.inf
    if pfl_count == 1:
        raise ValueError(
            f"At 2 portfolios are expected the moment - (Only {pnl.columns[0]} is available.)"
        )
    if row_count == 1:
        for column_idx in range(2):
            s = pnl.iloc[:, column_idx]
            ax = axes[column_idx]
            ax.set_title(s.name)
            s.plot(ax=ax, linewidth=0.8, figsize=(14, 6))
            smin = s.min()
            smax = s.max()
            drawdowns = math.get_drawdowns(s)
            drawdown_keys = sorted(drawdowns, key=drawdowns.get, reverse=True)
            worst_count = min(len(drawdown_keys), 5)
            overall_worst_count = max(worst_count, overall_worst_count)
            drawdown_keys = drawdown_keys[:worst_count]
            for idx, key in zip(range(len(drawdown_keys)), drawdown_keys):
                xs = s.index[key[0]]
                xe = s.index[key[2]]
                ax.fill_between([xs, xe], smin, smax, alpha=0.3)
                drawdown_table_data[(s.name, idx)] = [
                    f"{drawdowns[key]:.2%}",
                    xs.strftime("%Y-%m-%d"),
                    s.index[key[1]].strftime("%Y-%m-%d"),
                    xe.strftime("%Y-%m-%d"),
                    (xe - xs).days,
                ]
    else:
        for row_idx in range(row_count):
            for column_idx in range(2):
                pnl_column_idx = row_idx * 2 + column_idx
                ax = axes[row_idx, column_idx]
                if pnl_column_idx >= pfl_count:
                    fig.delaxes(ax)
                    continue
                s = pnl.iloc[:, pnl_column_idx]
                ax.set_title(s.name)
                s.plot(ax=ax, linewidth=0.8, figsize=(14, 6))
                smin = s.min()
                smax = s.max()
                drawdowns = math.get_drawdowns(s)
                drawdown_keys = sorted(drawdowns, key=drawdowns.get, reverse=True)
                worst_count = min(len(drawdown_keys), 5)
                overall_worst_count = max(worst_count, overall_worst_count)
                drawdown_keys = drawdown_keys[:worst_count]
                for idx, key in zip(range(len(drawdown_keys)), drawdown_keys):
                    xs = s.index[key[0]]
                    xe = s.index[key[2]]
                    ax.fill_between([xs, xe], smin, smax, alpha=0.3)
                    drawdown_table_data[(s.name, idx)] = [
                        f"{drawdowns[key]:.2%}",
                        xs.strftime("%Y-%m-%d"),
                        s.index[key[1]].strftime("%Y-%m-%d"),
                        xe.strftime("%Y-%m-%d"),
                        (xe - xs).days,
                    ]
    fig.suptitle(f"{overall_worst_count} Worst Drawdowns")
    plt.show()
    drawdown_table_data = drawdown_table_data.T
    drawdown_table_data.columns = [
        "Net drawdown in %",
        "Peak Date",
        "Valley date",
        "Recovery date",
        "Duration (Days)",
    ]
    print(f"Table: {worst_count} Worst Drawdowns")
    print_as_table(drawdown_table_data)


def correlations(matrix, rankcount):
    """Plot correlation matrix as heatmap:

    Args:
        matrix (pd.DataFrame): both rows and columns are assets
        rankcount (int): number of tops from correlation pairs
    """
    smalls, zeros, bigs = math.correlation_rankings(matrix, rankcount)
    rank_data = pd.DataFrame(
        {
            f"Biggest {rankcount}": bigs,
            f"Smallest {rankcount}": smalls,
            f"{rankcount} closest to 0": zeros,
        }
    )
    print_as_table(rank_data)

    plt.figure(figsize=[14, 14])
    sns.heatmap(matrix.round(2), annot=True, cmap="autumn", fmt="g")
    plt.title("Correlation Matrix")
    plt.ylabel("Assets"), plt.xlabel("Assets")
    plt.show()


def print_as_table(data):
    """Plot tabulars from data:
    3 tables are plots under different format:
    - simple psql-like display (readable)
    - html format that can be interpreted by markdown
    - latex format for latex writings

    Args:
        data (pd.DataFrame): Any pd.DataFrame object.
    """
    print(tabulate(data, headers="keys", tablefmt="psql"))
    print(tabulate(data, headers="keys", tablefmt="html"))
    print(tabulate(data, headers="keys", tablefmt="latex"))


def verbose_print(verbose=True, *args, **kwargs):
    """Wrap original python print:
    This allows us to decide whether to actual action on print

    Args:
        verbose (bool, optional): should print if true. Defaults to True.
    """
    if not verbose:
        return
    print(*args, **kwargs)
