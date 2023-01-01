import datetime

from pydantic import BaseModel

from .time_delta import TimeDelta


class Time(BaseModel):
    ts: int

    def to_datetime(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self.ts * 1.0 / 1000)

    def to_timestamp(self) -> int:
        return self.ts

    @classmethod
    def from_timestamp(cls, ts: int) -> "Time":
        return cls(ts=ts)

    @classmethod
    def from_datetime(cls, dt: datetime.datetime) -> "Time":
        return cls(
            ts=round(dt.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000)
        )

    def __sub__(self, other: "Time") -> TimeDelta:
        return TimeDelta(seconds=self.ts - other.ts)

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
