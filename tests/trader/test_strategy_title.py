from cipher.models import Datas
from cipher.strategy import Strategy
from cipher.trader import Trader


class MyStrategy(Strategy):
    """There is the title
    And some description,
    multiline.
    """


def test_extract_title():
    trader = Trader(datas=Datas(), strategy=MyStrategy())

    result = trader._extract_strategy_title()

    assert result == "There is the title"


def test_extract_description():
    trader = Trader(datas=Datas(), strategy=MyStrategy())

    result = trader._extract_strategy_description()

    assert result == "And some description,\nmultiline."


def test_no_docstring():
    trader = Trader(datas=Datas(), strategy=Strategy())

    title = trader._extract_strategy_title()
    description = trader._extract_strategy_description()

    assert title == "Strategy"
    assert description is None
