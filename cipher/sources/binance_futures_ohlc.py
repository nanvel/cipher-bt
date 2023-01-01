import csv
from pathlib import Path
from urllib.parse import urlencode, urljoin

import requests

from ..models import Interval, Time
from .base import Source


class BinanceFuturesOHLCSource(Source):
    base_url = "https://fapi.binance.com/fapi/"
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
        "take_buy_base_volume",
        "taker_buy_quote_volume",
    ]

    def __init__(self, symbol: str, interval: Interval):
        self.symbol = symbol
        self.interval = interval

    @property
    def slug(self):
        return f"binance_futures_ohlc/{self.symbol.lower()}_{self.interval.to_binance_slug()}"

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        """query: start_ts, interval, symbol"""
        start_ts = ts.block_ts(self.interval * self.limit)

        rows = self._request(
            uri="/fapi/v1/klines",
            data={
                "symbol": self.symbol,
                "interval": self.interval.to_binance_slug(),
                "limit": self.limit,
                "startTime": start_ts.to_timestamp(),
            },
        )

        self._write(rows, path=path)

        return (
            Time.from_timestamp(rows[0][0]),
            Time.from_timestamp(rows[-1][0]),
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

        response = requests.get(url)
        return response.json()
