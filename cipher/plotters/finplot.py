import colorsys
import datetime
from typing import Optional

import finplot
import pandas

from ..models import Output, Wallet
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

    def __init__(self, output: Output):
        self.output = output

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
                elif row in self.output.df.columns:
                    finplot.plot(
                        self.output.df[row],
                        ax=ax,
                        legend=row,
                    )

        finplot.show()

    def _ohlc_supported(self):
        pass

    def _ohlc(self, ax):
        finplot.candlestick_ochl(
            self.output.df[["open", "close", "high", "low"]], ax=ax
        )

    def _ohlcv(self, ax):
        finplot.candlestick_ochl(
            self.output.df[["open", "close", "high", "low"]], ax=ax
        )
        finplot.volume_ocv(self.output.df[["open", "close", "volume"]], ax=ax.overlay())

    def _signals(self, ax):
        palette = create_palette(len(self.output.signals) + 2)
        for n, signal in enumerate(self.output.signals):
            finplot.plot(
                self.output.df[signal].replace({True: n + 1, False: None}),
                ax=ax,
                color=palette[n],
                style="o",
                legend=signal,
            )

    def _position(self, ax):
        self.output.df["position"] = None
        wallet = Wallet()

        self.output.df.at[self.output.df.index.min(), "position"] = 0
        for transaction in self.output.sessions.transactions:
            wallet.apply(transaction)
            self.output.df.at[transaction.ts.to_datetime(), "position"] = float(
                wallet.base
            )
        self.output.df["position"] = self.output.df["position"].fillna(method="ffill")

        finplot.plot(
            self.output.df["position"],
            ax=ax,
            legend="Position",
        )

    def _balance(self, ax):
        self.output.df["position"] = pandas.Series(dtype="float64")
        self.output.df["quote"] = pandas.Series(dtype="float64")
        wallet = Wallet()

        self.output.df.at[self.output.df.index.min(), "position"] = 0
        self.output.df.at[self.output.df.index.min(), "quote"] = 0
        for transaction in self.output.sessions.transactions:
            wallet.apply(transaction)
            self.output.df.at[transaction.ts.to_datetime(), "position"] = float(
                wallet.base
            )
            self.output.df.at[transaction.ts.to_datetime(), "quote"] = float(
                wallet.quote
            )

        self.output.df["position"] = self.output.df["position"].fillna(method="ffill")
        self.output.df["quote"] = self.output.df["quote"].fillna(method="ffill")

        finplot.plot(
            self.output.df["position"] * self.output.df["close"]
            + self.output.df["quote"],
            ax=ax,
            legend="Balance",
        )

    def _sessions(self, ax):
        self.output.df["long_session_open"] = pandas.Series(dtype="float64")
        self.output.df["long_session_close"] = pandas.Series(dtype="float64")
        self.output.df["short_session_open"] = pandas.Series(dtype="float64")
        self.output.df["short_session_close"] = pandas.Series(dtype="float64")

        for session in self.output.sessions:
            ts = session.opened_ts.to_datetime()

            if session.is_long:
                self.output.df.at[ts, "long_session_open"] = self.output.df.at[
                    ts, "close"
                ]
            else:
                self.output.df.at[ts, "short_session_open"] = self.output.df.at[
                    ts, "close"
                ]

            if session.is_closed:
                close_ts = session.closed_ts.to_datetime()
                if session.is_long:
                    self.output.df.at[
                        close_ts, "long_session_close"
                    ] = self.output.df.at[close_ts, "close"]
                else:
                    self.output.df.at[
                        close_ts, "short_session_close"
                    ] = self.output.df.at[close_ts, "close"]

        finplot.plot(
            self.output.df["long_session_open"],
            ax=ax,
            style="^",
            legend="Long Open",
            color="green",
        )
        finplot.plot(
            self.output.df["long_session_close"],
            ax=ax,
            style="v",
            legend="Long Close",
            color="green",
        )
        finplot.plot(
            self.output.df["short_session_open"],
            ax=ax,
            style="v",
            legend="Short Open",
            color="red",
        )
        finplot.plot(
            self.output.df["short_session_close"],
            ax=ax,
            style="^",
            legend="Shor Close",
            color="red",
        )

    def _brackets(self, ax):
        self.output.df["bracket_sl"] = pandas.Series(dtype="float64")
        self.output.df["bracket_tp"] = pandas.Series(dtype="float64")
        for session in self.output.sessions.closed_sessions:
            ts = session.closed_ts.to_datetime()

            if session.stop_loss:
                self.output.df.at[ts, "bracket_sl"] = float(session.stop_loss)
            if session.take_profit:
                self.output.df.at[ts, "bracket_tp"] = float(session.take_profit)

        finplot.plot(
            self.output.df["bracket_tp"],
            ax=ax,
            style="+",
            legend="Take profit",
            color="green",
        )

        finplot.plot(
            self.output.df["bracket_sl"],
            ax=ax,
            style="+",
            legend="Stop loss",
            color="red",
        )
