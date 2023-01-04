from typing import Union
from decimal import Decimal

from pydantic import BaseModel


class Quote(BaseModel):
    value: Union[int, str, Decimal]


def quote(value: Union[int, str, Decimal]):
    return Quote(value=value)
