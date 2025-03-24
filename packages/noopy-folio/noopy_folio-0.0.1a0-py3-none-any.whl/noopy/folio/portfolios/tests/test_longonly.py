import numpy as np
import unittest

from ..longonly import LongOnlyPortfolio


class MinVariancePortfolioTestsWithM2L2(unittest.TestCase):
    """
    docstring here
        :param unittest2.TestCase
    """

    @unittest.skip("TODO")
    def test_get_weights(self):
        covariances = np.array(
            [
                [0.00134078, 0.00062061, 0.00047558, 0.0006046, 0.00051926],
                [0.00062061, 0.00166603, 0.00079953, 0.00083863, 0.00065944],
                [0.00047558, 0.00079953, 0.00137338, 0.00068738, 0.00057304],
                [0.0006046, 0.00083863, 0.00068738, 0.00122116, 0.00066706],
                [0.00051926, 0.00065944, 0.00057304, 0.00066706, 0.00099067],
            ]
        )
        returns = np.array(
            [0.01080418, 0.02082959, 0.04461181, 0.0, -0.00791353]
        ).reshape(-1, 1)
        pfl = LongOnlyPortfolio(covariances, returns, 2.0)
        actual = pfl.get_weights()
        np.testing.assert_allclose(
            np.array(
                [3.12182587, 4.01881406, 3.42687937, 3.52325076, 2.98910226]
            ).reshape(-1, 1),
            actual,
        )

    def test_get_weights2(self):
        correlations = np.array(
            [[1.00, 0.80, 0.50], [0.80, 1.00, 0.30], [0.50, 0.30, 1.00]]
        )
        std_dev = np.diagflat([0.30, 0.20, 0.15])
        covariances = std_dev @ correlations @ std_dev
        returns = np.array([[0.005], [0.003], [0.002]])
        pfl = LongOnlyPortfolio(covariances, returns, 2.0)
        actual = pfl.get_weights()
        np.testing.assert_allclose(
            np.array([0.02499018, 0.03366601, 0.05042882]).reshape(-1, 1),
            actual,
            atol=1e-8,
        )


if __name__ == "__main__":
    unittest.main()
