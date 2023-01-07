from decimal import Decimal
from typing import List, Optional, Union

from .container import Container
from .models import Commission, Datas, Output, SimpleCommission, Time
from .plotters import FinplotPlotter
from .sources import Source, SOURCES
from .strategy import Strategy
from .trader import Trader
from .values import Percent


class Cipher:
    def __init__(self, **settings):
        self.container = Container()
        self.container.config.from_dict(settings)

        self.strategy: Optional[Strategy] = None
        self.sources: List[Source] = []
        self.output: Optional[Output] = None
        self.commission: Optional[Commission] = None

        self.data_service = self.container.data_service()
        self.df = None

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def add_source(self, source: Union[Source, str], **kwargs):
        if isinstance(source, Source):
            self.sources.append(source)
        else:
            self.sources.append(SOURCES[source](**kwargs))

    def add_commission(self, value: Union[Commission, Decimal, str, Percent]):
        if isinstance(value, Commission):
            self.commission = value
        else:
            self.commission = SimpleCommission(value=value)

    def run(self, start_ts: Union[Time, str], stop_ts: Union[Time, str]):
        assert self.strategy
        assert self.sources

        self.output = Trader(
            datas=Datas(
                self.data_service.load_df(
                    source=s,
                    start_ts=Time.from_string(start_ts),
                    stop_ts=Time.from_string(stop_ts),
                )
                for s in self.sources
            ),
            strategy=self.strategy,
        ).run()

    @property
    def stats(self):
        return None

    def plot(self, plotter=None, **kwargs):
        """TODO: default plotter by env and what is installed."""
        assert self.output

        plotter = FinplotPlotter(output=self.output)
        plotter.run()
