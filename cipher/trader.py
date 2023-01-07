import inspect
from typing import List

from .models import Datas, Session, Sessions, Tick, Time, Wallet
from .services.data import DataService
from .sources import Source
from .strategy import Strategy


class Trader:
    def __init__(
        self,
        data_service: DataService,
        sources: List[Source],
        strategy: Strategy,
        start_ts: Time,
        stop_ts: Time,
    ):
        self.sources = sources
        self.data_service = data_service
        self.start_ts = start_ts
        self.stop_ts = stop_ts
        self.strategy = strategy
        self.sessions = Sessions()
        self.wallet = Wallet()
        self.strategy.wallet = self.wallet

    def run(self):
        datas = Datas(
            self.data_service.load_df(
                source=s, start_ts=self.start_ts, stop_ts=self.stop_ts
            )
            for s in self.sources
        )

        self.strategy.datas = datas

        tick = Tick.init()

        df = self.strategy.process()

        for ts, row in df.iterrows():
            row_dict = dict(row)
            tick.ts = row_dict["ts"] = Time.from_datetime(ts)
            tick.price = row["close"]

            lower_price, upper_price = self.sessions.prices_of_interest()
            if (lower_price and row["low"] < lower_price) or (
                upper_price and row["high"] > upper_price
            ):
                for session in self.sessions.open_sessions:
                    take_profit, stop_loss = session.check(
                        low=row["low"], high=row["high"]
                    )
                    if take_profit:
                        self.strategy.on_take_profit(row=row_dict, session=session)
                    if stop_loss:
                        self.strategy.on_stop_loss(row=row_dict, session=session)

            if row["entry"]:
                new_session = Session(tick=tick, wallet=self.strategy.wallet)
                self.strategy.on_entry(row=row_dict, session=new_session)
                if new_session.position != 0:
                    self.sessions += new_session

            signal = self._find_signal_handlers()
            for signal in signals:
                if row[signal]:
                    for session in self.sessions.open_sessions:
                        getattr(self.strategy, f"on_{signal}")(row=row, session=session)

        return df

    def _find_signal_handlers(self) -> List[str]:
        skip_handler = {"on_take_profit", "on_stop_loss", "on_stop"}

        handlers = []
        for key, _ in inspect.getmembers(self.strategy.__class__):
            if key.startswith("on_") and key not in skip_handler:
                handlers.append(key[3:])

        return handlers
