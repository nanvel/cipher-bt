from cipher.models import Interval


def test_from_binance_slug():
    result = Interval.from_binance_slug(slug="5m")

    assert result == 300


def test_to_slug():
    result = Interval(3600).to_slug()

    assert result == "1h"


def test_to_binance_slug():
    result = Interval(60).to_slug()

    assert result == "1m"


def test_mul():
    result = Interval(60) * 15

    assert result == 60 * 15
