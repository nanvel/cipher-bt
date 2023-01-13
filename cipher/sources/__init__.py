from .base import Source
from .binance_futures_ohlc import BinanceFuturesOHLCSource
from .binance_spot_ohlc import BinanceSpotOHLCSource


SOURCES = {
    "binance_futures_ohlc": BinanceFuturesOHLCSource,
    "binance_spot_ohlc": BinanceSpotOHLCSource,
}


__all__ = ("Source", "SOURCES")
