import pytest
from pandas import DataFrame, BooleanDtype

from cipher.models import Datas
from cipher.strategy import Strategy
from cipher.trader import Trader


@pytest.fixture(scope="module")
def trader():
    return Trader(datas=Datas(), strategy=Strategy())


def test_ensure_df_not_empty(trader):
    df = DataFrame({"entry": []})

    with pytest.raises(ValueError):
        trader._ensure_df_not_empty(df)

    df["entry"] = [1]

    trader._ensure_df_not_empty(df)


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
    df = DataFrame({"entry": [None, True]})

    with pytest.raises(ValueError):
        trader._validate_df_signals(df, signals=["entry", "another"])


def test_validate_df_signals_invalid_format(trader):
    df = DataFrame({"entry": [None, True], "another": [1, 2]})

    with pytest.raises(ValueError):
        trader._validate_df_signals(df, signals=["entry", "another"])


def test_cut_df_nulls(trader):
    df = DataFrame(
        {
            "column_a": list(range(20)),
            "column_b": ([None] * 5) + ([1] * 15),
            "column_c": [None] * 20,
        }
    )

    assert len(df) == 20

    trader._cut_df_nulls(df)

    assert len(df) == 15
