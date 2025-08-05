from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from .percent import to_decimal


class Quote(BaseModel):
    value: Decimal


def quote(value: Union[int, str, float, Decimal]):
    return Quote(value=to_decimal(value))
