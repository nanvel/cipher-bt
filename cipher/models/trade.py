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
    def is_long(self):
        return self.direction == Direction.LONG

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

    def liquidate(self, price: Decimal, ts: Time):
        self.reduce(price=price, ts=ts, quantity=self.position)

    def add(self, price: Decimal, quantity: Decimal, ts: Time):
        self.transactions.append(
            Transaction(ts=ts, base_quantity=quantity, quote_quantity=-quantity * price)
        )

    def reduce(self, price: Decimal, quantity: Decimal, ts: Time):
        self.transactions.append(
            Transaction(ts=ts, base_quantity=-quantity, quote_quantity=quantity * price)
        )

    def check(
        self, low: Decimal, high: Decimal
    ) -> (bool, bool):  # take_profit, stop_loss
        take_profit = False
        stop_loss = False

        if self.is_long:
            if low < self.stop_loss:
                stop_loss = True
            elif high > self.take_profit:
                take_profit = True
        else:
            if high > self.stop_loss:
                stop_loss = True
            elif low < self.take_profit:
                stop_loss = True

        return take_profit, stop_loss
