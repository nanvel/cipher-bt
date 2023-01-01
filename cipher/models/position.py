from decimal import Decimal
from typing import Union

from ..utils import to_decimal
from ..values import Base, Percent, Quote
from .cursor import Cursor
from .transaction import Transaction
from .transactions import Transactions
from .wallet import Wallet


class Position:
    def __init__(self, cursor: Cursor, transactions: Transactions, wallet: Wallet):
        self._cursor = cursor
        self._transactions = transactions
        self._wallet = wallet
        self.value = Decimal(0)

    def __iadd__(self, other: Union[Base, Quote, Percent, Decimal, int, str, float]):
        to_add = self._parse_quantity(other)
        return self._add(to_add)

    def __isub__(self, other: Union[Base, Quote, Percent, Decimal, int, str, float]):
        to_sub = self._parse_quantity(other)
        return self._add(-to_sub)

    def __imul__(self, other: Union[Decimal, int, str, float]):
        mul = self._parse_quantity(other)
        return self._add((self.value * mul) - self.value)

    def set(self, value: Union[Base, Quote, Percent, Decimal, int, str, float]):
        new_value = self._parse_quantity(value)
        self._add(new_value - self.value)

    def _add(self, to_add: Decimal):
        if to_add:
            self.value += to_add
            transaction = Transaction(
                ts=self._cursor.ts,
                base=to_add,
                quote=-to_add * self._cursor.price,
            )
            self._transactions.append(transaction)
            self._wallet.apply(transaction)
        return self

    def _parse_quantity(self, quantity) -> Decimal:
        if isinstance(quantity, Base):
            return quantity.value
        elif isinstance(quantity, Quote):
            return quantity.value / self._cursor.price
        elif isinstance(quantity, Percent):
            return quantity.value / Decimal(100) * self.value
        else:
            return to_decimal(quantity)
