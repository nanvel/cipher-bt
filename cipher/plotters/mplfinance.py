from typing import Optional

import mplfinance as mpf

from ..utils import create_palette
from .base import Plotter


class MPLFinancePlotter(Plotter):
    """https://github.com/matplotlib/mplfinance/blob/master/examples/addplot.ipynb"""

    @property
    def default_limit(self) -> int:
        return 200

    def run(self, rows: Optional[list] = None):
        if not self._ohlc_supported():
            return

        rows = self._filter_rows(
            rows or [["ohlc", "sessions"], ["balance", "position"]]
        )

        ap = []

        if self._signals_supported() and len(rows) > 1 and "signals" in rows[1]:
            palette = create_palette(len(self.signals) + 2)
            for n, signal in enumerate(self.signals):
                ap.append(
                    mpf.make_addplot(
                        self.build_signal_df(signal=signal, value=n + 1),
                        type="scatter",
                        marker="o",
                        panel=1,
                        color=palette[n],
                        secondary_y=False,
                    )  # markersize=200
                )

        palette = iter(create_palette(1 if len(rows) == 1 else len(rows[1])))

        if self._position_supported() and len(rows) > 1 and "position" in rows[1]:
            ap.append(
                mpf.make_addplot(self.build_position_df(), panel=1, color=next(palette))
            )

        if self._balance_supported() and len(rows) > 1 and "balance" in rows[1]:
            ap.append(
                mpf.make_addplot(self.build_balance_df(), panel=1, color=next(palette))
            )

        if self._sessions_supported() and "sessions" in rows[0]:
            long_open, long_close, short_open, short_close = self.build_sessions_df()

            if long_open[long_open.notnull()].size:
                ap.append(
                    mpf.make_addplot(
                        long_open,
                        type="scatter",
                        marker=">",
                        color="green",
                    )
                )
            if long_close[long_close.notnull()].size:
                ap.append(
                    mpf.make_addplot(
                        long_close,
                        type="scatter",
                        marker="<",
                        color="green",
                    )
                )
            if short_open[short_open.notnull()].size:
                ap.append(
                    mpf.make_addplot(
                        short_open,
                        type="scatter",
                        marker=">",
                        color="red",
                    )
                )
            if short_close[short_close.notnull()].size:
                ap.append(
                    mpf.make_addplot(
                        short_close,
                        type="scatter",
                        marker="<",
                        color="red",
                    )
                )

        if self._brackets_supported() and "brackets" in rows[0]:
            sl, tp = self.build_brackets_df()

            if sl[sl.notnull()].size:
                ap.append(
                    mpf.make_addplot(
                        sl,
                        type="scatter",
                        marker="+",
                        color="red",
                    )
                )

            if tp[tp.notnull()].size:
                ap.append(
                    mpf.make_addplot(
                        tp,
                        type="scatter",
                        marker="+",
                        color="green",
                    )
                )

        if "ohlcv" in rows[0] and self._ohlcv_supported():
            mpf.plot(self.df, type="candle", volume=True, addplot=ap)
        else:
            mpf.plot(self.df, type="candle", volume=False, addplot=ap)

    def _filter_rows(self, rows: list) -> list:
        columns = set(self.df.columns)
        result = []
        for n, rr in enumerate(rows):
            new_rr = []
            for r in rr:
                if r in {"ohlc", "ohlcv", "brackets", "sessions"} and n != 0:
                    continue
                if r in self.OPTIONS and getattr(self, f"_{r}_supported")():
                    new_rr.append(r)
                elif r in columns:
                    new_rr.append(r)
            if new_rr:
                result.append(new_rr)
        return result[:2]

    def _ohlc_supported(self):
        return {"open", "close", "high", "low"}.issubset(set(self.df.columns))

    def _ohlcv_supported(self):
        return {"open", "close", "high", "low", "volume"}.issubset(set(self.df.columns))

    def _signals_supported(self):
        return bool(self.signals)

    def _position_supported(self):
        return bool(self.sessions)

    def _balance_supported(self):
        return bool(self.sessions) and {"close"}.issubset(set(self.df.columns))

    def _sessions_supported(self):
        return bool(self.sessions)

    def _brackets_supported(self):
        return bool(self.sessions)