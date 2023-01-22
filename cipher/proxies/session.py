from decimal import Decimal
from typing import Optional, Union

from ..models import Cursor, Position, Session, Transactions, Wallet
from ..utils import to_decimal
from ..values import Base, Percent, Quote


class SessionProxy:
    def __init__(self, session: Session, cursor: Cursor, wallet: Wallet):
        self._session = session
        self._cursor = cursor
        self._position = Position(
            cursor=cursor, transactions=self._session.transactions, wallet=wallet
        )
        self.meta = session.meta

    def _parse_price(self, price: Union[Percent, Decimal, int, str, float]) -> Decimal:
        if isinstance(price, Percent):
            return (price.value / Decimal(100) + Decimal(1)) * self._cursor.price
        else:
            return to_decimal(price)

    @property
    def session(self) -> Session:
        return self._session

    @property
    def is_long(self) -> bool:
        return self._session.is_long

    @property
    def is_open(self) -> bool:
        return self._session.is_open

    @property
    def is_closed(self) -> bool:
        return self._session.is_closed

    @property
    def transactions(self) -> Transactions:
        return self._session.transactions

    @property
    def take_profit(self) -> Optional[Decimal]:
        return self._session.take_profit

    @take_profit.setter
    def take_profit(self, value: Union[Percent, Decimal, int, str, float]):
        price = self._parse_price(value)
        if self._session.take_profit == price:
            return

        if self._session.is_long:
            assert price > self._cursor.price
        else:
            assert price < self._cursor.price

        self._session.take_profit = price

    @property
    def stop_loss(self) -> Optional[Decimal]:
        return self._session.stop_loss

    @stop_loss.setter
    def stop_loss(self, value: Union[Percent, Decimal, int, str, float]):
        price = self._parse_price(value)
        if self._session.stop_loss == price:
            return

        if self._session.is_long:
            assert price < self._cursor.price
        else:
            assert price > self._cursor.price

        self._session.stop_loss = price

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

        if self._session.is_long:
            if self.stop_loss and low < self.stop_loss:
                stop_loss = self.stop_loss
            elif self.take_profit and high > self.take_profit:
                take_profit = self.take_profit
        else:
            if self.stop_loss and high > self.stop_loss:
                stop_loss = self.stop_loss
            elif self.take_profit and low < self.take_profit:
                take_profit = self.take_profit

        return take_profit, stop_loss
