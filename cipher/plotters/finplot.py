import colorsys
import datetime
from typing import Optional

import finplot as fplt
from pandas import DataFrame

from .base import Plotter


def create_palette(n):
    hsv_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples)

    return [
        "#{:02x}{:02x}{:02x}".format(*[int(i * 255) for i in t]) for t in rgb_tuples
    ]


class FinplotPlotter(Plotter):
    OHLC = "ohlc"
    OHLCV = "ohlcv"
    SIGNALS = "signals"
    SESSIONS = "sessions"
    BRACKETS = "brackets"
    BALANCE = "balance"
    POSITIONS = "positions"

    def __init__(
        self, df: DataFrame, rows: Optional[list] = None, title: str = "Example"
    ):
        self.rows = rows or [
            [self.OHLC, self.SESSIONS],
            [self.SIGNALS],
            [self.SESSIONS],
            [self.BALANCE],
        ]
        self.title = title
        self.df = df

    def run(self):
        fplt.display_timezone = datetime.timezone.utc
        axs = fplt.create_plot(self.title, rows=len(self.rows))
        if len(self.rows) == 1:
            axs = [axs]

        for rows, ax in zip(self.rows, axs):
            for row in rows:
                method = getattr(self, f"_{row}", None)
                if method:
                    method(ax)
                elif row in self.df.columns:
                    fplt.plot(
                        self.df[row],
                        ax=ax,
                        legend=row,
                    )

        fplt.show()

    def _ohlc(self, ax):
        fplt.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=ax)

    def _ohlcv(self, ax):
        fplt.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=ax)
        fplt.volume_ocv(self.df[["open", "close", "volume"]], ax=ax.overlay())

    def _signals(self, ax):
        palette = create_palette(len(self.signals) + 2)
        for n, signal in enumerate(self.signals):
            fplt.plot(
                self.df[signal].replace({True: n + 1, False: None}),
                ax=ax,
                color=palette[n],
                style="o",
                legend=signal,
            )
