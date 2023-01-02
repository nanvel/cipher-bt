from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from .direction import Direction
from .transaction import Transaction
from .time import Time


class Trade(BaseModel):
    direction: Direction
    transactions: List[Transaction]
    take_profit: Decimal
    stop_loss: Decimal

    @property
    def position(self) -> Decimal:
        return sum([i.base_quantity for i in self.transactions])

    @property
    def is_open(self) -> bool:
        return self.position > 0

    @property
    def opened_ts(self) -> Time:
        return self.transactions[0].ts

    @property
    def closed_ts(self) -> Optional[Time]:
        if self.is_open:
            return self.transactions[-1].ts
        return None

    def liquidate(self):
        pass
