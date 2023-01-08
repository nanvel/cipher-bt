import colorsys
import datetime
from typing import Optional, Union

import finplot
import pandas

from ..models import Output, Sessions, Wallet
from .base import Plotter


def create_palette(n):
    hsv_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples)

    return [
        "#{:02x}{:02x}{:02x}".format(*[int(i * 255) for i in t]) for t in rgb_tuples
    ]


class FinplotPlotter(Plotter):
    """Markers: https://matplotlib.org/stable/api/markers_api.html"""

    OHLC = "ohlc"
    OHLCV = "ohlcv"
    SIGNALS = "signals"
    SESSIONS = "sessions"
    BRACKETS = "brackets"
    BALANCE = "balance"
    POSITION = "position"

    def __init__(
        self,
        output: Output,
        start: Union[int, datetime.datetime, None] = None,
        limit: Optional[int] = None,
    ):
        limit = limit or 500
        self.output = output

        self.df = self.output.df

        if start is None:
            self.df = self.df.tail(limit)
        elif isinstance(start, int):
            if start == 0:
                self.df = self.df.head(limit)
            else:
                self.df = self.df.iloc[start : start + limit]
        elif isinstance(start, datetime.datetime):
            self.df = self.df.loc[start:].head(limit)

        self.start_ts = self.df.index[0]
        self.stop_ts = self.df.index[-1]

    def run(self, rows: Optional[list] = None):
        rows = rows or [
            [self.OHLC, self.SESSIONS],
            [self.SIGNALS],
            [self.POSITION],
            [self.BALANCE],
        ]

        finplot.display_timezone = datetime.timezone.utc
        axs = finplot.create_plot(self.output.title, rows=len(rows))
        if len(rows) == 1:
            axs = [axs]

        for rows, ax in zip(rows, axs):
            for row in rows:
                method = getattr(self, f"_{row}", None)
                if method:
                    method(ax)
                elif row in self.df.columns:
                    finplot.plot(
                        self.df[row],
                        ax=ax,
                        legend=row,
                    )

        finplot.show()

    def _ohlc_supported(self):
        pass

    def _ohlc(self, ax):
        finplot.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=ax)

    def _ohlcv(self, ax):
        finplot.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=ax)
        finplot.volume_ocv(self.df[["open", "close", "volume"]], ax=ax.overlay())

    def _signals(self, ax):
        palette = create_palette(len(self.output.signals) + 2)
        for n, signal in enumerate(self.output.signals):
            finplot.plot(
                self.df[signal].replace({True: n + 1, False: None}),
                ax=ax,
                color=palette[n],
                style="o",
                legend=signal,
            )

    def _position(self, ax):
        self.df["position"] = None
        wallet = Wallet()

        self.df.at[self.start_ts, "position"] = 0
        sessions = Sessions(
            [
                s
                for s in self.output.sessions
                if self.start_ts < s.opened_ts.to_datetime() < self.stop_ts
            ]
        )

        for transaction in sessions.transactions:
            ts = transaction.ts.to_datetime()
            if ts > self.stop_ts:
                continue

            wallet.apply(transaction)
            self.df.at[ts, "position"] = float(wallet.base)
        self.df["position"] = self.df["position"].fillna(method="ffill")

        finplot.plot(
            self.df["position"],
            ax=ax,
            legend="Position",
        )

    def _balance(self, ax):
        self.df["position"] = pandas.Series(dtype="float64")
        self.df["quote"] = pandas.Series(dtype="float64")
        wallet = Wallet()

        self.df.at[self.start_ts, "position"] = 0
        self.df.at[self.start_ts, "quote"] = 0

        sessions = Sessions(
            [
                s
                for s in self.output.sessions
                if self.start_ts < s.opened_ts.to_datetime() < self.stop_ts
            ]
        )

        for transaction in sessions.transactions:
            ts = transaction.ts.to_datetime()

            if ts > self.stop_ts:
                continue

            wallet.apply(transaction)
            self.df.at[ts, "position"] = float(wallet.base)
            self.df.at[ts, "quote"] = float(wallet.quote)

        self.df["position"] = self.df["position"].fillna(method="ffill")
        self.df["quote"] = self.df["quote"].fillna(method="ffill")

        finplot.plot(
            self.df["position"] * self.df["close"] + self.df["quote"],
            ax=ax,
            legend="Balance",
        )

    def _sessions(self, ax):
        self.df["long_session_open"] = pandas.Series(dtype="float64")
        self.df["long_session_close"] = pandas.Series(dtype="float64")
        self.df["short_session_open"] = pandas.Series(dtype="float64")
        self.df["short_session_close"] = pandas.Series(dtype="float64")

        for session in self.output.sessions:
            ts = session.opened_ts.to_datetime()

            if ts < self.start_ts or ts > self.stop_ts:
                continue

            if session.is_long:
                self.df.at[ts, "long_session_open"] = self.df.at[ts, "close"]
            else:
                self.df.at[ts, "short_session_open"] = self.df.at[ts, "close"]

            if session.is_closed:
                close_ts = session.closed_ts.to_datetime()
                if session.is_long:
                    self.df.at[close_ts, "long_session_close"] = self.df.at[
                        close_ts, "close"
                    ]
                else:
                    self.df.at[close_ts, "short_session_close"] = self.df.at[
                        close_ts, "close"
                    ]

        finplot.plot(
            self.df["long_session_open"],
            ax=ax,
            style=">",
            legend="Long Open",
            color="green",
        )
        finplot.plot(
            self.df["long_session_close"],
            ax=ax,
            style="<",
            legend="Long Close",
            color="green",
        )
        finplot.plot(
            self.df["short_session_open"],
            ax=ax,
            style=">",
            legend="Short Open",
            color="red",
        )
        finplot.plot(
            self.df["short_session_close"],
            ax=ax,
            style="<",
            legend="Shor Close",
            color="red",
        )

    def _brackets(self, ax):
        self.df["bracket_sl"] = pandas.Series(dtype="float64")
        self.df["bracket_tp"] = pandas.Series(dtype="float64")
        for session in self.output.sessions.closed_sessions:
            if session.opened_ts.to_datetime() < self.start_ts:
                continue
            if session.closed_ts.to_datetime() > self.stop_ts:
                continue

            ts = session.closed_ts.to_datetime()

            if session.stop_loss:
                self.df.at[ts, "bracket_sl"] = float(session.stop_loss)
            if session.take_profit:
                self.df.at[ts, "bracket_tp"] = float(session.take_profit)

        finplot.plot(
            self.df["bracket_tp"],
            ax=ax,
            style="+",
            legend="Take profit",
            color="green",
        )

        finplot.plot(
            self.df["bracket_sl"],
            ax=ax,
            style="+",
            legend="Stop loss",
            color="red",
        )
