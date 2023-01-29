from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from tabulate import tabulate

from .time import Time
from .time_delta import TimeDelta


class Stats(BaseModel):
    """https://github.com/ranaroussi/quantstats"""

    # general
    start_ts: Time
    stop_ts: Time
    period: TimeDelta  # dataframe size
    exposed_period: TimeDelta

    # sessions
    sessions_n: int
    success_n: int
    failure_n: int
    shorts_n: int
    longs_n: int
    session_period_median: Optional[TimeDelta]
    session_period_max: Optional[TimeDelta]

    # performance
    pnl: Decimal  # profit and loss
    volume: Decimal
    commission: Decimal
    success_pnl_med: Optional[Decimal]
    failure_pnl_med: Optional[Decimal]
    success_pnl_max: Optional[Decimal]
    failure_pnl_max: Optional[Decimal]
    success_row_max: int
    failure_row_max: int
    balance_min: Decimal
    balance_max: Decimal
    balance_drawdown_max: Decimal
    romad: Optional[Decimal]

    def to_table(self):
        return tabulate(
            [
                ["start", str(self.start_ts), ""],
                ["stop", str(self.stop_ts), ""],
                ["period", str(self.period), ""],
                ["trades", str(self.sessions_n), ""],
                [
                    "longs",
                    str(self.longs_n),
                    self._to_percent(self.longs_n, self.sessions_n),
                ],
                [
                    "shorts",
                    str(self.shorts_n),
                    self._to_percent(self.shorts_n, self.sessions_n),
                ],
                ["period median", str(self.session_period_median), ""],
                ["period max", str(self.session_period_max), ""],
                [
                    "success",
                    str(self.success_n),
                    self._to_percent(self.success_n, self.sessions_n),
                ],
                ["success median", str(self.success_pnl_med), ""],
                ["success max", str(self.success_pnl_max), ""],
                ["success row", str(self.success_row_max), ""],
                [
                    "failure",
                    str(self.failure_n),
                    self._to_percent(self.failure_n, self.sessions_n),
                ],
                ["failure median", str(self.failure_pnl_med), ""],
                ["failure max", str(self.failure_pnl_max), ""],
                ["failure row", str(self.failure_row_max), ""],
                [
                    "spf",
                    str(self.success_n / self.failure_n if self.failure_n else None),
                    "",
                ],
                ["pnl", str(self.pnl), ""],
                ["volume", str(self.volume), ""],
                [
                    "commission",
                    str(self.commission.normalize()),
                    self._to_percent(self.commission, self.pnl)
                    if self.pnl > self.commission
                    else "",
                ],
                [
                    "exposed period",
                    str(self.exposed_period),
                    self._to_percent(self.exposed_period, self.period),
                ],
                ["balance min", str(self.balance_min), ""],
                ["balance max", str(self.balance_max), ""],
                ["balance drawdown", str(self.balance_drawdown_max), ""],
                ["romad", str(self.romad), ""],
            ],
        )

    def __repr__(self):
        return self.to_table()

    def __str__(self):
        return self.to_table()

    def _to_percent(self, numerator, denominator) -> str:
        if numerator and denominator:
            return f"{Decimal(numerator * 100 / denominator).quantize(Decimal('0.1'))}%"
        return ""
