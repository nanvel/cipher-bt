import colorsys
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


def create_palette(n):
    hsv_tuples = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples)

    return [
        "#{:02x}{:02x}{:02x}".format(*[int(i * 255) for i in t]) for t in rgb_tuples
    ]
