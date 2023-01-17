import datetime

from cipher.models.time_delta import TimeDelta


def test_to_seconds():
    assert TimeDelta(10) == 10


def test_to_timedelta():
    assert TimeDelta(10).to_timedelta() == datetime.timedelta(seconds=10)


def test_str():
    assert str(TimeDelta(0)) == "0s"
    assert str(TimeDelta(10)) == "10s"
    assert str(TimeDelta(70)) == "1m 10s"
    assert str(TimeDelta(3700)) == "1h 1m 40s"
    assert str(TimeDelta(3600 * 24 * 5 + 60)) == "5d 1m"
