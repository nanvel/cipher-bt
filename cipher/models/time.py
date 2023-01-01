import datetime
from typing import Union

from pydantic import BaseModel

from .interval import Interval
from .time_delta import TimeDelta


STRING_FORMATS = ("%Y-%m-%dT%H:%M", "%Y-%m-%d", "%Y-%m-%d %H:%M")


class Time(BaseModel):
    ts: int  # ms

    class Config:
        frozen = True

    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self.ts * 1.0 / 1000)

    def to_timestamp(self) -> int:
        return self.ts

    def block_ts(self, interval: Interval):
        interval_ms = interval.seconds * 1000
        return self.__class__(ts=(self.ts // interval_ms) * interval_ms)

    @classmethod
    def from_timestamp(cls, ts: int) -> "Time":
        return cls(ts=ts)

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> "Time":
        return cls(
            ts=round(dt.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
        )

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
        return TimeDelta(seconds=int((self.ts - other.ts) / 1000))

    def __add__(self, other: Interval):
        return self.__class__(ts=self.ts + other.seconds * 1000)

    def __lt__(self, other):
        return self.ts < other.ts

    def __le__(self, other):
        return self.ts <= other.ts

    def __eq__(self, other):
        return self.ts == other.ts

    def __ge__(self, other):
        return self.ts >= other.ts

    def __gt__(self, other):
        return self.ts > other.ts

    def __ne__(self, other):
        return self.ts != other.ts

    def __str__(self):
        return self.to_datetime().strftime("%Y-%m-%d %H:%M")
