from ..utils.show import verbose_print

from pathlib import Path

import yfinance as yf
import numpy as np
import pandas as pd

import concurrent.futures

# The by-default path directory
_md_cache_dir = Path.home() / "noofolio/md_cache"


def get_md_observable(
    symbols,
    observable="Adj Close",
    startdate=None,
    enddate=None,
    cachedir=_md_cache_dir,
    frequency="1D",
):
    """Get historical time series for a particular market observable:
    - delegate data sourcing to _get_daily_md_observable;
    - and then transform by frequency

    Args:
        symbols (array-like): a list of valid symbols
        observable (str, optional): Valid market observable. Defaults to 'Adj Close'.
        startdate (str|datetime, optional): start of historical period of format 'yyyy-mm-dd' if str. Defaults to None.
        enddate (str|datetime, optional): end of historical period of format 'yyyy-mm-dd' if str. Defaults to None.
        cachedir (Path, optional): directory where market data is cached. Defaults to _md_cache_dir.
        frequency (str, optional): available ones - 1D, 1W, 1M, 3M and 1Y. Defaults to '1D'.

    Raises:
        ValueError: throws if frequency is not recognized

    Returns:
        pd.DataFrame: time on rows and symbols on columns
    """
    md = _get_daily_md_observable(symbols, observable, startdate, enddate, cachedir)
    freq_upper = frequency.upper()
    if freq_upper == "1D":
        return md

    if freq_upper == "1W":
        # the last incomplete week of year will be put into the 1 week of new
        # year, so need special handling here
        md["GroupKey"] = [
            (
                i.year + 1 if i.month == 12 and i.isocalendar()[1] < 2 else i.year,
                i.isocalendar()[1],
            )
            for i in md.index
        ]
        return md.groupby(md["GroupKey"]).tail(1).drop(columns="GroupKey")

    if freq_upper == "1M":
        return md.groupby([md.index.year, md.index.month]).tail(1)

    if freq_upper == "3M":
        return md.groupby([md.index.year, md.index.quarter]).tail(1)

    if freq_upper == "1Y":
        return md.groupby(md.index.year).tail(1)

    raise ValueError(
        f"Unsupported value for parameter [frequency]: {frequency}. \
        Valid options - 1D, 1W, 1M, 3M and 1Y"
    )


def get_md_rfr(startdate=None, enddate=None, frequency="1Y"):
    """Get historical time series for risk-free rates:
    - currently treasury 3M rates manually sourcing from https://fred.stlouisfed.org/series/TB3MS and cached;
    - simple transformation by frequency

    Args:
        startdate (str|datetime, optional): start of historical period of format 'yyyy-mm-dd' if str. Defaults to None.
        enddate (str|datetime, optional): end of historical period of format 'yyyy-mm-dd' if str. Defaults to None.
        frequency (str, optional): available ones - 1D, 1W, 1M, 3M and 1Y. Defaults to '1Y'.

    Raises:
        ValueError: throws if frequency is not recognized

    Returns:
        pd.DataFrame: time and rows and a single column for the rate
    """
    rfr_path = Path(__file__).parent / "datastore/rfr_treasury3m.csv"
    rfr = pd.read_csv(rfr_path, index_col="DATE")
    rfr.index = pd.to_datetime(rfr.index)
    if startdate is not None:
        rfr = rfr[rfr.index >= startdate]
    if enddate is not None:
        rfr = rfr[rfr.index <= enddate]
    rfr = rfr / 100

    freq_upper = frequency.upper()
    if freq_upper == "1D":
        return rfr / 360

    if freq_upper == "1W":
        return rfr * 7 / 360

    if freq_upper == "1M":
        return rfr * 30 / 360

    if freq_upper == "3M":
        return rfr * 90 / 360

    if freq_upper == "1Y":
        return rfr

    raise ValueError(
        f"Unsupported value for parameter [frequency]: {frequency}. \
        Valid options - 1D, 1W, 1M, 3M and 1Y"
    )


def get_asset_info():
    """Get asset related attributes:
    - currently manually sourcing from https://www.nasdaq.com/market-activity/stocks/screener, as of 13th Jan,2021 and get it cached

    Returns:
        pd.DataFrame: each column is an associated attribute of an asset
    """
    symbols_path = Path(__file__).parent / "datastore/symbols.csv"
    return pd.read_csv(symbols_path)


def get_symbols_from_cache(cachedir=_md_cache_dir):
    """Extact out list of symbols from cached data:

    Args:
        cachedir (Path, optional): directory where market data is cached. Defaults to _md_cache_dir.

    Returns:
        array: list of asset symbols
    """
    paths = list(Path(cachedir).rglob("*.csv"))
    symbols = []
    for path in paths:
        if path.is_file():
            symbol = (
                path.name.replace(".csv", "").replace("md_", "").replace("%2f", "/")
            )
            symbols.append(symbol)
    return symbols


def precache_md(symbols, cachedir=_md_cache_dir, verbose=True):
    """Batch cache market data for later usage so to avoid:
    - avoid internet connection stability issue;
    - improve performance for avoiding repeated remote downloading

    Args:
        symbols (array-like): a list of valid symbols
        cachedir (Path, optional): directory where market data is cached. Defaults to _md_cache_dir.
        verbose (bool, optional): print out some more details on retrieval and progress. Defaults to True.

    Returns:
        int: number of symbols successfully cached
    """
    symbol_count = len(symbols)
    print(f"It's in total {symbol_count} symbols to download.")

    cached_count = 0
    for i in range(symbol_count):
        verbose_print(verbose, f"Resolving {i+1}/{symbol_count} {symbols[i]}...")
        try:
            s_encoded = symbols[i].replace("/", "%2f").lower()
            file_path = cachedir / f"md_{s_encoded}.csv"
            if file_path.exists():
                verbose_print(verbose, f"{symbols[i]} already exists, so skip.")
                continue
            data = yf.download(symbols[i], threads=False, progress=verbose)
            if data is not None and not data.empty:
                data.to_csv(file_path)
                verbose_print(verbose, f"{symbols[i]} saved.")
                cached_count += 1
        except Exception as ex:
            print(ex)
    return cached_count


def _get_daily_md_observable(
    symbols, observable, startdate=None, enddate=None, cachedir=_md_cache_dir
):
    """Get historical daily time series for a particular market observable:
    - sourced from Yahoo Finance only for now;
    - with cached data taken as priority

    Args:
        symbols (array-like): a list of valid symbols
        observable (str, optional): Valid market observable. Defaults to 'Adj Close'.
        startdate (str|datetime, optional): start of historical period of format 'yyyy-mm-dd' if str. Defaults to None.
        enddate (str|datetime, optional): end of historical period of format 'yyyy-mm-dd' if str. Defaults to None.
        cachedir (Path, optional): directory where market data is cached. Defaults to _md_cache_dir.

    Returns:
        pd.DataFrame: time on rows and symbols on columns
    """
    symbols = [symbols] if isinstance(symbols, str) else symbols

    if cachedir is not None and not cachedir.exists():
        cachedir.mkdir(parents=True)

    def _retrieve_md(symbol):  # , observable, startdate, enddate, cachedir
        file_path = None if cachedir is None else cachedir / f"md_{symbol}.csv".lower()
        md = None
        if file_path is not None and file_path.exists():
            md = pd.read_csv(file_path, index_col="Date")
        else:
            md = yf.download(symbol)
            if file_path is not None:
                md.to_csv(file_path)
        if md.empty:
            return None
        md.index = pd.to_datetime(md.index)
        md = md[[observable]]
        md.columns = [symbol.upper()]
        if startdate is not None:
            md = md[md.index >= startdate]
        if enddate is not None:
            md = md[md.index <= enddate]
        return md

    md_joined = None
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for md in executor.map(_retrieve_md, symbols):
            if md_joined is None:
                md_joined = md
            elif md is not None:
                md_joined = md_joined.join(md, how="outer")
            else:
                continue

        # futures = []
        # for symbol in symbols:
        #     futures.append(executor.submit(_retrieve_md, symbol, observable, startdate, enddate, cachedir))
        # for future in concurrent.futures.as_completed(futures):
        #     md = future.result()
        #     if md_joined is None:
        #         md_joined = md
        #     elif md is not None:
        #         md_joined = md_joined.join(md, how='outer')
        #     else:
        #         continue
    return md_joined

    md_joined = None
    # download one by one to avoid rejection
    for symbol in symbols:
        file_path = None if cachedir is None else cachedir / f"md_{symbol}.csv".lower()
        md = None
        if file_path is not None and file_path.exists():
            md = pd.read_csv(file_path, index_col="Date")
        else:
            md = yf.download(symbol)
            if file_path is not None:
                md.to_csv(file_path)

        if md.empty:
            continue

        md.index = pd.to_datetime(md.index)
        md = md[[observable]]
        md.columns = [symbol.upper()]
        if startdate is not None:
            md = md[md.index >= startdate]
        if enddate is not None:
            md = md[md.index <= enddate]

        if md_joined is None:
            md_joined = md
        else:
            md_joined = md_joined.join(md, how="outer")

    return md_joined
