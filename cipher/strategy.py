import inspect
from abc import ABC, abstractmethod
from typing import List, Optional

from pandas import DataFrame

from .models import Datas, Trade, Trades, Wallet


class Strategy(ABC):
    datas: Datas
    trades: Trades
    wallet: Wallet

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

    @classmethod
    def find_signal_handlers(cls) -> List[str]:
        skip_handler = {"on_entry", "on_take_profit", "on_stop_loss"}

        handlers = []
        for key, _ in inspect.getmembers(cls):
            if key.startswith("on_") and key not in skip_handler:
                handlers.append(key[3:])

        return handlers
