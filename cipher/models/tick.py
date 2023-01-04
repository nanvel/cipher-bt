from decimal import Decimal

from pydantic import BaseModel

from .time import Time


class Tick(BaseModel):
    price: Decimal
    ts: Time

    @classmethod
    def init(cls):
        return cls(price=Decimal(0), ts=Time.from_timestamp(0))
