import colorsys
import datetime

import finplot as fplt


def create_palette(n):
    hsv_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples)

    return [
        "#{:02x}{:02x}{:02x}".format(*[int(i * 255) for i in t]) for t in rgb_tuples
    ]


class PlotRow:
    pass


class OHLCPlotRow(PlotRow):
    def __init__(self, df, show_volume=False):
        # TODO: check if all rows that required are present
        self.df = df
        self.show_volume = show_volume

    def plot(self, axes):
        fplt.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=axes)
        if self.show_volume:
            fplt.volume_ocv(self.df[["open", "close", "volume"]], ax=axes.overlay())


class SignalsPlotRow(PlotRow):
    def __init__(self, df, signals):
        self.df = df
        self.signals = signals

    def plot(self, axes):
        palette = create_palette(len(self.signals) + 2)
        for n, signal in enumerate(self.signals):
            fplt.plot(
                self.df[signal].replace({True: n + 1, False: None}),
                ax=axes,
                color=palette[n],
                style="o",
                legend=signal,
            )


class IndicatorsPlotRow(PlotRow):
    def __init__(self, df, indicators):
        self.df = df
        self.indicators = indicators

    def plot(self, axes):
        for n, indicator in enumerate(self.indicators):
            fplt.plot(
                self.df[indicator],
                ax=axes,
                legend=indicator,
            )


class FinplotPlotter:
    def __init__(self, rows, title="Example"):
        self.rows = rows
        self.title = title

    def run(self):
        fplt.display_timezone = datetime.timezone.utc
        axs = fplt.create_plot(self.title, rows=len(self.rows))
        if len(self.rows) == 1:
            axs = [axs]

        for rows, ax in zip(self.rows, axs):
            for row in rows:
                row.plot(axes=ax)

        fplt.show()
