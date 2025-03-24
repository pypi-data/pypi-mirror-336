import numpy as np


def balance_weights_with_cash(riskyassetweights):
    """get weights that consider the portion borrowed on risk free rate:

    Args:
        riskyassetweights (np.array): weights for all risky assets

    Returns:
        np.array: vector that appends risk-free part
    """
    weights_sum = np.sum(riskyassetweights)
    cash_weight = 1.0 - weights_sum
    weights = np.append(riskyassetweights, cash_weight).reshape(-1, 1)
    return weights
