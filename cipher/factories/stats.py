from decimal import Decimal
from statistics import median
from typing import Optional

import pandas as pd

from ..models import Commission, Output, Stats, Time, Wallet


class StatsFactory:
    def __init__(self, commission: Optional[Commission]):
        self.commission = commission

    def from_output(self, output: Output) -> Stats:
        if len(output.df.index):
            start_ts = Time.from_datetime(output.df.index[0])
            stop_ts = Time.from_datetime(output.df.index[-1])
        else:
            start_ts = Time(0)
            stop_ts = Time(0)

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
            periods.append(session.transactions[-1].ts - session.transactions[0].ts)

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

        if output.sessions:
            balance_df = self._balance_df(output=output)
            balance_min = balance_df.min()
            balance_max = balance_df.max()
            balance_drawdown_max = abs((balance_df - balance_df.cummax()).min())
            romad = (
                balance_df.iat[-1] / balance_drawdown_max
                if balance_drawdown_max
                else None
            )
        else:
            balance_min = Decimal(0)
            balance_max = Decimal(0)
            balance_drawdown_max = Decimal(0)
            romad = None

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
            balance_min=balance_min,
            balance_max=balance_max,
            balance_drawdown_max=balance_drawdown_max,
            romad=romad,
        )

    def _balance_df(self, output: Output) -> pd.DataFrame:
        df = output.df

        position_col = "_position"
        quote_col = "_quote"

        df[position_col] = pd.Series(dtype="float64")
        df[quote_col] = pd.Series(dtype="float64")

        df.at[df.index[0], position_col] = 0
        df.at[df.index[0], quote_col] = 0

        wallet = Wallet()

        for transaction in output.sessions.transactions:
            wallet.apply(transaction, commission=self.commission)
            ts = transaction.ts.to_datetime()
            df.at[ts, position_col] = float(wallet.base)
            df.at[ts, quote_col] = float(wallet.quote)

        df[position_col] = df[position_col].fillna(method="ffill")
        df[quote_col] = df[quote_col].fillna(method="ffill")

        _df = df[position_col] * df["close"] + df[quote_col]

        output.df = df.drop([position_col, quote_col], axis=1)

        return _df
