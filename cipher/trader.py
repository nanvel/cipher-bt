import inspect
from re import finditer
from typing import List

from .models import Cursor, Datas, Output, Session, Sessions, Time, Wallet
from .strategy import Strategy


class Trader:
    def __init__(self, datas: Datas, strategy: Strategy):
        self.datas = datas
        self.strategy = strategy

    def run(self) -> Output:
        self.strategy.datas = self.datas
        self.strategy.wallet = Wallet()

        sessions = Sessions()
        cursor = Cursor()

        df = self.strategy.process()
        signals = self._extract_strategy_signal_handlers()

        row_dict = {}
        for ts, row in df.iterrows():
            row_dict = dict(row)
            cursor.ts = row_dict["ts"] = Time.from_datetime(ts)
            cursor.price = row["close"]

            lower_price, upper_price = sessions.closest_sl_tp()
            if (lower_price and row["low"] < lower_price) or (
                upper_price and row["high"] > upper_price
            ):
                for session in sessions.open_sessions:
                    take_profit, stop_loss = session.check(
                        low=row["low"], high=row["high"]
                    )
                    if take_profit:
                        self.strategy.on_take_profit(row=row_dict, session=session)
                    if stop_loss:
                        self.strategy.on_stop_loss(row=row_dict, session=session)

            if row["entry"]:
                new_session = Session(cursor=cursor, wallet=self.strategy.wallet)
                self.strategy.on_entry(row=row_dict, session=new_session)
                if new_session.position != 0:
                    sessions.append(new_session)

            for signal in signals:
                if row[signal]:
                    for session in sessions.open_sessions:
                        getattr(self.strategy, f"on_{signal}")(row=row, session=session)

        for session in sessions.open_sessions:
            self.strategy.on_stop(row=row_dict, session=session)

        return Output(
            df=df,
            sessions=sessions,
            signals=signals,
            title=self._extract_strategy_title(),
            description=self._extract_strategy_description(),
        )

    def _extract_strategy_signal_handlers(self) -> List[str]:
        skip_handler = {"on_take_profit", "on_stop_loss", "on_stop"}

        handlers = []
        for key, _ in inspect.getmembers(self.strategy.__class__):
            if key.startswith("on_") and key not in skip_handler:
                handlers.append(key[3:])

        return handlers

    def _extract_strategy_title(self) -> str:
        doc = self.strategy.__doc__ or ""
        lines = list(
            filter(lambda x: len(x), map(lambda i: i.strip(), doc.split("\n")))
        )

        if not lines:
            matches = finditer(
                r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)",
                self.strategy.__class__.__name__,
            )
            lines.append((" ".join([m.group(0) for m in matches])).title())

        return lines[0]

    def _extract_strategy_description(self) -> str:
        return "\n".join((self.strategy.__doc__ or "").split("\n")[1:]).strip() or None
