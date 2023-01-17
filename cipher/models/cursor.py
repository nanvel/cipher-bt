from contextlib import contextmanager
from datetime import datetime
from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from ..utils import float_to_decimal
from .time import Time


class Cursor(BaseModel):
    """Current backtest position storage."""

    price: Decimal = Decimal(0)
    ts: Time = Time(0)

    def set(self, ts: datetime, price: Union[int, float, Decimal]):
        self.ts = Time.from_datetime(ts)
        self.price = float_to_decimal(price)

    @contextmanager
    def patch_price(self, price: Decimal):
        _saved_price = self.price
        self.price = price
        try:
            yield
        finally:
            self.price = _saved_price
