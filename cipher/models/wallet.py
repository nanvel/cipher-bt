from decimal import Decimal
from typing import Optional

from .commission import Commission
from .transaction import Transaction


class Wallet:
    def __init__(self):
        self._base = Decimal(0)
        self._quote = Decimal(0)

    def apply(self, transaction: Transaction, commission: Optional[Commission] = None):
        self._base += transaction.base
        self._quote += transaction.quote

        if commission:
            self._quote -= commission.for_transaction(transaction)

    @property
    def base(self) -> Decimal:
        return self._base

    @property
    def quote(self) -> Decimal:
        return self._quote
