import pytest

from pandas import read_csv

from .. import DATA_PATH


@pytest.fixture
def df():
    return (
        read_csv(DATA_PATH / "df.csv").astype({"ts": "datetime64[ms]"}).set_index("ts")
    )
