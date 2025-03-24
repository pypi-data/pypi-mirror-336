"""Noojing
"""


class Portfolio:
    def __init__(self, weights=None, tickers=None) -> None:
        self._weights = weights
        self._tickers = tickers
        self._timeseries = None

    @property
    def tickers(self):
        return self._tickers

    @tickers.setter
    def tickers(self, newtickers):
        if (
            self._tickers is None
            and self._weights is not None
            and len(self._weights) != len(newtickers)
        ):
            raise ValueError(
                "[tickers] definition should have the same shape as [weights]"
                f" - weights: {self._weights}; tickers: {newtickers}."
            )

        if self._tickers is not None and len(self._tickers) != len(newtickers):
            raise ValueError(
                "[tickers] redefinition should remain the same shape"
                f" - Old: {self._tickers}; new: {newtickers}."
            )

        self._tickers = newtickers

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, newweights):
        if (
            self._tickers is None
            and self._weights is not None
            and len(self._weights) != len(newtickers)
        ):
            raise ValueError(
                "[weights] definition should have the same shape as [tickers]"
                f" - tickers: {self._tickers}; weights: {newweights}."
            )

        if self._weights is not None and len(self._weights) != len(newweights):
            raise ValueError(
                "[weights] redefinition should remain the same shape"
                f" - Old: {self._weights}; new: {newweights}."
            )

        self._weights = newweights

    @property
    def timeseries(self):
        return self._timeseries

    @timeseries.setter
    def timeseries(self, newtimeseries):
        if self.tickers is None:
            self.tickers = list(newtimeseries.columns)
            self._timeseries = newtimeseries
            return

        if len(newtimeseries.columns) != len(self.tickers):
            raise ValueError(
                "[timeseries] definition should have the consistent shape as [tickers]"
                f" - tickers: {self._tickers}; timeseries: {newtimeseries.shape}."
            )

        if (self.tickers != newtimeseries.columns).all():
            self.tickers = list(newtimeseries.columns)

        self._timeseries = newtimeseries
