import numpy as np
from sklearn.covariance import LedoitWolf


def get_cov(data, robust=True, verbose=True):
    """Compute covariance matrix from samples:
    - naive: simply by the numpy.cov implementation
    - robust: Ledoit-Wolf method implemented in sklearn

    Args:
        data (matrix-like): sample data where a row a 1 sample, and columns represent variables
        robust (bool, optional): use robust method. Defaults to True.
        verbose (bool, optional): print available details. Defaults to True.

    Returns:
        [type]: [description]
    """
    if robust:
        estimator = LedoitWolf().fit(data)
        if verbose:
            print("LedoitWolf:")
            print("    shrinkage: ", estimator.shrinkage_)
            print("    precision: ", estimator.precision_)
            print("    location: ", estimator.location_)
        return estimator.covariance_

    return np.cov(data, rowvar=False)


def get_drawdowns(data):
    """Compute draw downs over a time series:

    Args:
        data (array-like): the time series

    Returns:
        dict: (min_index, max_index) -> drawdown mappings
    """
    emin = data[0]
    emax = data[0]
    imin = 0
    imax = 0
    n = len(data)
    drawdowns = {}
    downed = False
    for i, e in zip(range(n), data):
        if e < emin:
            emin = e
            imin = i
            downed = True
        elif e >= emax and downed:
            drawdowns[(imax, imin, i)] = (emax - emin) / emax
            emax = e
            emin = e
            imax = i
            downed = False
        elif e > emax:
            emax = e
            emin = e
            imax = i
        else:
            continue

    if (emin < emax) and downed:
        drawdowns[(imax, imin, n - 1)] = (emax - emin) / emax
    return drawdowns


def correlation_rankings(matrix, rankcount):
    """Extract tops from correlation matrix:
    - most correlated pairs
    - most uncorrelated pairs
    - most inversely correlated pairs.

    Args:
        matrix (pd.DataFrame): the correlation matrix
        rankcount ([type]): first N from the ranked tops

    Returns:
        tuple: 3 entries, each is a list of (pairs, correlation_value)
    """
    corr_dict = {}
    asset_count = len(matrix)
    rankcount = min(asset_count, rankcount)
    for row_idx in range(asset_count):
        for column_idx in range(row_idx):
            corr_dict[
                (matrix.index[row_idx], matrix.columns[column_idx])
            ] = matrix.iloc[row_idx, column_idx]
    corr_dict_keys = sorted(corr_dict, key=corr_dict.get)
    smalls = [(key, corr_dict[key]) for key in corr_dict_keys[:rankcount]]
    bigs = [(key, corr_dict[key]) for key in corr_dict_keys[-1 : -rankcount - 1 : -1]]
    corr_dict_abs = sorted(corr_dict.items(), key=lambda item: np.abs(item[1]))
    zeros = corr_dict_abs[:rankcount]
    return smalls, zeros, bigs
