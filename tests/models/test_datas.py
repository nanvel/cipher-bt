from pandas import DataFrame

from cipher.models import Datas


def test_df():
    df1 = DataFrame([1, 2, 3])
    df2 = DataFrame([4, 5, 6])
    datas = Datas(data_frames=[df1, df2])

    assert datas.df.compare(df1).size == 0


def test_getitem():
    df = DataFrame([1, 2, 3])
    datas = Datas(data_frames=[df])

    assert datas[0].compare(df).size == 0
