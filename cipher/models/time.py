import datetime
from typing import Union

from .interval import Interval
from .time_delta import TimeDelta


STRING_FORMATS = ("%Y-%m-%dT%H:%M", "%Y-%m-%d", "%Y-%m-%d %H:%M")


class Time(int):
    def __new__(cls, value):
        value = int(value)
        if value < 0:
            raise ValueError("Seconds since January 1, 1970.")
        return super(cls, cls).__new__(cls, value)

    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(int(self))

    def block_ts(self, interval: Interval):
        return self.__class__(int(self) // interval * interval)

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> "Time":
        return cls(dt.replace(tzinfo=datetime.timezone.utc).timestamp())

    @classmethod
    def from_string(cls, s: Union[str, datetime.datetime]):
        if isinstance(s, datetime.datetime):
            return cls.from_datetime(s)
        for string_format in STRING_FORMATS:
            try:
                dt = datetime.datetime.strptime(s, string_format)
            except ValueError:
                continue
            return cls.from_datetime(dt)
        raise ValueError("Invalid datetime format.")

    def __sub__(self, other: "Time") -> TimeDelta:
        return TimeDelta(int(self) - other)

    def __add__(self, other: Union[Interval, TimeDelta]):
        return self.__class__(int(self) + other)

    def __str__(self) -> str:
        return self.to_datetime().strftime("%Y-%m-%d %H:%M")

    def __repr__(self):
        return f"{self.__class__.__name__}({int(self)})"
