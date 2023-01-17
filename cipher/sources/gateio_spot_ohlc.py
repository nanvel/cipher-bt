import csv
import time
from pathlib import Path
from typing import Union
from urllib.parse import urlencode, urljoin

import requests

from ..models import Interval, Time
from .base import Source


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

        self._latest_request_time_ms = None

    @property
    def slug(self):
        return (
            f"gateio_spot_ohlc/{self.symbol.lower()}_{self.interval.to_gateio_slug()}"
        )

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        time_ms = int(time.monotonic() * 1000)
        if (
            self._latest_request_time_ms
            and time_ms - self._latest_request_time_ms < 200
        ):
            time.sleep(0.2)

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

        self._latest_request_time_ms = time_ms

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

        response = requests.get(
            url,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )

        assert response.status_code == 200, response.content

        return response.json()
