import datetime

from cipher.factories.datas import DatasFactory

from cipher.sources import BinanceFuturesOHLCSource
from cipher.models import Interval, Time

from .. import DATA_PATH


def test_find_cached():
    cache_path = DATA_PATH / "sources_cache"

    factory = DatasFactory(cache_root=cache_path)

    source = BinanceFuturesOHLCSource(
        symbol="BTCUSDT", interval=Interval.from_binance_slug("1h")
    )

    datas = factory.from_sources(
        sources=[source],
        start_ts=Time.from_datetime(
            datetime.datetime(2022, 1, 1),
        ),
        stop_ts=Time.from_datetime(
            datetime.datetime(2022, 1, 2),
        ),
    )

    assert False
