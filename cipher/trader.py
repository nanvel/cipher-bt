import inspect
import re
from typing import List, Optional

from .models import Cursor, Datas, Output, Session, Sessions, Wallet
from .proxies import SessionProxy
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

            cursor.set(ts=ts, price=row_dict["close"])

            for session in sessions.open_sessions:
                take_profit, stop_loss = session.should_tp_sl(
                    low=row_dict["low"], high=row_dict["high"]
                )
                if take_profit:
                    with cursor.patch_price(take_profit):
                        self.strategy.on_take_profit(row=row_dict, session=session)
                if stop_loss:
                    with cursor.patch_price(stop_loss):
                        self.strategy.on_stop_loss(row=row_dict, session=session)

            for signal in signals:
                if not row[signal]:
                    continue
                if signal == "entry":
                    new_session = SessionProxy(
                        Session(cursor=cursor, wallet=self.strategy.wallet),
                        wallet=self.strategy.wallet,
                        cursor=cursor,
                    )
                    self.strategy.on_entry(
                        row=row_dict,
                        session=new_session,
                    )
                    if new_session.position != 0:
                        sessions.append(new_session)
                else:
                    for session in sessions.open_sessions:
                        getattr(self.strategy, f"on_{signal}")(row=row, session=session)

        for session in sessions.open_sessions:
            self.strategy.on_stop(row=row_dict, session=session)

        return Output(
            df=df,
            sessions=Sessions(s.session for s in sessions),
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
            matches = re.finditer(
                r".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)",
                self.strategy.__class__.__name__,
            )
            lines.append((" ".join([m.group(0) for m in matches])).title())

        return lines[0]

    def _extract_strategy_description(self) -> Optional[str]:
        spaces_re = re.compile(r"\s+")
        description = "\n".join(
            map(
                lambda i: spaces_re.sub(" ", i).strip(),
                (self.strategy.__doc__ or "").split("\n")[1:],
            )
        )
        return description.strip() or None
