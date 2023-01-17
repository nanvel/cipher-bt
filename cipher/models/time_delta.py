import datetime
from functools import reduce


class TimeDelta(int):
    def to_timedelta(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=int(self))

    def __add__(self, other) -> "TimeDelta":
        return self.__class__(int(self) + other)

    def __truediv__(self, other: int) -> "TimeDelta":
        return self.__class__(int(self) // other)

    def __repr__(self):
        return f"{self.__class__.__name__}({int(self)})"

    def __str__(self):
        if not int(self):
            return "0s"

        minutes = self // 60
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
                        (int(self) % 60, "s"),
                    ],
                ),
            ),
            "",
        ).strip()
