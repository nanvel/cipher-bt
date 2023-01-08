from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Union

from ..values import Percent
from .transaction import Transaction


class Commission(ABC):
    @abstractmethod
    def for_transaction(self, transaction: Transaction) -> Decimal:
        pass


class SimpleCommission(Commission):
    def __init__(self, value: Union[Decimal, str, Percent]):
        if isinstance(value, Percent):
            self.value = value.value / Decimal(100)
        elif isinstance(value, Decimal):
            self.value = value
        else:
            self.value = Decimal(value)

    def for_transaction(self, transaction: Transaction) -> Decimal:
        return abs(transaction.quote) * self.value
