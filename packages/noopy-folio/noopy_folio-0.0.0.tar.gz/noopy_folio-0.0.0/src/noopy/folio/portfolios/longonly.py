from .baseportfolio import BasePortfolio

import numpy as np
import scipy as sp


class LongOnlyPortfolio(BasePortfolio):
    """Class for modelling long-only portfolios:

    Args:
        BasePortfolio (BasePortfolio): inheriting for some commonly used functions, e.g.: get_weights
    """

    def __init__(self, covariances, returns, budget=1.0):
        """Constructor for passing in covariance matrix and returns of assets in portfolio:

        Args:
            covariances (np.array): covariance matrix
            returns (np.array): column vector for individual asset returns
            budget (float, optional): capital usable for investment, which is expressed relative term.
                1.0 represents full balance in one's account. Defaults to 1.0.
        """
        # inheriting from base
        super().__init__()
        self._covariances = covariances
        self._returns = returns

        self._budget = budget
        self._risk_aversion = None

    def get_weights(self, riskaversion=1.0):
        """Override function from base:
        - if weights have been calculated once and risk aversion hasn't changed, use cached ones;
        - otherwise, recalculate the weights

        Args:
            riskaversion (float, optional): risk aversion to reflect one's appetite. Defaults to 1.0.

        Returns:
            np.array: column vector calculated from the model
        """
        if self._weights is not None and self._risk_aversion == riskaversion:
            return self._weights

        def objective_func(weights):
            w = weights.reshape(-1, 1)

            risk = (w.T @ self._covariances @ w * 0.5 * riskaversion)[0][0]
            ret = (w.T @ self._returns)[0][0]
            return risk - ret

            sig_weights = self._covariances @ w
            to_return = sig_weights * riskaversion - self._returns
            return np.sum(to_return**2.0)

        n = len(self._returns)
        res = sp.optimize.minimize(
            objective_func,
            [1.0 / float(n)] * n,  # x0
            method="SLSQP",  # sequential least square quadratic programming
            bounds=sp.optimize.Bounds(0, np.inf),  # 0 <= x
            constraints=sp.optimize.LinearConstraint(
                np.ones((1, n)), -np.inf, self._budget
            ),  # 1^T x <= budget
            options={"disp": True, "ftol": 1e-11},
        )
        weights = res.x.reshape(n, 1)
        self._weights = weights
        return weights
