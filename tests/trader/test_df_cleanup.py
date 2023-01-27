import pytest
from pandas import DataFrame, BooleanDtype

from cipher.models import Datas
from cipher.strategy import Strategy
from cipher.trader import Trader


@pytest.fixture(scope="module")
def trader():
    return Trader(datas=Datas(), strategy=Strategy())


def test_ensure_df_entry(trader):
    df = DataFrame({"acolumn": [1, 2, 3]})

    trader._ensure_df_entry(df)

    assert set(df.columns) == {"acolumn", "entry"}
    assert isinstance(df.dtypes["entry"], BooleanDtype)


def test_validate_df_signals_ok(trader):
    trader = Trader(datas=Datas(), strategy=Strategy())

    df = DataFrame({"entry": [None, True], "another": [True, False]})

    trader._validate_df_signals(df, signals=["entry", "another"])


def test_validate_df_signals_missing(trader):
    trader = Trader(datas=Datas(), strategy=Strategy())

    df = DataFrame({"entry": [None, True]})

    with pytest.raises(ValueError):
        trader._validate_df_signals(df, signals=["entry", "another"])


def test_validate_df_signals_invalid_format(trader):
    trader = Trader(datas=Datas(), strategy=Strategy())

    df = DataFrame({"entry": [None, True], "another": [1, 2]})

    with pytest.raises(ValueError):
        trader._validate_df_signals(df, signals=["entry", "another"])
