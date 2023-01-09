from ..models import Output, Stats, Time


class StatsFactory:
    def from_output(self, output: Output):
        start_ts = Time.from_datetime(output.df.index[0])
        stop_ts = Time.from_datetime(output.df.index[-1])

        return Stats(start_ts=start_ts, stop_ts=stop_ts, period=stop_ts - start_ts)
