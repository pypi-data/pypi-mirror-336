from .baseportfolio import BasePortfolio

import numpy as np


class BlackLittermanPortfolio(BasePortfolio):
    """Class for modelling Black-Litterman portfolios

    Args:
        BasePortfolio (BasePortfolio): inheriting for some commonly used functions, e.g.: get_weights
    """

    def __init__(
        self,
        equilcovariances,
        equilweights,
        P,
        Q,
        riskaversion=None,
        tau=0.05,
        omega=None,  # specified values here is take as priority
    ):
        """Constructor for passing equilibrium parameters and views:

        Args:
            equilcovariances (np.array): covariance matrix from equilibrium portfolio
            equilweights (np.array): column vector for weights from equilibrium portfolio
            P (np.array): K x N matrix, where K is number of views and N is number of assets
            Q (np.array): K column vector for absolute or relative returns
            riskaversion (float, optional): if not defined, calculate a default in the constructor. Defaults to None.
            tau (float, optional): ratio of covariances between views and estimated returns. Defaults to 0.05.
            omega (np.array, optional): K x K matrix, which avoids hassle of estimating omega in model. Defaults to None.
        """

        # inheriting from base
        super().__init__()

        self._equil_covariances = equilcovariances
        self._equil_weights = equilweights

        # Initial portfolio: Sigma, weigh, risk aversion
        if riskaversion is None:
            # reference Idzorek(2002) A STEP-BY-STEP GUIDE TO THE BLACK-LITTERMAN MODEL
            self._risk_aversion = 0.5 / np.sqrt(
                (equilweights.T @ equilcovariances @ equilweights)[0, 0]
            )
        else:
            self._risk_aversion = riskaversion

        # views; P, v
        self._P = P
        self._Q = Q
        self._tau = tau

        self._pi = None
        self._omega = omega  # calculated

        return

    def get_covariances(self, **kwargs):
        """override function from base"""
        if self._covariances is None:
            self._get_bl_returns_covariancematrix(**kwargs)
        return self._covariances

    def get_weights(self, **kwargs):
        """Override function from base"""
        return self._get_bl_weights(**kwargs)

    def get_returns(self, **kwargs):
        """Override function from base"""
        if self._returns is None:
            self._get_bl_returns_covariancematrix(**kwargs)
        return self._returns

    def get_pi(self):
        """Estimate returns from the equilibrium portfolio"""
        if self._pi is None:
            self._pi = self._risk_aversion * (
                self._equil_covariances @ self._equil_weights
            )
        return self._pi

    def get_view_omega(self):
        """get covariances on views:
        for now, we simply take \tau P * \Sigma * P
        """
        if self._omega is None:
            self._omega = np.diagflat(
                np.diag(self._tau * self._P @ self._equil_covariances @ self._P.T)
            )
        return self._omega

    def get_risk_aversion(self):
        """Get risk aversion"""
        return self._risk_aversion

    def _get_bl_returns_covariancematrix(self, version):
        """Get updated covariance matrix and returns upon BL model:
        use different formula in Meucci(2010) - The Black-Litterman Approach: Original Model and Extensions

        Args:
            version (str): valid string - v0, v1 and v2, which can be seen from related private functions below

        Raises:
            ValueError: throws if no valid string for version

        Returns:
            tuple: BL returns and BL covariance matrix
        """
        if version == "v0":
            return self._get_bl_returns_covariancematrix_v0()
        elif version == "v1":
            return self._get_bl_returns_covariancematrix_v1()
        else:
            raise ValueError(
                f'Invalid value for {version} - only "v0" or "v1" are supported.'
            )

    def _get_bl_weights(self, version, riskaversion=None):
        """get BL weights:
        - use analytical solution for unconstrained optimization if calculating for the 1st time;
        - otherwise, use the cached one

        Args:
            version (str): valid string - v0, v1 and v2, which can be seen from related private functions below
            riskaversion (float, optional): update risk aversion if given here. Defaults to None.

        Returns:
            np.array: BL weights
        """
        # can specify different risk aversion?
        risk_aversion = self._risk_aversion if riskaversion is None else riskaversion
        if self._returns is None:
            self._get_bl_returns_covariancematrix(version)
        bl_weights = np.linalg.inv(self._covariances) @ self._returns / risk_aversion
        return bl_weights

    def _get_bl_returns_covariancematrix_v0(self):
        """Get BL returns and covariance by Meucci(2010):
        - eq(16) for returns;
        - eq(17) for covariance matrix

        Returns:
            tuple: BL returns and BL covariance matrix
        """
        if self._returns is None or self._covariances is None:
            a = np.linalg.inv(self._tau * self._equil_covariances)
            omega_inv = np.linalg.inv(self.get_view_omega())
            # eq(17)
            self._covariances = np.linalg.inv(a + self._P.T @ omega_inv @ self._P)
            # eq(16)
            self._returns = self._covariances @ (
                a @ self.get_pi() + self._P.T @ omega_inv @ self._Q
            )
        return self._returns, self._covariances

    def _get_bl_returns_covariancematrix_v1(self):
        """Get BL returns and covariance by Meucci(2010):
        - eq(20) for returns;
        - eq(21) for covariance matrix

        Returns:
            tuple: BL returns and BL covariance matrix
        """
        if self._returns is None or self._covariances is None:
            temp_mat = (
                self._equil_covariances
                @ self._P.T
                @ np.linalg.inv(
                    self._tau * self._P @ self._equil_covariances @ self._P.T
                    + self.get_view_omega()
                )
            )
            # eq(20)
            self._returns = self.get_pi() + self._tau * temp_mat @ (
                self._Q - self._P @ self.get_pi()
            )
            # eq(21)
            self._covariances = (1 + self._tau) * self._equil_covariances - np.square(
                self._tau
            ) * temp_mat @ self._P @ self._equil_covariances
        return self._returns, self._covariances

    def _get_bl_returns_covariancematrix_v2(self):
        """Get BL returns and covariance by Meucci(2010):
        - eq(32) for returns;
        - eq(33) for covariance matrix

        Returns:
            tuple: BL returns and BL covariance matrix
        """
        p_sig = self._P @ self._equil_covariances
        p_sig_p_omega = p_sig @ self._P.T + self.get_view_omega()
        p_sig_p_omega_inv = np.linalg.inv(p_sig_p_omega)

        # eq(32)
        self._returns = self.get_pi() + p_sig.T @ p_sig_p_omega_inv @ (
            self._Q - self._P @ self.get_pi()
        )
        # eq(33)
        self._covariances = self._covariances - p_sig.T @ p_sig_p_omega_inv @ p_sig

        return self._returns, self._covariances
