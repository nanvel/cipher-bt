from cipher.models import Interval


def test_from_slug():
    assert Interval.from_binance_slug(slug="5m") == 300
    assert Interval.from_yfinance_slug(slug="2m") == 120
    assert Interval.from_gateio_slug(slug="5m") == 300


def test_to_slug():
    assert Interval(300).to_binance_slug() == "5m"
    assert Interval(300).to_yfinance_slug() == "5m"
    assert Interval(300).to_gateio_slug() == "5m"


def test_mul():
    result = Interval(60) * 15

    assert result == 60 * 15
