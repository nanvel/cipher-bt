from decimal import Decimal

from pydantic import BaseModel

from .time import Time


class Transaction(BaseModel):
    base_quantity: Decimal
    quote_quantity: Decimal
    ts: Time

    @property
    def price(self) -> Decimal:
        return self.quote_quantity / self.base_quantity
