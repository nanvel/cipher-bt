from decimal import Decimal
from typing import List, Optional, Union

from .events import Event, SetStopLoss, SetTakeProfit, Transaction
from .tick import Tick
from .time import Time
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
    def __init__(self, tick: Tick, events: List[Event], wallet: Wallet):
        self._tick = tick
        self._events = events
        self._wallet = wallet
        self.value = Decimal(0)

    def __iadd__(self, other: Union[Base, Quote, Percent, Decimal, int, str]):
        difference = self._parse_quantity(other)
        if difference:
            self.value += difference
            transaction = Transaction(
                ts=self._tick.ts,
                base_quantity=difference,
                quote_quantity=difference * self._tick.price,
            )
            self._events.append(transaction)
            self._wallet.apply(transaction)

    def __isub__(self, other: Union[Base, Quote, Percent, Decimal, int, str]):
        self.__iadd__(-self._parse_quantity(other))

    def set(self, value: Union[Base, Quote, Percent, Decimal, int, str]):
        new_value = self._parse_quantity(value)
        difference = new_value - self.value
        if difference:
            self.value = new_value
            transaction = Transaction(
                ts=self._tick.ts,
                base_quantity=difference,
                quote_quantity=difference * self._tick.price,
            )
            self._events.append(transaction)
            self._wallet.apply(transaction)

    def _parse_quantity(self, quantity) -> Decimal:
        if isinstance(quantity, Base):
            return to_decimal(quantity.value)
        elif isinstance(quantity, Quote):
            return to_decimal(quantity.value) / self._tick.price
        elif isinstance(quantity, Percent):
            return to_decimal(quantity.value) * self.value
        else:
            return to_decimal(quantity)


class Session:
    def __init__(self, tick: Tick, wallet: Wallet):
        self._tick = tick
        self._take_profit: Optional[Decimal] = None
        self._stop_loss: Optional[Decimal] = None
        self.events: List[Event] = []
        self._position = Position(tick=tick, events=self.events, wallet=wallet)

    def _parse_price(self, price: Union[Percent, Decimal, int, str]) -> Decimal:
        if isinstance(price, Percent):
            return to_decimal(price.value) * self._tick.price
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
        self.events.append(SetTakeProfit(ts=self._tick.ts, price=price))

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
        self.events.append(SetStopLoss(ts=self._tick.ts, price=price))

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
    def transactions(self) -> List[Transaction]:
        return list(filter(lambda i: isinstance(i, Transaction), self.events))

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
