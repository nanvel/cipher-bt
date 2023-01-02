import datetime

from pydantic import BaseModel


class TimeDelta(BaseModel):
    seconds: int

    def to_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.seconds)

    def to_seconds(self) -> int:
        return self.seconds

    def __truediv__(self, other: int) -> "TimeDelta":
        return self.__class__(seconds=self.seconds // other)
