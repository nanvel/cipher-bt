from cipher.models import Datas
from cipher.strategy import Strategy
from cipher.trader import Trader


class MyStrategy(Strategy):
    def on_my_event(self, row, session):
        pass


def test_extract_strategy_signal_handlers():
    trader = Trader(datas=Datas(), strategy=MyStrategy())

    signals = trader._extract_strategy_signal_handlers()

    assert list(sorted(signals)) == ["entry", "my_event"]
