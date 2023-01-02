from typing import List

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

        signals = self.strategy.find_signal_handlers()

        df = self.strategy.process()
        lower_price, upper_price = None, None

        for ts, row in df.iterrows():
            row_dict = dict(row)
            if row["entry"]:
                self.strategy.on_entry(row=row_dict)
            lower_price, upper_price = trades.prices_of_interest(row.close)

    def _signal_methods(self):
        pass
