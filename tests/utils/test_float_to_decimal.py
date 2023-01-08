from decimal import Decimal

from cipher.utils import float_to_decimal


def test_float_to_decimal():
    assert float_to_decimal(1) == Decimal(1)
    assert float_to_decimal(1.2) == Decimal("1.2")
    assert float_to_decimal(1.2) == Decimal("1.2")
    assert float_to_decimal(1.0 / 3) == Decimal("0.3333")
    assert float_to_decimal(0.000567123) == Decimal("0.0005671")
