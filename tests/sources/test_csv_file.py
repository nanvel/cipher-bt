import pytest

from cipher.models import Time
from cipher.sources import CsvFileSource
from .. import DATA_PATH


@pytest.fixture(scope="module")
def source():
    return CsvFileSource(path=str((DATA_PATH / "df.csv").resolve()))


def test_slug(source):
    assert source.slug == "csv_file/df"


def test_detect_ts_format(source):
    assert (
        source._detect_ts_format(str(int(Time.from_string("2020-01-01")) * 1000))
        == "ms"
    )
    assert source._detect_ts_format(str(int(Time.from_string("2020-01-01")))) == "s"
    assert source._detect_ts_format("2020-01-01") == "%Y-%m-%d"
