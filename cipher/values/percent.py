from typing import Union
from decimal import Decimal

from pydantic import BaseModel

from ..utils import to_decimal


class Percent(BaseModel):
    value: Decimal


def percent(value: Union[int, str, float, Decimal]):
    return Percent(value=to_decimal(value))
