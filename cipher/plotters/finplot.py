import datetime
from typing import Optional

try:
    import finplot

    FINPLOT_INSTALLED = True
except ImportError:
    FINPLOT_INSTALLED = False

from ..utils import create_palette
from .base import Plotter


class FinplotPlotter(Plotter):
    """Markers: https://matplotlib.org/stable/api/markers_api.html"""

    @property
    def default_limit(self) -> int:
        return 2000

    def run(self, rows: Optional[list] = None):
        assert FINPLOT_INSTALLED, "finplot is not installed"

        rows = self._filter_rows(
            rows
            or [
                ["ohlc", "sessions"] + self.suggest_indicators(),
                ["signals"],
                ["position"],
                ["balance"],
            ]
        )
        if not rows:
            return

        finplot.display_timezone = datetime.timezone.utc
        axs = finplot.create_plot(self.title, rows=len(rows))
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

    def _filter_rows(self, rows: list) -> list:
        columns = set(self.df.columns)
        result = []
        for rr in rows:
            new_rr = []
            for r in rr:
                if r in self.OPTIONS and getattr(self, f"_{r}_supported")():
                    new_rr.append(r)
                elif r in columns:
                    new_rr.append(r)
            if new_rr:
                result.append(new_rr)
        return result

    def _ohlc_supported(self):
        return {"open", "close", "high", "low"}.issubset(set(self.df.columns))

    def _ohlc(self, ax):
        finplot.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=ax)

    def _ohlcv_supported(self):
        return {"open", "close", "high", "low", "volume"}.issubset(set(self.df.columns))

    def _ohlcv(self, ax):
        finplot.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=ax)
        finplot.volume_ocv(self.df[["open", "close", "volume"]], ax=ax.overlay())

    def _signals_supported(self):
        return bool(self.signals)

    def _signals(self, ax):
        palette = create_palette(len(self.signals) + 2)
        for n, signal in enumerate(self.signals):
            finplot.plot(
                self.build_signal_df(signal=signal, value=n + 1),
                ax=ax,
                color=palette[n],
                style="o",
                legend=signal,
            )

    def _position_supported(self):
        return bool(self.sessions)

    def _position(self, ax):
        finplot.plot(
            self.build_position_df(),
            ax=ax,
            legend="Position",
        )

    def _balance_supported(self):
        return bool(self.sessions) and {"close"}.issubset(set(self.df.columns))

    def _balance(self, ax):
        finplot.plot(
            self.build_balance_df(),
            ax=ax,
            legend="Balance",
        )

    def _sessions_supported(self):
        return bool(self.sessions)

    def _sessions(self, ax):
        long_open, long_close, short_open, short_close = self.build_sessions_df()

        finplot.plot(
            long_open,
            ax=ax,
            style=">",
            legend="Long Open",
            color="green",
        )
        finplot.plot(
            long_close,
            ax=ax,
            style="<",
            legend="Long Close",
            color="green",
        )
        finplot.plot(
            short_open,
            ax=ax,
            style=">",
            legend="Short Open",
            color="red",
        )
        finplot.plot(
            short_close,
            ax=ax,
            style="<",
            legend="Shor Close",
            color="red",
        )

    def _brackets_supported(self):
        return bool(self.sessions)

    def _brackets(self, ax):
        sl, tp = self.build_brackets_df()

        finplot.plot(
            sl,
            ax=ax,
            style="+",
            legend="Stop loss",
            color="red",
        )
        finplot.plot(
            tp,
            ax=ax,
            style="+",
            legend="Take profit",
            color="green",
        )
