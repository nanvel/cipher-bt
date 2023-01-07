from typing import Union
from decimal import Decimal

from pydantic import BaseModel


class Percent(BaseModel):
    value: Decimal


def percent(value: Union[int, str, Decimal]):
    if isinstance(value, Decimal):
        return Percent(value=value)
    return Percent(value=Decimal(value))
