from .baseportfolio import BasePortfolio

import numpy as np


class MinVariancePortfolio(BasePortfolio):
    """Class for modelling min-variance portfolios:

    Args:
        BasePortfolio (BasePortfolio): inheriting for some commonly used functions.
    """

    def __init__(self, covariances):
        """Constructor where convariances are passed in

        Args:
            covariances (np.array): covariance matrix
        """
        # inheriting from base
        super().__init__()
        self._covariances = covariances

    def get_weights(self):
        """override function from base"""
        n = len(self._covariances)
        _covariancesinv = np.linalg.inv(self._covariances)
        ones = np.ones((n, 1))
        a = _covariancesinv @ ones
        return a / (ones.T @ a)
