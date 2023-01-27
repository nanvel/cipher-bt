from pandas import DataFrame, BooleanDtype

from cipher.models import Datas
from cipher.strategy import Strategy
from cipher.trader import Trader


def test_ensure_df_entry():
    trader = Trader(datas=Datas(), strategy=Strategy())

    df = DataFrame({"acolumn": [1, 2, 3]})

    trader._ensure_df_entry(df)

    assert set(df.columns) == {"acolumn", "entry"}
    assert isinstance(df.dtypes["entry"], BooleanDtype)
