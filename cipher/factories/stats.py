from statistics import median
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
        wallet_no_commission = Wallet()

        success = []
        failure = []

        success_row_max = 0
        failure_row_max = 0
        success_row = 0
        failure_row = 0

        longs_n = 0
        shorts_n = 0

        periods = []

        for session in sessions:
            periods.append(
                session.transactions[-1].ts - session.transactions[0].ts
            )

            session_wallet = Wallet()
            for transaction in session.transactions:
                wallet.apply(transaction, commission=self.commission)
                session_wallet.apply(transaction, commission=self.commission)
                wallet_no_commission.apply(transaction)

            if session_wallet.quote > 0:
                success.append(session_wallet.quote)
                success_row += 1
                failure_row = 0
            else:
                failure.append(-session_wallet.quote)
                failure_row += 1
                success_row = 0

            if success_row > success_row_max:
                success_row_max = success_row
            if failure_row > failure_row_max:
                failure_row_max = failure_row

            if session.is_long:
                longs_n += 1
            else:
                shorts_n += 1

        assert wallet.base == 0

        return Stats(
            start_ts=start_ts,
            stop_ts=stop_ts,
            period=stop_ts - start_ts,
            sessions_n=len(sessions),
            success_n=len(success),
            failure_n=len(failure),
            success_pnl_med=median(success) if success else None,
            failure_pnl_med=median(failure) if failure else None,
            success_pnl_max=max(success) if success else None,
            failure_pnl_max=max(failure) if failure else None,
            success_row_max=success_row_max,
            failure_row_max=failure_row_max,
            pnl=wallet.quote,
            longs_n=longs_n,
            shorts_n=shorts_n,
            commission=wallet_no_commission.quote - wallet.quote,
            session_period_max=max(periods) if periods else None,
            session_period_median=median(periods) if periods else None,
        )
