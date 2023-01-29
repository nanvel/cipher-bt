import inspect
import re
from typing import List, Optional

from pandas import BooleanDtype, DataFrame, isna, Series

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

        signals = self._extract_strategy_signal_handlers()

        df = self.strategy.compose()
        self._ensure_df_not_empty(df)
        self._ensure_df_entry(df)
        self._ensure_df_signals_type(df, signals=signals)
        self._cut_df_nulls(df)

        row_dict = {}
        for ts, row in df.iterrows():
            row_dict = dict(row)

            cursor.set(ts=ts, price=row_dict["close"])

            for session in sessions.open_sessions:
                if session.take_profit or session.stop_loss:
                    take_profit, stop_loss = session.should_tp_sl(
                        low=row_dict["low"], high=row_dict["high"]
                    )
                else:
                    continue

                if take_profit:
                    with cursor.patch_price(take_profit):
                        self.strategy.on_take_profit(row=row_dict, session=session)
                if stop_loss:
                    with cursor.patch_price(stop_loss):
                        self.strategy.on_stop_loss(row=row_dict, session=session)

            for signal in signals:
                if signal == "entry":
                    continue
                if isna(row[signal]) or not row[signal]:
                    continue
                for session in sessions.open_sessions:
                    getattr(self.strategy, f"on_{signal}")(row=row, session=session)

            if not isna(row["entry"]) and row["entry"]:
                new_session = SessionProxy(
                    Session(cursor=cursor, wallet=self.strategy.wallet),
                    wallet=self.strategy.wallet,
                    cursor=cursor,
                )
                self.strategy.on_entry(
                    row=row_dict,
                    session=new_session,
                )
                if new_session.position.value != 0:
                    sessions.append(new_session)

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

    def _ensure_df_not_empty(self, df: DataFrame):
        if len(df) == 0:
            raise ValueError("Dataframe is empty.")

    def _ensure_df_entry(self, df: DataFrame):
        if "entry" not in df.columns:
            df["entry"] = Series(None, dtype="boolean")

    def _ensure_df_signals_type(self, df: DataFrame, signals: List[str]):
        for signal in signals:
            if signal not in df.columns:
                raise ValueError(f"{signal} signal column is missing in the dataframe.")
            if isinstance(df[signal].dtype, BooleanDtype) or df[signal].dtype == "bool":
                continue
            raise ValueError(f"{signal} signal column type have to be boolean.")

    def _cut_df_nulls(self, df: DataFrame):
        if len(df) < 10:
            return

        indexes = []
        for column in df.columns:
            if not df[column].isnull().any():
                continue
            index = df[column].first_valid_index()
            if index is None or index == df.index[0] or index > df.index[len(df) // 2]:
                continue
            if not df[column][df.index > index].isnull().any():
                indexes.append(index)

        if indexes:
            df.drop(df.index[df.index < max(indexes)], inplace=True)
