import datetime
from decimal import Decimal
from pathlib import Path

import numpy as np
import typer
from pandas import DataFrame
from typing import Optional

from cipher.strategy import Strategy
from cipher.models import Trade, Interval, Wallet, Time
from cipher.engine import Engine
from cipher.sources import BinanceFuturesOHLCSource
from cipher.services.data import DataService


app = typer.Typer()


@app.callback()
def callback():
    """Cipher - trading strategy backtester."""


class GoldenStrategy(Strategy):
    def process(self) -> DataFrame:
        df = self.datas.df
        df["sma200"] = df.ta.sma(length=200)
        df["ema50"] = df.ta.ema(length=50)

        difference = df["sma200"] - df["ema50"]

        cross = np.sign(difference.shift(1)) != np.sign(difference)

        df["entry"] = cross & np.sign(difference)

        return df

    def on_entry(self, row: dict) -> Optional[Trade]:
        print(row)
        return None


@app.command()
def run():
    source = BinanceFuturesOHLCSource(
        symbol="BTCUSDT", interval=Interval.from_binance_slug("1h")
    )

    data_service = DataService(cache_root=Path(__file__).parent / "../.cache")
    wallet = Wallet(assets={"usdt": Decimal(100), "btc": Decimal(0)})

    engine = Engine(
        sources=[source],
        data_service=data_service,
        strategy=GoldenStrategy(),
        wallet=wallet,
        start_ts=Time.from_datetime(datetime.datetime(2022, 1, 1)),
        stop_ts=Time.from_datetime(datetime.datetime(2022, 2, 1)),
    )

    engine.run()
