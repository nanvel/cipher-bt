import datetime

from cipher.models import Interval, Time


def test_from_timestamp():
    result = Time(10)

    assert result == 10


def test_from_datetime():
    dt = datetime.datetime(2000, 1, 2, 3, 4)
    result = Time.from_datetime(dt)

    assert result == 946_782_240
    assert result.to_datetime() == dt


def test_to_datetime():
    ts = 940_000_000
    result = Time(ts)

    assert result.to_datetime() == datetime.datetime(1999, 10, 15, 15, 6, 40)


def test_compare():
    ts = 940_000_000
    delta = 100
    time1 = Time(ts)
    time2 = Time(ts + delta)

    assert time1 < time2
    assert time1 <= time2
    assert time1 != time2
    assert not (time1 > time2)
    assert not (time1 >= time2)
    assert not (time1 == time2)


def test_sub():
    ts = 940_000_000
    delta = 100
    time1 = Time(ts)
    time2 = Time(ts + delta)

    assert (time2 - time1) == 100


def test_block_start():
    ts = 940_000_000
    result = Time(ts).block_ts(interval=Interval(3600))

    assert result == 939_999_600

    interval = Interval(3600) * 500

    ts = Time.from_string("2020-01-01 00:00")
    assert ts.block_ts(interval=interval) == Time.from_string("2019-12-20 00:00")


def test_str():
    dt = datetime.datetime(2000, 1, 2, 3, 4)
    result = Time.from_datetime(dt)

    assert str(result) == "2000-01-02 03:04"
