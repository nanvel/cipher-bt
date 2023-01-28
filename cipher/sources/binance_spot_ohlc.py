import csv
from pathlib import Path
from typing import Union
from urllib.parse import urlencode, urljoin

import requests

from ..models import Interval, Time
from ..utils import RateLimiter
from .base import Source


class BinanceSpotOHLCSource(Source):
    base_url = "https://api.binance.com/api/"
    limit = 500
    field_names = [
        "ts",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "close_time",
        "quote_volume",
        "trades_number",
        "taker_buy_base_volume",
        "taker_buy_quote_volume",
    ]

    def __init__(self, symbol: str, interval: Union[Interval, str]):
        if isinstance(interval, str):
            self.interval = Interval.from_binance_slug(interval)
        else:
            self.interval = interval

        self.symbol = symbol

        self.rate_limiter = RateLimiter(calls_per_seconds=2.0)

    @property
    def slug(self):
        return (
            f"binance_spot_ohlc/{self.symbol.lower()}_{self.interval.to_binance_slug()}"
        )

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        """query: start_ts, interval, symbol"""
        start_ts = ts.block_ts(self.interval * self.limit)

        rows = self._request(
            uri="/api/v3/klines",
            data={
                "symbol": self.symbol,
                "interval": self.interval.to_binance_slug(),
                "limit": self.limit,
                "startTime": int(start_ts) * 1000,
            },
        )

        self._write(rows, path=path)

        return (
            Time(rows[0][0] // 1000),
            Time(rows[-1][0] // 1000),
            len(rows) == self.limit,
        )

    def _write(self, rows, path):
        with path.open("w") as f:
            writer = csv.writer(f)
            writer.writerow(self.field_names)
            for row in rows:
                writer.writerow([row[0] // 1000] + row[1 : len(self.field_names)])

    def _request(self, uri, data=None):
        data = data or {}
        data_str = urlencode(data)

        url = urljoin(self.base_url, uri)
        if data_str:
            url = "?".join([url, data_str])

        with self.rate_limiter.call():
            response = requests.get(url)

        assert response.status_code == 200, response.content

        return response.json()
