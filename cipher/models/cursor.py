from decimal import Decimal

from pydantic import BaseModel

from .time import Time


class Cursor(BaseModel):
    """Current backtest position storage."""

    price: Decimal = Decimal(0)
    ts: Time = Time.from_timestamp(0)
