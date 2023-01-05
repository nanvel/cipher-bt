import sys
from typing import Union
from pathlib import Path

from .engine import Engine
from .models import Time
from .plotters import FinplotPlotter, OHLCPlotRow
from .services import DataService
from .sources import SOURCES
from .strategy import Strategy


class Cipher:
    def __init__(self):
        self.strategy = None
        self.sources = []
        self.sessions = None

        work_dir = Path(sys.argv[0]).resolve().parent

        self.data_service = DataService(cache_root=work_dir / ".cache")
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

    @property
    def stats(self):
        return None

    def plot(self, plotter=None):
        """TODO: default plotter by env and what is installed."""
        plotter = FinplotPlotter(rows=[[OHLCPlotRow(df=self.df)]])
        plotter.run()
