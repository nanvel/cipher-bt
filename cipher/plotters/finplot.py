import finplot as fplt


class PlotRow:
    pass


class OHLCPlotRow(PlotRow):
    def __init__(self, df):
        # TODO: check if all rows that required are present
        self.df = df

    def plot(self, axes):
        fplt.candlestick_ochl(self.df[["open", "close", "high", "low"]], ax=axes)


class FinplotPlotter:
    def __init__(self, rows, title="Example"):
        self.rows = rows
        self.title = title

    def run(self):
        axs = fplt.create_plot(self.title, rows=len(self.rows))
        if len(self.rows) == 1:
            axs = [axs]

        for rows, ax in zip(self.rows, axs):
            for row in rows:
                row.plot(axes=ax)

        fplt.show()
