from decimal import Decimal


class Wallet:
    def __init__(self):
        self._base = Decimal(0)
        self._quote = Decimal(0)

    def apply(self, transaction):
        self._base += transaction.base
        self._quote += transaction.quote

    @property
    def base(self):
        return self._base

    @property
    def quote(self):
        return self._quote
