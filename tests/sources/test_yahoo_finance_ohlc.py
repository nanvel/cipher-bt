import pytest

from cipher.sources import YahooFinanceOHLCSource


@pytest.fixture(scope="module")
def source():
    return YahooFinanceOHLCSource(symbol="SPY", interval="1d")


def test_slug(source):
    assert source.slug == "yahoo_finance_ohlc/spy_1d"
