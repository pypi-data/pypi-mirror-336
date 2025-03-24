from .baseportfolio import BasePortfolio

import numpy as np
import scipy as sp


class RiskBudgetingPortfolio(BasePortfolio):
    """Class for modelling risk-budgeting portfolios:

    Args:
        BasePortfolio (BasePortfolio): inheriting for some commonly used functions, e.g.: get_weights
    """

    def __init__(
        self,
        covariances,
        returns,
        budget,
        riskbudgets=None,
        weights=None,
        by="es",
        confidence=0.99,
    ):
        """Constructor for initialising member variables

        Args:
            covariances (np.array): convariance matrix
            returns (np.array): column vector for returns of assets comprising of the portfolio
            budget (float): maximum number of captital for usage. 1 standard the full balance in one's account;
                1.5 means 50% of one's own money is borrowed
            riskbudgets (np.array, optional): column vector for risk assigned to each asset.
                It's in relative term. Defaults to None.
            weights (np.array, optional): column vector of the portfolio which is exclusive with
                riskbudgets above. Defaults to None.
            by (str, optional): risk measure option. Defaults to 'es'.
            confidence (float, optional): confidence level applied to risk measure. Defaults to 0.99.
        """
        # inheriting from base
        super().__init__()
        self._covariances = covariances
        self._returns = returns
        self._weights = weights

        # specific to class itself
        self._budgets = budget
        self._risk_budgets = riskbudgets
        self._confidence = confidence
        self._risk_measure = by

    def get_weights(self, by="es", confidence=0.99):
        """Get weights for the portfolio:
        - if risk budget allocation is not define, return whatever is from its base get_weights
        - if weights have been calculated and no change in risk measure yet, return cached _weights
        - otherwise, recalculate weights from risk budgeting definition
        """
        if self._risk_budgets is None:
            return super().get_weights()

        if (
            self._risk_measure == by
            and self._confidence == confidence
            and self._weights is not None
        ):
            return self._weights

        def objective_func(init_weights):
            sig_weights = self._covariances @ init_weights
            marginal_risk = sig_weights / np.sqrt(init_weights @ sig_weights)
            if by == "var":
                c = sp.stats.norm.ppf(confidence)
                marginal_risk = self._returns.T - c * marginal_risk
            elif by == "es":
                c = sp.stats.norm.pdf(sp.stats.norm.ppf(confidence)) / (
                    1.0 - confidence
                )
                marginal_risk = self._returns.T - c * marginal_risk
            elif by != "volatility":
                raise ValueError(f"risk measure [{by}] is not recognized.")
            rc = init_weights * marginal_risk
            rc = rc / np.sum(rc)
            return np.sum((rc - self._risk_budgets.T) ** 2.0)

        n = len(self._returns)
        res = sp.optimize.minimize(
            objective_func,
            [1.0 / float(n)] * n,  # x0
            method="SLSQP",  # sequential least square quadratic programming
            bounds=sp.optimize.Bounds(0, np.inf),  # 0 <= x long only
            constraints=sp.optimize.LinearConstraint(
                [1] * n, -np.inf, self._budgets
            ),  # 1^T x <=budget
        )
        weights = np.atleast_2d(res.x).reshape(n, 1)
        self._weights = weights
        self._risk_measure = by
        self._confidence = confidence
        return weights
