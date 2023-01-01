from cipher.models import Interval


def test_from_seconds():
    result = Interval.from_seconds(seconds=10)

    assert result.seconds == 10


def test_from_binance_slug():
    result = Interval.from_binance_slug(slug="5m")

    assert result.seconds == 300


def test_to_seconds():
    result = Interval(seconds=10).to_seconds()

    assert result == 10


def test_to_slug():
    result = Interval(seconds=3600).to_slug()

    assert result == "1h"


def test_to_binace_slug():
    result = Interval(seconds=60).to_slug()

    assert result == "1m"
