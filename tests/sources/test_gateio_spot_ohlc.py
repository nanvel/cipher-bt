import pytest

from cipher.sources import GateioSpotOHLCSource


@pytest.fixture(scope="module")
def source():
    return GateioSpotOHLCSource(symbol="BTC_USDT", interval="1h")


def test_slug(source):
    assert source.slug == "gateio_spot_ohlc/btc_usdt_1h"
