import pytest
from pandas import BooleanDtype, DataFrame, Series

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


def test_ensure_df_signals_type_ok(trader):
    trader = Trader(datas=Datas(), strategy=Strategy())

    df = DataFrame(
        {
            "entry": Series([False, True], dtype="boolean"),
            "another": [None, True],
        }
    )
    df["my_signal"] = df["entry"] & df["another"]

    trader._ensure_df_signals_type(df, signals=["entry", "my_signal"])


def test_ensure_df_signals_type_missing(trader):
    df = DataFrame({"entry": Series([None, True], dtype="boolean")})

    with pytest.raises(ValueError) as e:
        trader._ensure_df_signals_type(df, signals=["entry", "another"])

    assert "another signal column is missing in the dataframe." in str(e)


def test_ensure_df_signals_type_invalid_type(trader):
    df = DataFrame(
        {
            "entry": Series(None, dtype="boolean"),
            "another": Series([1, 2], dtype="int32"),
        }
    )

    with pytest.raises(ValueError) as e:
        trader._ensure_df_signals_type(df, signals=["entry", "another"])

    assert "another signal column type have to be boolean." in str(e)


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


def test_cut_df_nulls_scatter(trader):
    df = DataFrame(
        {
            "column_a": list(range(20)),
            "column_b": ([None] * 5) + [1, None, 2, 3, 4] + ([1] * 10),
        }
    )

    trader._cut_df_nulls(df)

    assert len(df) == 20
