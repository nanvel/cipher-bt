from .base import Source
from .binance_futures_ohlc import BinanceFuturesOHLCSource


SOURCES = {
    'binance_futures_ohlc': BinanceFuturesOHLCSource,
}


__all__ = ("Source", "SOURCES")
