from .. import math

import unittest as ut
import numpy as np
import pandas as pd


class MathTests(ut.TestCase):
    def test_get_cov(self):
        # TODO
        return

    def test_get_drawdowns(self):
        data = [1] * 10
        self.assertDictEqual(math.get_drawdowns(data), {})

        data = [1, 0.2, 0.3, 0.05, 1]
        self.assertDictEqual(math.get_drawdowns(data), {(0, 3, 4): 0.95})

        data = [1, 0.2, 0.3, 2.0, 0.05, 1]
        self.assertDictEqual(
            math.get_drawdowns(data), {(0, 1, 3): 0.8, (3, 4, 5): 0.975}
        )

        data = [1, 0.2, 0.3, 2.0, 2.3, 2.5, 0.5, 1.5]
        self.assertDictEqual(math.get_drawdowns(data), {(0, 1, 3): 0.8, (5, 6, 7): 0.8})

        data = [1, 0.2, 0.3, 2.0, 0.05, 3.5]
        self.assertDictEqual(
            math.get_drawdowns(data), {(0, 1, 3): 0.8, (3, 4, 5): 0.975}
        )
        self.assertDictEqual(
            math.get_drawdowns(pd.Series(data)), {(0, 1, 3): 0.8, (3, 4, 5): 0.975}
        )

    def test_correlation_rankings(self):
        samples = pd.DataFrame(
            {
                "column1": [0.1, 1.5, 1.3, 1.0, 0.9, 0.8],
                "column2": [0.2, 0.5, 0.3, 0.0, 0.5, 0.3],
                "column3": [-0.1, -2.5, 3.3, 0.1, 0.9, 0.8],
            }
        )
        s, z, b = math.correlation_rankings(samples.corr(), 2)

        columns = sorted(set(np.array([i[0] for i in s]).flatten()))
        self.assertSequenceEqual(columns, ["column1", "column2", "column3"])

        self.assertSequenceEqual(s[0][0], ("column3", "column2"))
        self.assertSequenceEqual(s[1][0], ("column3", "column1"))
        self.assertAlmostEqual(s[0][1], -0.19119537521843286)
        self.assertAlmostEqual(s[1][1], -0.0557977069592031)

        self.assertSequenceEqual(z[0][0], ("column3", "column1"))
        self.assertSequenceEqual(z[1][0], ("column3", "column2"))
        self.assertAlmostEqual(z[0][1], -0.0557977069592031)
        self.assertAlmostEqual(z[1][1], -0.19119537521843286)

        self.assertSequenceEqual(b[0][0], ("column2", "column1"))
        self.assertSequenceEqual(b[1][0], ("column3", "column1"))
        self.assertAlmostEqual(b[0][1], 0.36991501890585793)
        self.assertAlmostEqual(b[1][1], -0.0557977069592031)


if __name__ == "__main__":
    ut.main()
