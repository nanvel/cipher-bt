import datetime

from cipher.models.time_delta import TimeDelta


def test_to_seconds():
    assert TimeDelta(seconds=10).seconds == 10


def test_to_timedelta():
    assert TimeDelta(seconds=10).to_timedelta() == datetime.timedelta(seconds=10)
