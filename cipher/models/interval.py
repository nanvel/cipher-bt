from pydantic import BaseModel


BINANCE_INTERVALS = {
    "1m": 60,
    "3m": 60 * 3,
    "5m": 60 * 5,
    "15m": 60 * 15,
    "30m": 60 * 30,
    "1h": 3600,
    "2h": 3600 * 2,
    "4h": 3600 * 4,
    "6h": 3600 * 6,
    "8h": 3600 * 8,
    "12h": 3600 * 12,
    "1d": 3600 * 24,
    "3d": 3600 * 24 * 3,
    "1w": 3600 * 24 * 7,
}


class Interval(BaseModel):
    seconds: int

    class Config:
        frozen = True

    def to_seconds(self) -> int:
        return self.seconds

    def to_binance_slug(self) -> str:
        return {v: k for k, v in BINANCE_INTERVALS.items()}[self.seconds]

    def to_slug(self) -> str:
        return self.to_binance_slug()

    @classmethod
    def from_binance_slug(cls, slug: str):
        return cls(seconds=BINANCE_INTERVALS[slug])

    @classmethod
    def from_seconds(cls, seconds: int):
        return cls(seconds=seconds)

    def __mul__(self, other: int) -> "Interval":
        return self.__class__(seconds=self.seconds * other)
