from typing import Union
from decimal import Decimal

from pydantic import BaseModel


class Base(BaseModel):
    value: Decimal


def base(value: Union[int, str, Decimal]):
    if isinstance(value, Decimal):
        return Base(value=value)
    return Base(value=Decimal(value))
