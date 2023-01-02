from typing import Optional

from pandas import DataFrame

from cipher.models import Trade
from cipher.strategy import Strategy


class SignalStrategy(Strategy):
    def process(self) -> DataFrame:
        return self.datas.df

    def on_entry(self, row: dict) -> Optional[Trade]:
        return None

    def on_something_else(self, row: dict, trade: Trade) -> None:
        pass


def test_signal_handlers():
    assert SignalStrategy().find_signal_handlers() == ["something_else"]
