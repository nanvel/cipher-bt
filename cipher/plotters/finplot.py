import datetime

import finplot as fplt


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
        for n, signal in enumerate(self.signals):
            fplt.plot(
                self.df[signal][self.df[signal] == True].replace({True: n + 1}),
                ax=axes,
                color="#4a5",
                style="^",
                legend=signal,
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
