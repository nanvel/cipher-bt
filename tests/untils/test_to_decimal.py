import pytest

from decimal import Decimal

from cipher.utils import to_decimal


def test_to_decimal():
    assert to_decimal(Decimal(10)) == Decimal(10)
    assert to_decimal("10.1") == Decimal("10.1")
    assert to_decimal(1) == Decimal(1)

    with pytest.raises(ValueError):
        to_decimal(1.5)

    with pytest.raises(ValueError):
        to_decimal([])
