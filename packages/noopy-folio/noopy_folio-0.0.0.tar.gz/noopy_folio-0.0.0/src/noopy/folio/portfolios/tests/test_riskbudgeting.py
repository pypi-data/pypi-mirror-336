from ..riskbudgeting import RiskBudgetingPortfolio

import unittest
import numpy as np


class RiskBudgetingPortfolioTestsWithElectiveRBPort1(unittest.TestCase):

    def setUp(self):
        correlations = np.array(
            [[1.00, 0.50, 0.25], [0.50, 1.00, 0.60], [0.25, 0.60, 1.00]]
        )
        std_dev = np.diagflat([0.02, 0.03, 0.01])
        covariances = std_dev @ correlations @ std_dev
        returns = np.array([[0.005], [0.003], [0.002]])
        weights = np.array([[0.5203], [0.1439], [0.3358]])
        self._portfolio = RiskBudgetingPortfolio(
            covariances, returns, 1.0, weights=weights
        )

    def test_get_valueatrisk(self):
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.90), -0.0152, 4)
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.95), -0.0206, 4)
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.99), -0.0306, 4)
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.995), -0.0343, 4)

    def test_get_expectedshortfall(self):
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.90), -0.0222, 4)
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.95), -0.0267, 4)
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.99), -0.0356, 4)
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.995), -0.0390, 4)


@unittest.skip("to correct according to baseline later")
class RiskBudgetingPortfolioTestsWithElectiveRBPort2(unittest.TestCase):

    def setUp(self):
        correlations = np.array(
            [[1.00, 0.50, 0.25], [0.50, 1.00, 0.60], [0.25, 0.60, 1.00]]
        )
        std_dev = np.diagflat([0.02, 0.03, 0.01])
        covariances = std_dev @ correlations @ std_dev
        returns = np.array([[0.005], [0.003], [0.002]])
        # weights = np.array([[0.7305], [-0.2021], [0.4716]])
        weights = np.array([[488.0], [-135.0], [315]])
        self._portfolio = RiskBudgetingPortfolio(
            covariances, returns, 1.0, weights=weights
        )

    def test_get_valueatrisk(self):
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.90), -0.0568, 4)
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.95), -0.0745, 4)
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.99), -0.1076, 4)
        self.assertAlmostEqual(self._portfolio.get_valueatrisk(0.995), -0.1198, 4)

    def test_get_expectedshortfall(self):
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.90), -0.0798, 4)
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.95), -0.0948, 4)
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.99), -0.1241, 4)
        self.assertAlmostEqual(self._portfolio.get_expectedshortfall(0.995), -0.1352, 4)


class RiskBudgetingPortfolioTestsWithElectiveRBExample7(unittest.TestCase):

    def setUp(self):
        correlations = np.array(
            [[1.00, 0.80, 0.50], [0.80, 1.00, 0.30], [0.50, 0.30, 1.00]]
        )
        std_dev = np.diagflat([0.30, 0.20, 0.15])
        covariances = std_dev @ correlations @ std_dev
        returns = np.array([[0.0], [0.0], [0.0]])
        weights = np.array([[0.5], [0.2], [0.3]])
        self._portfolio = RiskBudgetingPortfolio(
            covariances, returns, 1.0, weights=weights
        )

    def test_get_variance(self):
        self.assertAlmostEqual(self._portfolio.get_variance(), 0.043555, 6)

    def test_get_riskcontribution(self):
        np.testing.assert_allclose(
            self._portfolio.get_riskcontribution(returnpercentage=False),
            np.array([[0.1470], [0.0333], [0.0285]]),
            2e-3,
        )
        np.testing.assert_allclose(
            self._portfolio.get_riskcontribution(returnpercentage=True),
            np.array([[0.7043], [0.1593], [0.1364]]),
            3e-4,
        )

        np.testing.assert_allclose(
            self._portfolio.get_riskcontribution(
                by="var", confidence=0.99, returnpercentage=False
            ),
            np.array([[-0.3419], [-0.0774], [-0.0662]]),
            6e-4,
        )
        np.testing.assert_allclose(
            self._portfolio.get_riskcontribution(
                by="var", confidence=0.99, returnpercentage=True
            ),
            np.array([[0.7043], [0.1593], [0.1364]]),
            3e-4,
        )

        np.testing.assert_allclose(
            self._portfolio.get_riskcontribution(
                by="es", confidence=0.99, returnpercentage=False
            ),
            np.array([[-0.3917], [-0.0886], [-0.0759]]),
            6e-4,
        )
        np.testing.assert_allclose(
            self._portfolio.get_riskcontribution(
                by="es", confidence=0.99, returnpercentage=True
            ),
            np.array([[0.7043], [0.1593], [0.1364]]),
            3e-4,
        )


class RiskBudgetingPortfolioTestsWithElectiveRBExample11(unittest.TestCase):

    def setUp(self):
        correlations = np.array(
            [[1.00, 0.80, 0.50], [0.80, 1.00, 0.30], [0.50, 0.30, 1.00]]
        )
        std_dev = np.diagflat([0.30, 0.20, 0.15])
        covariances = std_dev @ correlations @ std_dev
        returns = np.array([[0.10], [0.05], [0.09]])
        risk_budgets = np.array([[0.5], [0.2], [0.3]])
        self._portfolio = RiskBudgetingPortfolio(
            covariances, returns, 1.0, riskbudgets=risk_budgets
        )

    def test_get_weights(self):
        np.testing.assert_allclose(
            self._portfolio.get_weights(confidence=0.95),
            np.array([[0.2821], [0.1968], [0.5211]]),
            atol=5e-4,
        )
        np.testing.assert_allclose(
            self._portfolio.get_weights(confidence=0.99),
            np.array([[0.29], [0.2026], [0.5074]]),
            atol=5e-4,
        )


if __name__ == "__main__":
    unittest.main()
