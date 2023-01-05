from typing import Union
from decimal import Decimal

from pydantic import BaseModel


class Percent(BaseModel):
    value: Union[int, str, Decimal]


def percent(value: Union[int, str, Decimal]):
    return Percent(value=value)
