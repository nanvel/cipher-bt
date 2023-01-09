from typing import Optional

from ..models import Commission, Output, Stats, Time, Wallet


class StatsFactory:
    def __init__(self, commission: Optional[Commission]):
        self.commission = commission

    def from_output(self, output: Output):
        start_ts = Time.from_datetime(output.df.index[0])
        stop_ts = Time.from_datetime(output.df.index[-1])

        sessions = output.sessions.closed_sessions

        wallet = Wallet()

        for transaction in sessions.transactions:
            wallet.apply(transaction, commission=self.commission)

        assert wallet.base == 0

        return Stats(
            start_ts=start_ts,
            stop_ts=stop_ts,
            period=stop_ts - start_ts,
            sessions_n=len(sessions),
            pnl=wallet.quote,
        )
