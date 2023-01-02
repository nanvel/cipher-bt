import datetime

from pydantic import BaseModel

from .interval import Interval
from .time_delta import TimeDelta


class Time(BaseModel):
    ts: int  # ms

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
