from decimal import Decimal

from pydantic import BaseModel

from .time import Time


class Transaction(BaseModel):
    ts: Time
    base: Decimal
    quote: Decimal

    @property
    def price(self) -> Decimal:
        return abs(self.quote / self.base)

    class Config:
        frozen = True
