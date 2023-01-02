from typing import List

from .factories.trade import TradeFactory
from .models import Datas, Time, Trades, Wallet
from .services.data import DataService
from .sources import Source
from .strategy import Strategy


class Engine:
    def __init__(
        self,
        data_service: DataService,
        sources: List[Source],
        strategy: Strategy,
        wallet: Wallet,
        start_ts: Time,
        stop_ts: Time,
    ):
        self.sources = sources
        self.data_service = data_service
        self.start_ts = start_ts
        self.stop_ts = stop_ts
        self.strategy = strategy
        self.wallet = wallet

    def run(self):
        datas = Datas(
            data_frames=[
                self.data_service.load_df(
                    source=s, start_ts=self.start_ts, stop_ts=self.stop_ts
                )
                for s in self.sources
            ]
        )

        trades = Trades()

        self.strategy.datas = datas
        self.strategy.trades = trades
        self.strategy.wallet = self.wallet
        self.strategy.trade_factory = TradeFactory()

        signals = self.strategy.find_signal_handlers()

        df = self.strategy.process()

        for ts, row in df.iterrows():
            row_dict = dict(row)
            row_dict["ts"] = ts

            lower_price, upper_price = trades.prices_of_interest(row.close)
            if (lower_price and row["low"] < lower_price) or (
                upper_price and row["high"] > upper_price
            ):
                for trade in trades.open_trades:
                    take_profit, stop_loss = trade.check(
                        low=row["low"], high=row["high"]
                    )
                    if take_profit:
                        self.strategy.on_take_profit(row=row_dict, trade=trade)
                    if stop_loss:
                        self.strategy.on_stop_loss(row=row_dict, trade=trade)

            if row["entry"]:
                self.strategy.on_entry(row=row_dict)

            for signal in signals:
                if row[signal]:
                    for trade in trades.open_trades():
                        getattr(self.strategy, f"on_{signal}")(row=row, trade=trade)

    def _signal_methods(self):
        pass
