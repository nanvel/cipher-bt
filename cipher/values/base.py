from typing import Union
from decimal import Decimal

from pydantic import BaseModel


class Base(BaseModel):
    value: Union[int, str, Decimal]


def base(value: Union[int, str, Decimal]):
    return Base(value=value)
