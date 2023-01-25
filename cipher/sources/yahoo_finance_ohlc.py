import csv
from pathlib import Path
from typing import Union

try:
    import yfinance

    YFINANCE_INSTALLED = True
except ImportError:
    YFINANCE_INSTALLED = False

from ..models import Interval, Time
from .base import Source


class YahooFinanceOHLCSource(Source):
    limit = 500
    field_names = [
        "ts",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]

    def __init__(self, symbol: str, interval: Union[Interval, str]):
        if not YFINANCE_INSTALLED:
            raise RuntimeError("yfinance is not installed, run pip install yfinance")

        if isinstance(interval, str):
            self.interval = Interval.from_yfinance_slug(interval)
        else:
            self.interval = interval

        self.symbol = symbol

    @property
    def slug(self):
        return f"yahoo_finance_ohlc/{self.symbol.lower()}_{self.interval.to_yfinance_slug()}"

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        """query: start_ts, interval, symbol"""
        start_ts = ts.block_ts(self.interval * self.limit)

        yf_start = start_ts.to_datetime().isoformat()
        yf_stop = (start_ts + (self.interval * self.limit)).to_datetime().isoformat()

        if self.interval >= 3600 * 24:
            yf_start = yf_start.split("T")[0]
            yf_stop = yf_stop.split("T")[0]

        data = yfinance.download(
            self.symbol,
            start=yf_start,
            end=yf_stop,
        )

        self._write(data, path=path)

        return (
            Time.from_datetime(data.index[0]),
            Time.from_datetime(data.index[-1]),
            len(data) == self.limit,
        )

    def _write(self, data, path):
        with path.open("w") as f:
            writer = csv.writer(f)
            writer.writerow(self.field_names)
            for ts, row in data.iterrows():
                writer.writerow(
                    [
                        int(Time.from_datetime(ts)),
                        row["Open"],
                        row["High"],
                        row["Low"],
                        row["Close"],
                        row["Adj Close"],
                        row["Volume"],
                    ]
                )
