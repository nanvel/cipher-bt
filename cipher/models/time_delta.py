import datetime
from functools import reduce

from pydantic import BaseModel


class TimeDelta(BaseModel):
    seconds: int

    class Config:
        frozen = True

    def to_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self.seconds)

    def to_seconds(self) -> int:
        return self.seconds

    def __gt__(self, other) -> bool:
        return self.seconds > other.seconds

    def __add__(self, other) -> "TimeDelta":
        return self.__class__(seconds=self.seconds + other.seconds)

    def __truediv__(self, other: int) -> "TimeDelta":
        return self.__class__(seconds=self.seconds // other)

    def __str__(self):
        if not self.seconds:
            return "0s"

        minutes = self.seconds // 60
        hours = minutes // 60
        days = hours // 24
        return reduce(
            lambda a, b: f"{a} {b}",
            map(
                lambda c: str(c[0]) + c[1],
                filter(
                    lambda d: d[0] != 0,
                    [
                        (days, "d"),
                        (hours % 24, "h"),
                        (minutes % 60, "m"),
                        (self.seconds % 60, "s"),
                    ],
                ),
            ),
            "",
        ).strip()
