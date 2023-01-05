from typing import Union

from .container import Container
from .engine import Engine
from .models import Time
from .plotters import FinplotPlotter, OHLCPlotRow, SignalsPlotRow, IndicatorsPlotRow
from .sources import SOURCES
from .strategy import Strategy


class Cipher:
    def __init__(self):
        self.container = Container()

        self.strategy = None
        self.sources = []
        self.sessions = None
        self.signals = None

        self.data_service = self.container.data_service()
        self.df = None

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def add_source(self, source, **kwargs):
        self.sources.append(SOURCES[source](**kwargs))

    def run(self, start_ts: Union[Time, str], stop_ts: Union[Time, str], **kwargs):
        _engine = Engine(
            data_service=self.data_service,
            sources=self.sources,
            strategy=self.strategy,
            start_ts=Time.from_string(start_ts),
            stop_ts=Time.from_string(stop_ts),
        )

        self.df = _engine.run()
        self.sessions = _engine.sessions
        self.signals = _engine.signals

    @property
    def stats(self):
        return None

    def plot(self, plotter=None):
        """TODO: default plotter by env and what is installed."""
        plotter = FinplotPlotter(
            rows=[
                [
                    OHLCPlotRow(df=self.df, show_volume=False),
                    IndicatorsPlotRow(df=self.df, indicators=["sma200", "ema50"]),
                ],
                [SignalsPlotRow(df=self.df, signals=self.signals)],
            ]
        )
        plotter.run()
