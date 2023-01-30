import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Union

import pandas as pd

from ..models import Commission, Output, Time, Wallet


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
        start: Union[int, str, None] = None,
        limit: Optional[int] = None,
        commission: Optional[Commission] = None,
    ):
        self.check_requirements()

        self.output = output

        limit = limit or self.default_limit

        if start is None:
            start_i = len(output.df) - limit
        elif isinstance(start, int):
            if start == 0:
                start_i = 0
            elif start < 0:
                start_i = len(output.df) + start
            else:
                start_i = start
        elif isinstance(start, str):
            start = Time.from_string(start).to_datetime()
            start_i = len(output.df.index[output.df.index <= start])
        else:
            raise ValueError("Invalid start value.")

        if start_i > len(output.df):
            start_i = len(output.df) - limit
        if start_i < 0:
            start_i = 0

        self.commission = commission
        self.title = output.title
        self.signals = output.signals
        self.sessions = output.sessions.closed_sessions

        extras_df = output.df[[]]
        extras_df["base"] = self._build_asset_series(asset_name="base")
        extras_df["quote"] = self._build_asset_series(asset_name="quote")
        extras_df["balance"] = (
            extras_df["base"] * output.df["close"] + extras_df["quote"]
        )
        extras_df["sessions_long_open"] = self._build_session_series(is_long=True, is_open=True)
        extras_df["sessions_long_close"] = self._build_session_series(is_long=True, is_open=False)
        extras_df["sessions_short_open"] = self._build_session_series(is_long=False, is_open=True)
        extras_df["sessions_short_close"] = self._build_session_series(is_long=False, is_open=False)
        extras_df['stop_loss'] = self._build_brackets_series(bracket_name='stop_loss')
        extras_df['take_profit'] = self._build_brackets_series(bracket_name='take_profit')

        self.original_df = output.df.iloc[start_i: start_i + limit]
        self.extras_df = extras_df.iloc[start_i: start_i + limit]

        if len(self.original_df) != len(output.df):
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

        min_low = self.original_df["low"].min()
        max_high = self.original_df["high"].max()

        result = []
        for column in self.original_df.columns:
            if column in exclude:
                continue

            if self.original_df.dtypes[column] != "float64":
                continue

            if min_low < self.original_df[column].median() < max_high:
                result.append(column)

        return result

    def build_signal_df(self, signal, value=1):
        return self.original_df[signal].replace({True: value, False: None})

    def _build_asset_series(self, asset_name):
        df = self.output.df
        column_name = f"_asset_{asset_name}"

        df[column_name] = pd.Series(dtype="float64")
        df.at[df.index[0], column_name] = 0

        wallet = Wallet()

        for transaction in self.sessions.transactions:
            wallet.apply(transaction, commission=self.commission)
            df.at[transaction.ts.to_datetime(), column_name] = float(
                getattr(wallet, asset_name)
            )

        df[column_name] = df[column_name].fillna(method="ffill")

        result = df[column_name]

        df.drop([column_name], axis=1, inplace=True)

        return result

    def _build_session_series(self, is_long, is_open):
        df = self.output.df
        column_name = f"_sessions_{is_long}_{is_open}"

        df[column_name] = pd.Series(dtype="float64")

        for session in self.sessions:
            if is_open:
                opened_ts = session.opened_ts.to_datetime()
                if session.is_long and is_long:
                    df.at[opened_ts, column_name] = float(session.transactions[0].price)
                elif not session.is_long and not is_long:
                    df.at[opened_ts, column_name] = float(session.transactions[0].price)
            else:
                close_ts = session.closed_ts.to_datetime()
                if session.is_long and is_long:
                    df.at[close_ts, column_name] = float(session.transactions[-1].price)
                elif not session.is_long and not is_long:
                    df.at[close_ts, column_name] = float(
                        session.transactions[-1].price
                    )

        result = df[column_name]

        df.drop([column_name], axis=1, inplace=True)

        return result

    def _build_brackets_series(self, bracket_name):
        df = self.output.df
        column_name = f"_brackets_{bracket_name}"

        df[column_name] = pd.Series(dtype="float64")
        for session in self.sessions:
            ts = session.closed_ts.to_datetime()

            if getattr(session, bracket_name):
                df.at[ts, column_name] = float(getattr(session, bracket_name))

        result = df[column_name]

        df.drop([column_name], axis=1, inplace=True)

        return result
