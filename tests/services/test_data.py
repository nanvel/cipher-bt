import datetime
from pathlib import Path

import pytest
from pandas import DataFrame

from cipher.services.data import DataService
from cipher.sources import Source
from cipher.models import Time

from .. import DATA_PATH


class FakeOHLCSource(Source):
    def __init__(self, raise_error=False):
        self.raise_error = raise_error

    @property
    def slug(self):
        return "fake_ohlc/btcusdt_1h"

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        if self.raise_error:
            raise AssertionError("Should not be called!")

        return (
            Time.from_timestamp(1578600000000),
            Time.from_timestamp(1580396400000),
            True,
        )


def test_use_cached():
    cache_path = DATA_PATH / "sources_cache"
    service = DataService(cache_root=cache_path)
    source = FakeOHLCSource(raise_error=True)

    result = service.load_df(
        source=source,
        start_ts=Time.from_datetime(
            datetime.datetime(2020, 1, 1),
        ),
        stop_ts=Time.from_datetime(
            datetime.datetime(2020, 1, 2),
        ),
    )

    assert isinstance(result, DataFrame)
    assert result.shape == (1, 10)


def test_load():
    cache_path = DATA_PATH / "sources_cache"
    service = DataService(cache_root=cache_path)
    source = FakeOHLCSource()

    with pytest.raises(FileNotFoundError) as e:
        service.load_df(
            source=source,
            start_ts=Time.from_datetime(
                datetime.datetime(2020, 1, 1),
            ),
            stop_ts=Time.from_datetime(
                datetime.datetime(2020, 1, 15),
            ),
        )

    assert "fake_ohlc/btcusdt_1h/1579494600.csv" in str(e.value)
    assert "fake_ohlc/btcusdt_1h/1578600000_1580396400.csv" in str(e.value)
