import numpy as np
import unittest

from ..minvariance import MinVariancePortfolio


class MinVariancePortfolioTestsWithM2L2(unittest.TestCase):
    """
    docstring here
        :param unittest2.TestCase
    """

    _minvar = None

    def setUp(self):
        covariances = np.array(
            [
                [0.0049, 0.00672, 0.0105, 0.0168],
                [0.00672, 0.0144, 0.0252, 0.036],
                [0.0105, 0.0252, 0.09, 0.144],
                [0.0168, 0.036, 0.144, 0.36],
            ]
        )
        self._minvar = MinVariancePortfolio(covariances)

    def test_get_weights(self):
        actual = self._minvar.get_weights()
        np.testing.assert_allclose(
            [[1.274886723], [-0.263112728], [0.016339421], [-0.028113415]], actual
        )

    def test_covariances_(self):
        actual = self._minvar._covariances
        np.testing.assert_allclose(
            np.array(
                [
                    [0.0049, 0.00672, 0.0105, 0.0168],
                    [0.00672, 0.0144, 0.0252, 0.036],
                    [0.0105, 0.0252, 0.09, 0.144],
                    [0.0168, 0.036, 0.144, 0.36],
                ]
            ),
            actual,
        )


if __name__ == "__main__":
    unittest.main()
