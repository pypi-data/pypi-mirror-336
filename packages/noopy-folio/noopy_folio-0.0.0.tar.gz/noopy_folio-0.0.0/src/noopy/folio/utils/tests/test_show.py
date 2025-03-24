from .. import show

import unittest as ut
import pandas as pd


class ShowTests(ut.TestCase):
    def test_performance_stats(self):
        returns = pd.DataFrame(
            {
                "Portfolio 1": [0.05, 0.07, -0.01, 0.1, 0.01],
                "Portfolio 2": [0.033, -0.054, 0.3, 0.005, -0.032],
            },
            index=[
                "2011-07-01",
                "2012-07-01",
                "2013-07-01",
                "2014-07-01",
                "2015-07-01",
            ],
        )
        returns.index = pd.to_datetime(returns.index)
        actual = show.performance_stats(returns)
        expected = pd.DataFrame(
            {
                "Portfolio 1": [
                    "2011-07-01",
                    "2015-07-01",
                    5,
                    0,
                    -0.01,
                    0.1,
                    0.044,
                    0.0445,
                    -1.5810,
                    -0.0159,
                    1.2461,
                    0.9888,
                    0.1563,
                    -0.006,
                ],
                "Portfolio 2": [
                    "2011-07-01",
                    "2015-07-01",
                    5,
                    0,
                    -0.054,
                    0.3,
                    0.0504,
                    0.1435,
                    3.9449,
                    1.9399,
                    1.3284,
                    0.3513,
                    0.2629,
                    -0.0496,
                ],
            },
            [
                "Start Date",
                "End Date",
                "Count of Returns",
                "Count of NaN Returns",
                "Min of Returns",
                "Max of Returns",
                "Mean of Returns",
                "Volatility of Returns",
                "Kurtosis of Returns",
                "Skew of Returns",
                "Cumulative Returns",
                "Sharpe Ratio",
                "Max Drawdown",
                "Value at Risk (95%)",
            ],
        )
        pd.testing.assert_frame_equal(expected, actual)


if __name__ == "__main__":
    ut.main()
