import datetime

from cipher.models.time_delta import TimeDelta


def test_to_seconds():
    assert TimeDelta(seconds=10).seconds == 10


def test_to_timedelta():
    assert TimeDelta(seconds=10).to_timedelta() == datetime.timedelta(seconds=10)


def test_str():
    assert str(TimeDelta(seconds=0)) == "0s"
    assert str(TimeDelta(seconds=10)) == "10s"
    assert str(TimeDelta(seconds=70)) == "1m 10s"
    assert str(TimeDelta(seconds=3700)) == "1h 1m 40s"
    assert str(TimeDelta(seconds=3600 * 24 * 5 + 60)) == "5d 1m"
