from decimal import Decimal
from typing import List, Optional, Union

from .container import Container
from .models import Commission, Time, SimpleCommission
from .plotters import FinplotPlotter, OHLCPlotRow, SignalsPlotRow, IndicatorsPlotRow
from .sources import Source, SOURCES
from .strategy import Strategy
from .trader import Trader
from .values import Percent


class Cipher:
    def __init__(self, **settings):
        self.container = Container()
        self.container.config.from_dict(settings)

        self.strategy = None
        self.sources: List[Source] = []
        self.sessions = None
        self.signals = None
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

    def run(self, start_ts: Union[Time, str], stop_ts: Union[Time, str], **kwargs):
        trader = Trader(
            data_service=self.data_service,
            sources=self.sources,
            strategy=self.strategy,
            start_ts=Time.from_string(start_ts),
            stop_ts=Time.from_string(stop_ts),
        )

        self.df = trader.run()
        self.sessions = trader.sessions
        self.signals = trader.signals

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
