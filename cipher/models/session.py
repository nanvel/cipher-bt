from decimal import Decimal
from typing import List, Optional, Union

from .tick import Tick
from .time import Time
from .transaction import Transaction
from .wallet import Wallet
from ..values import Base, Percent, Quote


def to_decimal(value: Union[int, str, Decimal]) -> Decimal:
    if isinstance(value, Decimal):
        return value
    elif isinstance(value, (int, str)):
        return Decimal(value)
    elif isinstance(value, float):
        raise ValueError(
            "Float is not supported, pass either string '1.2', or Decimal('1.2')."
        )
    else:
        raise ValueError("Supported types: int, str, Decimal.")


class Position:
    def __init__(self, tick: Tick, transactions: List[Transaction], wallet: Wallet):
        self._tick = tick
        self._transactions = transactions
        self._wallet = wallet
        self.value = Decimal(0)

    def __iadd__(self, other: Union[Base, Quote, Percent, Decimal, int, str]):
        to_add = self._parse_quantity(other)
        self._add(to_add)

    def __isub__(self, other: Union[Base, Quote, Percent, Decimal, int, str]):
        to_sub = self._parse_quantity(other)
        self._add(-to_sub)

    def __imul__(self, other: Union[Decimal, int, str]):
        mul = self._parse_quantity(other)
        self._add((self.value * mul) - self.value)

    def set(self, value: Union[Base, Quote, Percent, Decimal, int, str]):
        new_value = self._parse_quantity(value)
        self._add(new_value - self.value)

    def _add(self, to_add: Decimal):
        if to_add:
            self.value += to_add
            transaction = Transaction(
                ts=self._tick.ts,
                base_quantity=to_add,
                quote_quantity=to_add * self._tick.price,
            )
            self._transactions.append(transaction)
            self._wallet.apply(transaction)

    def _parse_quantity(self, quantity) -> Decimal:
        if isinstance(quantity, Base):
            return quantity.value
        elif isinstance(quantity, Quote):
            return quantity.value / self._tick.price
        elif isinstance(quantity, Percent):
            return quantity.value / Decimal(100) * self.value
        else:
            return to_decimal(quantity)


class Session:
    def __init__(self, tick: Tick, wallet: Wallet):
        self._tick = tick
        self._take_profit: Optional[Decimal] = None
        self._stop_loss: Optional[Decimal] = None
        self.transactions: List[Transaction] = []
        self._position = Position(
            tick=tick, transactions=self.transactions, wallet=wallet
        )

    def _parse_price(self, price: Union[Percent, Decimal, int, str]) -> Decimal:
        if isinstance(price, Percent):
            return (price.value / Decimal(100) + Decimal(1)) * self._tick.price
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
            assert price > self._tick.price
        else:
            assert price < self._tick.price

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
            assert price < self._tick.price
        else:
            assert price > self._tick.price

        self._stop_loss = price

    @property
    def position(self) -> Decimal:
        return self._position.value

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
