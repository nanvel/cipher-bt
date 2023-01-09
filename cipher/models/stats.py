from pydantic import BaseModel
from tabulate import tabulate

from .time import Time
from .time_delta import TimeDelta


class Stats(BaseModel):
    """https://github.com/ranaroussi/quantstats
    period - dataframe size
    pnl - profit and loss
    trades_count - sessions count
    success_count
    failure_count
    success_pnl_med - success pnl median
    failure_pnl_med
    pnl_max
    pnl_min
    failure_row_max - max failures in row
    success_row_max
    drawdown_max
    drawdown_duration_max
    high_watermark - the highest balance
    romad - return over maximum drawdown
    overperform - pnl/(last - start price change abs)
    spf - success per failure
    largest_win
    largest_loss
    number_of_longs
    number_of_shorts
    commission paid
    holding_period
    sharpe_ratio
    calmar_ratio
    sortino_ratio
    """

    start_ts: Time
    stop_ts: Time
    period: TimeDelta

    def __str__(self):
        return tabulate(
            [
                ["start", str(self.start_ts)],
                ["stop", str(self.stop_ts)],
                ["period", str(self.period)],
            ],
        )
