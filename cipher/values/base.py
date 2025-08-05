from decimal import Decimal
from typing import Union

from pydantic import BaseModel

from ..utils import to_decimal


class Base(BaseModel):
    value: Decimal


def base(value: Union[int, str, float, Decimal]):
    return Base(value=to_decimal(value))
