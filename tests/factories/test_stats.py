from cipher.factories import StatsFactory


def test_stats(output):
    stats = StatsFactory().from_output(output)
    assert str(stats.start_ts) == "2022-01-23 07:00"
    assert str(stats.stop_ts) == "2022-02-28 23:00"
    assert str(stats.period) == "36d 16h"
