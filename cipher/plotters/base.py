import datetime
import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Union

import pandas as pd

from ..models import Commission, Output, Wallet


logger = logging.getLogger(__name__)


class Plotter(ABC):
    OPTIONS = (
        "ohlc",
        "ohlcv",
        "signals",
        "sessions",
        "brackets",
        "balance",
        "position",
    )

    def __init__(
        self,
        output: Output,
        start: Union[int, datetime.datetime, None] = None,
        limit: Optional[int] = None,
        commission: Optional[Commission] = None,
    ):
        self.check_requirements()

        limit = limit or self.default_limit

        self.df = output.df

        if start is None:
            self.df = self.df.tail(limit)
        elif isinstance(start, int):
            if start == 0:
                self.df = self.df.head(limit)
            elif start < 0:
                first = len(self.df.index) + start
                self.df = self.df.iloc[first : first + limit]
            else:
                self.df = self.df.iloc[start : start + limit]
        elif isinstance(start, datetime.datetime):
            self.df = self.df.loc[start:].head(limit)

        self.start_ts = self.df.index[0]
        self.stop_ts = self.df.index[-1]

        self.signals = output.signals
        self.sessions = output.sessions.closed_sessions.filter(
            lambda s: s.opened_ts.to_datetime() >= self.start_ts
            and s.closed_ts.to_datetime() <= self.stop_ts
        )
        self.commission = commission

        self.title = output.title

        if len(self.df) != len(output.df):
            logger.warning(
                "Only a part of the dataframe is shown on the plot, use start/limit plot arguments to paginate"
            )

    @classmethod
    @abstractmethod
    def check_requirements(cls):
        """The if required libraries are installed."""
        pass

    @abstractmethod
    def run(self, rows: list):
        pass

    @property
    def default_limit(self) -> int:
        return 500

    def suggest_indicators(self) -> List[str]:
        """Float columns where median value falls into proces range."""
        exclude = {"open", "close", "high", "low", "volume"}

        min_low = self.df["low"].min()
        max_high = self.df["high"].max()

        result = []
        for column in self.df.columns:
            if column in exclude:
                continue

            if self.df.dtypes[column] != "float64":
                continue

            if min_low < self.df[column].median() < max_high:
                result.append(column)

        return result

    def build_signal_df(self, signal, value=1):
        return self.df[signal].replace({True: value, False: None})

    def build_position_df(self):
        col = "_position"
        self.df[col] = pd.Series(dtype="float64")
        self.df.at[self.start_ts, col] = 0

        wallet = Wallet()

        for transaction in self.sessions.transactions:
            wallet.apply(transaction, commission=self.commission)
            self.df.at[transaction.ts.to_datetime(), col] = float(wallet.base)

        self.df[col] = self.df[col].fillna(method="ffill")

        df = self.df[col]

        self.df = self.df.drop([col], axis=1)

        return df

    def build_quote_df(self):
        col = "_quote"
        self.df[col] = pd.Series(dtype="float64")
        self.df.at[self.start_ts, col] = 0

        wallet = Wallet()

        for transaction in self.sessions.transactions:
            wallet.apply(transaction, commission=self.commission)
            self.df.at[transaction.ts.to_datetime(), col] = float(wallet.quote)

        self.df[col] = self.df[col].fillna(method="ffill")

        df = self.df[col]

        self.df = self.df.drop([col], axis=1)

        return df

    def build_balance_df(self):
        position = self.build_position_df()
        quote = self.build_quote_df()

        return position * self.df["close"] + quote

    def build_sessions_df(self):
        long_open = "_long_session_open"
        long_close = "_long_session_close"
        short_open = "_short_session_open"
        short_close = "_short_session_close"

        self.df[long_open] = pd.Series(dtype="float64")
        self.df[long_close] = pd.Series(dtype="float64")
        self.df[short_open] = pd.Series(dtype="float64")
        self.df[short_close] = pd.Series(dtype="float64")

        for session in self.sessions:
            opened_ts = session.opened_ts.to_datetime()
            if session.is_long:
                self.df.at[opened_ts, long_open] = float(session.transactions[0].price)
            else:
                self.df.at[opened_ts, short_open] = float(session.transactions[0].price)

            close_ts = session.closed_ts.to_datetime()
            if session.is_long:
                self.df.at[close_ts, long_close] = float(session.transactions[-1].price)
            else:
                self.df.at[close_ts, short_close] = float(
                    session.transactions[-1].price
                )

        result = (
            self.df[long_open],
            self.df[long_close],
            self.df[short_open],
            self.df[short_close],
        )

        self.df = self.df.drop([long_open, long_close, short_open, short_close], axis=1)

        return result

    def build_brackets_df(self):
        sl_col = "_brackets_sl"
        tp_col = "_brackets_tp"

        self.df[sl_col] = pd.Series(dtype="float64")
        self.df[tp_col] = pd.Series(dtype="float64")
        for session in self.sessions:
            ts = session.closed_ts.to_datetime()

            if session.stop_loss:
                self.df.at[ts, sl_col] = float(session.stop_loss)
            if session.take_profit:
                self.df.at[ts, tp_col] = float(session.take_profit)

        result = (self.df[sl_col], self.df[tp_col])

        self.df = self.df.drop([sl_col, tp_col], axis=1)

        return result
