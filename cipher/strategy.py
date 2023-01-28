from pandas import DataFrame

from .models import Datas, Wallet
from .proxies import SessionProxy as Session


class Strategy:
    datas: Datas
    wallet: Wallet

    # def __init__(self, param1, param2):
    #     self.param1 = param1
    #     self.param2 = param2

    def compose(self) -> DataFrame:
        return self.datas.df

    def on_entry(self, row: dict, session: Session) -> None:
        pass

    # def on_<signal>(self, row: dict, session: Session) -> None:
    #     pass

    def on_take_profit(self, row: dict, session: Session) -> None:
        session.position = 0

    def on_stop_loss(self, row: dict, session: Session) -> None:
        session.position = 0

    def on_stop(self, row: dict, session: Session) -> None:
        pass
