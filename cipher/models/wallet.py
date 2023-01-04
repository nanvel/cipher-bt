from decimal import Decimal

from pydantic import BaseModel


class Wallet(BaseModel):
    base: Decimal = Decimal(0)
    quote: Decimal = Decimal(0)

    def apply(self, transaction):
        self.base += transaction.base
        self.quote -= transaction.quote
