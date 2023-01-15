from cipher import Cipher, Strategy

from .. import DATA_PATH
from ..services.test_data import FakeOHLCSource


class MyStrategy(Strategy):
    pass


def test_cipher():
    cipher = Cipher(cache_root=DATA_PATH / "sources_cache")

    cipher.set_strategy(Strategy())
    cipher.add_source(FakeOHLCSource())
    cipher.run(start_ts="2020-01-01", stop_ts="2020-01-02")

    assert cipher.stats
