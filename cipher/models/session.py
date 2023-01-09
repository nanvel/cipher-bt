from decimal import Decimal
from typing import Optional, Union

from ..utils import to_decimal
from ..values import Base, Percent, Quote
from .cursor import Cursor
from .position import Position
from .time import Time
from .transactions import Transactions
from .wallet import Wallet


class BaseSession:
    def __init__(
        self,
        transactions: Transactions,
        take_profit: Optional[Decimal] = None,
        stop_loss: Optional[Decimal] = None,
    ):
        self.transactions = transactions
        self._take_profit = take_profit
        self._stop_loss = stop_loss

    @property
    def take_profit(self) -> Optional[Decimal]:
        return self._take_profit

    @property
    def stop_loss(self) -> Optional[Decimal]:
        return self._stop_loss

    @property
    def base(self):
        return sum(t.base for t in self.transactions)

    @property
    def quote(self) -> Decimal:
        return sum(t.quote for t in self.transactions)

    @property
    def is_long(self) -> bool:
        return self.transactions[0].base > 0

    @property
    def is_open(self) -> bool:
        return self.base != 0

    @property
    def is_closed(self) -> bool:
        return not self.is_open

    @property
    def opened_ts(self) -> Time:
        return self.transactions[0].ts

    @property
    def closed_ts(self) -> Optional[Time]:
        if self.is_open:
            return None
        return self.transactions[-1].ts


class Session(BaseSession):
    def __init__(self, cursor: Cursor, wallet: Wallet):
        super().__init__(Transactions())
        self._cursor = cursor

        self._position = Position(
            cursor=cursor, transactions=self.transactions, wallet=wallet
        )

    def _parse_price(self, price: Union[Percent, Decimal, int, str, float]) -> Decimal:
        if isinstance(price, Percent):
            return (price.value / Decimal(100) + Decimal(1)) * self._cursor.price
        else:
            return to_decimal(price)

    @property
    def take_profit(self) -> Optional[Decimal]:
        return self._take_profit

    @take_profit.setter
    def take_profit(self, value: Union[Percent, Decimal, int, str, float]):
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
    def stop_loss(self, value: Union[Percent, Decimal, int, str, float]):
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
    def position(
        self, value: Union[Base, Quote, Percent, Decimal, int, str, float, Position]
    ):
        if isinstance(value, Position):
            self._position = value
        else:
            self._position.set(value)

    def should_tp_sl(
        self, low: Decimal, high: Decimal
    ) -> (Optional[Decimal], Optional[Decimal]):  # take_profit, stop_loss
        take_profit = None
        stop_loss = None

        if self.is_long:
            if low < self.stop_loss:
                stop_loss = self.stop_loss
            elif high > self.take_profit:
                take_profit = self.take_profit
        else:
            if high > self.stop_loss:
                stop_loss = self.stop_loss
            elif low < self.take_profit:
                take_profit = self.take_profit

        return take_profit, stop_loss

    def to_base(self):
        return BaseSession(
            self.transactions, take_profit=self.take_profit, stop_loss=self.stop_loss
        )
