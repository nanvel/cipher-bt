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

YFINANCE_INTERVALS = {
    "1m": 60,
    "2m": 60 * 2,
    "5m": 60 * 5,
    "15m": 60 * 15,
    "30m": 60 * 30,
    "60m": 3600,
    "90m": 60 * 90,
    "1h": 3600,
    "1d": 3600 * 24,
    "5d": 3600 * 24 * 5,
    "1wk": 3600 * 24 * 7,
    "1mo": 3600 * 24 * 30,
    "3mo": 3600 * 24 * 90,
}

GATEIO_INTERVALS = {
    "10s": 10,
    "1m": 60,
    "5m": 60 * 5,
    "15m": 60 * 15,
    "30m": 60 * 30,
    "1h": 3600,
    "4h": 3600 * 4,
    "8h": 3600 * 8,
    "1d": 3600 * 24,
    "7d": 3600 * 24 * 7,
    "30d": 3600 * 24 * 30,
}


class Interval(BaseModel):
    seconds: int

    class Config:
        frozen = True

    def to_seconds(self) -> int:
        return self.seconds

    def to_binance_slug(self) -> str:
        return {v: k for k, v in BINANCE_INTERVALS.items()}[self.seconds]

    def to_yfinance_slug(self) -> str:
        return {v: k for k, v in YFINANCE_INTERVALS.items()}[self.seconds]

    def to_gateio_slug(self):
        return {v: k for k, v in GATEIO_INTERVALS.items()}[self.seconds]

    def to_slug(self) -> str:
        return self.to_binance_slug()

    @classmethod
    def from_binance_slug(cls, slug: str):
        return cls(seconds=BINANCE_INTERVALS[slug])

    @classmethod
    def from_yfinance_slug(cls, slug: str):
        return cls(seconds=YFINANCE_INTERVALS[slug])

    @classmethod
    def from_gateio_slug(cls, slug: str):
        return cls(seconds=GATEIO_INTERVALS[slug])

    @classmethod
    def from_seconds(cls, seconds: int):
        return cls(seconds=seconds)

    def __mul__(self, other: int) -> "Interval":
        return self.__class__(seconds=self.seconds * other)

    def __ge__(self, other: "Interval"):
        return self.seconds >= other.seconds
