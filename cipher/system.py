from decimal import Decimal
from typing import List, Optional, Type, Union

from .container import Container
from .factories import StatsFactory
from .models import Commission, Datas, Output, Sessions, SimpleCommission, Stats, Time
from .plotters import get_default_plotter, Plotter, PLOTTERS
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

    def set_commission(self, value: Union[Commission, Decimal, str, Percent]):
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
    def stats(self) -> Stats:
        assert self.output

        return StatsFactory(commission=self.commission).from_output(self.output)

    @property
    def sessions(self):
        return Sessions(self.output.sessions, commission=self.commission)

    def plot(
        self,
        plotter: Union[None, Type[Plotter], str] = None,
        start: Union[str, int, None] = None,
        limit: Optional[int] = None,
        **kwargs
    ):
        assert self.output

        if isinstance(plotter, str):
            plotter_cls = PLOTTERS[plotter]
        elif isinstance(plotter, type) and issubclass(plotter, Plotter):
            plotter_cls = plotter
        else:
            plotter_cls = get_default_plotter()

        plotter_cls(
            output=self.output, start=start, limit=limit, commission=self.commission
        ).run(**kwargs)
