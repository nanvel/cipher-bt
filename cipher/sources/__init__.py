from .base import Source
from .binance_futures_ohlc import BinanceFuturesOHLCSource
from .binance_spot_ohlc import BinanceSpotOHLCSource
from .csv_file import CsvFileSource
from .yahoo_finance_ohlc import YahooFinanceOHLCSource


SOURCES = {
    "binance_futures_ohlc": BinanceFuturesOHLCSource,
    "binance_spot_ohlc": BinanceSpotOHLCSource,
    "csv_file": CsvFileSource,
    "yahoo_finance_ohlc": YahooFinanceOHLCSource,
}


__all__ = ("Source", "SOURCES")
