from decimal import Decimal
from typing import Optional, Union

from ..utils import to_decimal
from ..values import Base, Percent, Quote
from .cursor import Cursor
from .position import Position
from .time import Time
from .transactions import Transactions
from .wallet import Wallet


class Session:
    def __init__(self, cursor: Cursor, wallet: Wallet):
        self._cursor = cursor
        self._take_profit: Optional[Decimal] = None
        self._stop_loss: Optional[Decimal] = None

        self.transactions = Transactions()
        self._position = Position(
            cursor=cursor, transactions=self.transactions, wallet=wallet
        )

    def _parse_price(self, price: Union[Percent, Decimal, int, str]) -> Decimal:
        if isinstance(price, Percent):
            return (price.value / Decimal(100) + Decimal(1)) * self._cursor.price
        else:
            return to_decimal(price)

    @property
    def take_profit(self) -> Optional[Decimal]:
        return self._take_profit

    @take_profit.setter
    def take_profit(self, value: Union[Percent, Decimal, int, str]):
        price = self._parse_price(value)
        if self._take_profit == price:
            return

        if self.is_long:
            assert price > self._cursor.price
        else:
            assert price < self._cursor.price

        self._take_profit = price

    @property
    def stop_loss(self) -> Optional[Decimal]:
        return self._stop_loss

    @stop_loss.setter
    def stop_loss(self, value: Union[Percent, Decimal, int, str]):
        price = self._parse_price(value)
        if self._stop_loss == price:
            return

        if self.is_long:
            assert price < self._cursor.price
        else:
            assert price > self._cursor.price

        self._stop_loss = price

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Union[Base, Quote, Percent, Decimal, int, str]):
        self._position.set(value)

    @property
    def quote(self) -> Decimal:
        return sum([t.quote for t in self.transactions])

    @property
    def is_long(self) -> bool:
        return self.transactions[0].base > 0

    @property
    def is_open(self) -> bool:
        return self.position != 0

    @property
    def opened_ts(self) -> Time:
        return self.transactions[0].ts

    @property
    def closed_ts(self) -> Optional[Time]:
        if self.is_open:
            return self.transactions[-1].ts
        return None

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
