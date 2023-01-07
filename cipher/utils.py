from decimal import Decimal
from typing import Union


def to_decimal(value: Union[int, str, Decimal]) -> Decimal:
    if isinstance(value, Decimal):
        return value
    elif isinstance(value, (int, str)):
        return Decimal(value)
    elif isinstance(value, float):
        raise ValueError(
            "Float is not supported, pass either string '1.2', or Decimal('1.2')."
        )
    else:
        raise ValueError("Supported types: int, str, Decimal.")
