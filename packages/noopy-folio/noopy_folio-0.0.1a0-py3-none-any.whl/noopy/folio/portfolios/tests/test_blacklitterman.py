"""
test bl
"""

import numpy as np
import unittest

from ..blacklitterman import BlackLittermanPortfolio


class BlackLittermanPortfolioTestsWithMeucci2010(unittest.TestCase):
    """
    docstring here
        :param unittest2.TestCase
    """

    _bl = None

    def setUp(self):
        correlation_matrix = np.array(
            [
                [1.00, 0.54, 0.62, 0.25, 0.41, 0.59],
                [0.54, 1.00, 0.69, 0.29, 0.36, 0.83],
                [0.62, 0.69, 1.00, 0.15, 0.46, 0.65],
                [0.25, 0.29, 0.15, 1.00, 0.47, 0.39],
                [0.41, 0.36, 0.46, 0.47, 1.00, 0.38],
                [0.59, 0.83, 0.65, 0.39, 0.38, 1.00],
            ]
        )
        std_dev = np.diagflat([0.21, 0.24, 0.24, 0.25, 0.29, 0.31])
        covariance_matrix = std_dev @ correlation_matrix @ std_dev
        weights = np.atleast_2d([0.04, 0.04, 0.05, 0.08, 0.71, 0.08]).T
        risk_aversion = 2.4

        P = np.array([[0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, -1]])
        Q = np.array([[0.12], [-0.10]])
        self._bl = BlackLittermanPortfolio(
            covariance_matrix, weights, P, Q, risk_aversion
        )

    # def tearDown(self):
    #     return super().tearDown()

    def test_get_pi(self):
        """
        test get_parser() with SystemExit expected.
            :param self:
        """
        np.testing.assert_array_almost_equal(
            self._bl.get_pi(),
            np.array(
                [
                    [0.0630378],
                    [0.07080422],
                    [0.07929562],
                    [0.0798774],
                    [0.16505222],
                    [0.0978851],
                ]
            ),
        )

    def test_get_view_omega(self):
        omega = self._bl.get_view_omega()
        np.testing.assert_array_almost_equal(
            omega, np.array([[0.00288, 0.0], [0.0, 0.0055938]])
        )

    def test_get_bl_returns_covariancematrix(self):
        bl_returns, bl_cov_mat = self._bl._get_bl_returns_covariancematrix(version="v1")
        np.testing.assert_array_almost_equal(
            bl_returns,
            np.array(
                [
                    [0.07806836],
                    [0.1085098],
                    [0.0988999],
                    [0.08059798],
                    [0.13437509],
                    [0.15445164],
                ]
            ),
        )
        np.testing.assert_array_almost_equal(
            bl_cov_mat,
            np.array(
                [
                    [
                        0.04597815,
                        0.02787576,
                        0.03233678,
                        0.01358628,
                        0.02598662,
                        0.03955246,
                    ],
                    [
                        0.02787576,
                        0.05896063,
                        0.04072166,
                        0.01787563,
                        0.02593296,
                        0.06311295,
                    ],
                    [
                        0.03233678,
                        0.04072166,
                        0.05979122,
                        0.00915801,
                        0.03323489,
                        0.04967607,
                    ],
                    [
                        0.01358628,
                        0.01787563,
                        0.00915801,
                        0.06547279,
                        0.03546126,
                        0.0313635,
                    ],
                    [
                        0.02598662,
                        0.02593296,
                        0.03323489,
                        0.03546126,
                        0.08724156,
                        0.03577576,
                    ],
                    [
                        0.03955246,
                        0.06311295,
                        0.04967607,
                        0.0313635,
                        0.03577576,
                        0.09882869,
                    ],
                ]
            ),
        )

    def test_get_bl_weights(self):
        bl_weights = self._bl.get_weights(version="v1")
        np.testing.assert_array_almost_equal(
            bl_weights,
            np.array(
                [
                    [0.03809524],
                    [0.13587425],
                    [0.04761905],
                    [0.07619048],
                    [0.39394338],
                    [0.35843758],
                ]
            ),
        )


class BlackLittermanTestsWithM2L2(unittest.TestCase):
    """
    docstring here
        :param unittest2.TestCase
    """

    _bl = None

    def setUp(self):
        covariance_matrix = np.array(
            [
                [0.0049, 0.00672, 0.0105, 0.0168],
                [0.00672, 0.0144, 0.0252, 0.036],
                [0.0105, 0.0252, 0.09, 0.144],
                [0.0168, 0.036, 0.144, 0.36],
            ]
        )
        weights = np.array([[0.05], [0.40], [0.45], [0.10]])

        P = np.array([[-1, 0, 1, 0], [0, 1, 0, 0]])
        Q = np.array([[0.10], [0.03]])
        tau = 0.0083
        self._bl = BlackLittermanPortfolio(covariance_matrix, weights, P, Q, None, tau)

    # def tearDown(self):
    #     return super().tearDown()

    def test_get_pi(self):
        """
        test get_parser() with SystemExit expected.
            :param self:
        """
        np.testing.assert_array_almost_equal(
            self._bl.get_pi(), np.array([[0.0209], [0.0471], [0.1465], [0.2596]]), 4
        )

    def test_get_risk_aversion(self):
        ra = self._bl.get_risk_aversion()
        self.assertAlmostEqual(ra, 2.2369058556648116)

    def test_get_view_omega(self):
        omega = self._bl.get_view_omega()
        np.testing.assert_array_almost_equal(
            omega, np.array([[0.000615833, 0.0], [0.0, 0.00012]]), 5
        )

    def test_get_bl_returns_covariancematrix(self):
        bl_returns, bl_cov_mat = self._bl._get_bl_returns_covariancematrix("v0")
        np.testing.assert_array_almost_equal(
            bl_returns, np.array([[0.0168], [0.0375], [0.1248], [0.2270]]), 4
        )
        np.testing.assert_array_almost_equal(
            bl_cov_mat,
            np.array(
                [
                    [0.0000276650, 0.0000272705, 0.00003, 0.00006],
                    [0.0000272705, 0.000054766, 0.00007, 0.00009],
                    [0.00003, 0.00007, 0.00032, 0.00053],
                    [0.00006, 0.00009, 0.00053, 0.00196],
                ]
            ),
            5,
        )

    def test_get_bl_weights(self):
        np.testing.assert_array_almost_equal(
            self._bl.get_weights(version="v1"),
            np.array([[0.0983], [0.1663], [0.4017], [0.10]]),
            2,
        )

        np.testing.assert_allclose(
            self._bl.get_weights(version="v1", riskaversion=0.1),
            np.array([[2.1995], [3.7192], [8.9850], [2.2369]]),
            5e-2,
        )

        np.testing.assert_allclose(
            self._bl.get_weights(version="v1", riskaversion=1.0),
            np.array([[0.22], [0.3719], [0.8985], [0.2237]]),
            5e-2,
        )

        np.testing.assert_allclose(
            self._bl.get_weights(version="v1", riskaversion=6.0),
            np.array([[0.0367], [0.062], [0.1498], [0.0373]]),
            5e-2,
        )


class BlackLittermanPortfolioTestsWithIdzorek2004(unittest.TestCase):
    """
    docstring here
        :param unittest2.TestCase
    """

    def setUp(self):
        self._covariance_matrix = np.array(
            [
                [
                    0.001005,
                    0.001328,
                    -0.000579,
                    -0.000675,
                    0.000121,
                    0.000128,
                    -0.000445,
                    -0.000437,
                ],
                [
                    0.001328,
                    0.007277,
                    -0.001307,
                    -0.000610,
                    -0.002237,
                    -0.000989,
                    0.001442,
                    -0.001535,
                ],
                [
                    -0.000579,
                    -0.001307,
                    0.059852,
                    0.027588,
                    0.063497,
                    0.023036,
                    0.032967,
                    0.048039,
                ],
                [
                    -0.000675,
                    -0.000610,
                    0.027588,
                    0.029609,
                    0.026572,
                    0.021465,
                    0.020697,
                    0.029854,
                ],
                [
                    0.000121,
                    -0.002237,
                    0.063497,
                    0.026572,
                    0.102488,
                    0.042744,
                    0.039943,
                    0.065994,
                ],
                [
                    0.000128,
                    -0.000989,
                    0.023036,
                    0.021465,
                    0.042744,
                    0.032056,
                    0.019881,
                    0.032235,
                ],
                [
                    -0.000445,
                    0.001442,
                    0.032967,
                    0.020697,
                    0.039943,
                    0.019881,
                    0.028355,
                    0.035064,
                ],
                [
                    -0.000437,
                    -0.001535,
                    0.048039,
                    0.029854,
                    0.065994,
                    0.032235,
                    0.035064,
                    0.079958,
                ],
            ]
        )
        self._equil_weights = np.atleast_2d(
            [0.1934, 0.2613, 0.1209, 0.1209, 0.0134, 0.0134, 0.2418, 0.0349]
        ).T
        self._equil_returns = np.atleast_2d(
            [0.0008, 0.0067, 0.0641, 0.0408, 0.0743, 0.0370, 0.0480, 0.0660]
        ).T
        self._risk_aversion = (self._equil_weights.T @ self._equil_returns)[0, 0] / (
            self._equil_weights.T @ self._covariance_matrix @ self._equil_weights
        )[0, 0]

        self._P = np.array(
            [
                [0, 0, 0, 0, 0, 0, 1, 0],
                [-1, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0.9, -0.9, 0.1, -0.1, 0, 0],
            ]
        )
        self._Q = np.array([[0.0525], [0.0025], [0.02]])

    def test_get_pi(self):
        """
        test get_parser() with SystemExit expected.
            :param self:
        """
        pfl = BlackLittermanPortfolio(
            self._covariance_matrix,
            self._equil_weights,
            self._P,
            self._Q,
            self._risk_aversion,
            tau=0.025,
        )
        actual = pfl.get_pi()
        expected = self._equil_returns
        np.testing.assert_allclose(actual, expected, atol=1e-3)

    def test_get_view_omega(self):
        pfl = BlackLittermanPortfolio(
            self._covariance_matrix,
            self._equil_weights,
            self._P,
            self._Q,
            self._risk_aversion,
            tau=0.025,
        )
        omega = pfl.get_view_omega()
        np.testing.assert_array_almost_equal(
            omega,
            np.array(
                [[0.000709, 0.0, 0.0], [0.0, 0.000141, 0.0], [0.0, 0.0, 0.000866]]
            ),
        )

    def test_get_returns_weights_v0(self):
        pfl = BlackLittermanPortfolio(
            self._covariance_matrix,
            self._equil_weights,
            self._P,
            self._Q,
            self._risk_aversion,
            tau=0.025,
        )
        actual = pfl.get_returns(version="v0")
        expected = np.array(
            [0.0007, 0.0050, 0.0650, 0.0432, 0.0759, 0.0394, 0.0493, 0.0684]
        ).reshape(-1, 1)
        np.testing.assert_array_almost_equal(actual, expected, 4)

        # actual = self._pfl.get_weights(version='v0')
        # expected = np.array([0.2988, 0.1559, 0.0935, 0.1482, 0.0104, 0.0165, 0.2781, 0.0349]).reshape(-1, 1)
        # np.testing.assert_allclose(actual, expected)

    def test_get_returns_weights_fullconfidence(self):
        pfl = BlackLittermanPortfolio(
            self._covariance_matrix,
            self._equil_weights,
            self._P,
            self._Q,
            self._risk_aversion,
            tau=0.025,
            omega=0,
        )

        actual = pfl.get_weights(version="v1")
        expected = np.array(
            [0.4382, 0.0165, 0.0381, 0.2037, 0.0042, 0.0226, 0.3521, 0.0349]
        ).reshape(-1, 1)
        np.testing.assert_array_almost_equal(actual, expected, 2)


if __name__ == "__main__":
    unittest.main()
