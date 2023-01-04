from decimal import Decimal

from pydantic import BaseModel

from .time import Time


class Event(BaseModel):
    ts: Time


class Transaction(Event):
    base: Decimal
    quote: Decimal

    @property
    def price(self) -> Decimal:
        return self.quote / self.base


class SetStopLoss(Event):
    price: Decimal


class SetTakeProfit(Event):
    price: Decimal
