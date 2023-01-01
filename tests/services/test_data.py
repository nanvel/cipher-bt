import datetime

from cipher.services.data import DataService
from cipher.sources import BinanceFuturesOHLCSource
from cipher.models import Interval, Time

from .. import DATA_PATH


def test_find_cached():
    cache_path = DATA_PATH / "sources_cache"

    service = DataService(cache_root=cache_path)

    source = BinanceFuturesOHLCSource(
        symbol="BTCUSDT", interval=Interval.from_binance_slug("1h")
    )

    result = service.load_df(
        source=source,
        start_ts=Time.from_datetime(
            datetime.datetime(2022, 12, 20),
        ),
        stop_ts=Time.from_datetime(
            datetime.datetime(2023, 1, 30),
        ),
    )

    assert False
