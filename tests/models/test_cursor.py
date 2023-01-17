from decimal import Decimal

import pytest

from cipher.models import Cursor


def test_default():
    cursor = Cursor()

    assert cursor.price == 0
    assert cursor.ts == 0


def test_patch_price():
    cursor = Cursor()

    assert cursor.price == 0

    with cursor.patch_price(price=Decimal(1)):
        assert cursor.price == 1

    assert cursor.price == 0


def test_patch_price_with_error():
    cursor = Cursor()

    assert cursor.price == 0

    with pytest.raises(AssertionError):
        with cursor.patch_price(price=Decimal(1)):
            raise AssertionError("For test.")

    assert cursor.price == 0
