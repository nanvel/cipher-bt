from typing import Union
from decimal import Decimal

from pydantic import BaseModel


class Quote(BaseModel):
    value: Decimal


def quote(value: Union[int, str, Decimal]):
    if isinstance(value, Decimal):
        return Quote(value=value)
    return Quote(value=Decimal(value))
