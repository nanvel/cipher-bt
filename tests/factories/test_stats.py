from cipher.factories import StatsFactory
from cipher.models import SimpleCommission


def test_stats(output):
    commission = SimpleCommission("0.0025")
    stats = StatsFactory(commission=commission).from_output(output)
    assert str(stats.start_ts) == "2022-01-23 07:00"
    assert str(stats.stop_ts) == "2022-02-28 23:00"
    assert str(stats.period) == "36d 16h"
    assert str(stats.sessions_n) == "4"
    assert str(stats.pnl) == "-10.560706823534050339"
