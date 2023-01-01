from abc import ABC, abstractmethod
from typing import Optional

from pandas import DataFrame

from .models import Datas, Trade, Trades


class Strategy(ABC):
    datas: Datas
    trades: Trades

    # def __init__(self, param1, param2):
    #     self.param1 = param1
    #     self.param2 = param2

    @abstractmethod
    def process(self) -> DataFrame:
        pass

    @abstractmethod
    def on_entry(self, row: dict) -> Optional[Trade]:
        pass

    # def on_<signal>(self, row: dict, trade: Trade) -> None:
    #     pass

    def on_take_profit(self, row: dict, trade: Trade) -> None:
        trade.liquidate()

    def on_stop_loss(self, row: dict, trade: Trade) -> None:
        trade.liquidate()
