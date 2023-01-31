from cipher.factories import StatsFactory
from cipher.models import SimpleCommission


def test_stats(output):
    commission = SimpleCommission("0.0025")
    stats = StatsFactory(commission=commission).from_output(output)
    assert str(stats.start_ts) == "2020-01-08 09:00"
    assert str(stats.stop_ts) == "2020-01-10 23:00"
    assert str(stats.period) == "2d 14h"
    assert str(stats.sessions_n) == "1"
    assert str(stats.pnl) == "2.0116391678622668586"
