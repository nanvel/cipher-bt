import csv
from pathlib import Path
from typing import Union
from urllib.parse import urlencode, urljoin

import requests

from ..models import Interval, Time
from ..utils import RateLimiter
from .base import Source


rate_limiter = RateLimiter(calls_per_seconds=2.0)


class GateioSpotOHLCSource(Source):
    base_url = "https://api.gateio.ws/api/v4/"
    limit = 500
    field_names = [
        "ts",
        "volume_quote",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    def __init__(self, symbol: str, interval: Union[Interval, str]):
        if isinstance(interval, str):
            self.interval = Interval.from_gateio_slug(interval)
        else:
            self.interval = interval

        self.symbol = symbol

    @property
    def slug(self):
        return (
            f"gateio_spot_ohlc/{self.symbol.lower()}_{self.interval.to_gateio_slug()}"
        )

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        start_ts = ts.block_ts(self.interval * self.limit)

        rows = self._request(
            uri="spot/candlesticks",
            data={
                "currency_pair": self.symbol,
                "interval": self.interval.to_binance_slug(),
                "limit": self.limit,
                "from": int(start_ts),
            },
        )
        assert isinstance(rows, list), rows

        self._write(rows, path=path)

        return (
            Time(rows[0][0]),
            Time(rows[-1][0]),
            len(rows) == self.limit,
        )

    def _write(self, rows, path):
        with path.open("w") as f:
            writer = csv.writer(f)
            writer.writerow(self.field_names)
            for row in rows:
                writer.writerow(row[: len(self.field_names)])

    def _request(self, uri, data=None):
        data = data or {}
        data_str = urlencode(data)

        url = urljoin(self.base_url, uri)
        if data_str:
            url = "?".join([url, data_str])

        with rate_limiter():
            response = requests.get(
                url,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
            )

        assert response.status_code == 200, response.content

        return response.json()
