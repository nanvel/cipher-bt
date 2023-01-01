import math
from decimal import Decimal
from typing import Union


def to_decimal(value: Union[int, str, Decimal, float]) -> Decimal:
    if isinstance(value, Decimal):
        return value
    elif isinstance(value, (int, str)):
        return Decimal(value)
    elif isinstance(value, float):
        return float_to_decimal(value)
    else:
        raise ValueError("Supported types: int, str, Decimal, float.")


def float_to_decimal(value: Union[float, int]) -> Decimal:
    """Keep 4 significant numbers precision
    that should be ok for prices."""
    if isinstance(value, Decimal):
        return value

    assert isinstance(value, (float, int))

    if value > 1:
        q = ".01"
    else:
        q = "." + "0" * round(-math.log10(value)) + "0001"

    return Decimal(value).quantize(Decimal(q))
