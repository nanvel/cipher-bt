from .base import Source
from .binance_futures_ohlc import BinanceFuturesOHLCSource
from .binance_spot_ohlc import BinanceSpotOHLCSource
from .csv_file import CsvFileSource


SOURCES = {
    "binance_futures_ohlc": BinanceFuturesOHLCSource,
    "binance_spot_ohlc": BinanceSpotOHLCSource,
    "csv_file": CsvFileSource,
}


__all__ = ("Source", "SOURCES")
