from decimal import Decimal

from pydantic import BaseModel

from .time import Time


class Position(BaseModel):
    quantity: int
    price: Decimal
    ts: Time
