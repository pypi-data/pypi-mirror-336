from .. import marketdata

import unittest as ut
from pathlib import Path


class MarketDataTests(ut.TestCase):
    def test_get_md_observable_single(self):
        close = marketdata.get_md_observable(
            "JD", cachedir=Path(__file__).resolve().parent / "data"
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "2014-05-22")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 1666)

    def test_get_md_observable_multi(self):
        close = marketdata.get_md_observable(
            ["JD", "AAPL"], cachedir=Path(__file__).resolve().parent / "data"
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "1980-12-12")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 10099)
        self.assertListEqual(list(close.columns), ["JD", "AAPL"])

    def test_get_md_observable_eod(self):
        close = marketdata.get_md_observable(
            ["JD", "AAPL"],
            cachedir=Path(__file__).resolve().parent / "data",
            frequency="1D",
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "1980-12-12")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 10099)
        self.assertListEqual(list(close.columns), ["JD", "AAPL"])

    def test_get_md_observable_eow(self):
        close = marketdata.get_md_observable(
            ["JD", "AAPL"],
            cachedir=Path(__file__).resolve().parent / "data",
            frequency="1W",
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "1980-12-12")
        self.assertEqual(close.index[1].strftime("%Y-%m-%d"), "1980-12-19")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 2091)
        self.assertListEqual(list(close.columns), ["JD", "AAPL"])

    def test_get_md_observable_eom(self):
        close = marketdata.get_md_observable(
            ["JD", "AAPL"],
            cachedir=Path(__file__).resolve().parent / "data",
            frequency="1M",
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "1980-12-31")
        self.assertEqual(close.index[1].strftime("%Y-%m-%d"), "1981-01-30")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 481)
        self.assertListEqual(list(close.columns), ["JD", "AAPL"])

    def test_get_md_observable_eoq(self):
        close = marketdata.get_md_observable(
            ["JD", "AAPL"],
            cachedir=Path(__file__).resolve().parent / "data",
            frequency="3M",
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "1980-12-31")
        self.assertEqual(close.index[1].strftime("%Y-%m-%d"), "1981-03-31")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 161)
        self.assertListEqual(list(close.columns), ["JD", "AAPL"])

    def test_get_md_observable_eoy(self):
        close = marketdata.get_md_observable(
            ["JD", "AAPL"],
            cachedir=Path(__file__).resolve().parent / "data",
            frequency="1Y",
        )
        self.assertEqual(close.index.min().strftime("%Y-%m-%d"), "1980-12-31")
        self.assertEqual(close.index.max().strftime("%Y-%m-%d"), "2020-12-31")
        self.assertEqual(len(close), 41)
        self.assertListEqual(list(close.columns), ["JD", "AAPL"])

    def test_get_symbols_from_cache(self):
        actual = marketdata.get_symbols_from_cache(
            cachedir=Path(__file__).resolve().parent / "data"
        )
        self.assertListEqual(actual, ["aapl", "jd"])


if __name__ == "__main__":
    ut.main()
