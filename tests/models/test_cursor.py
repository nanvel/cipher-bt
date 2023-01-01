from cipher.models import Cursor


def test_default():
    cursor = Cursor()

    assert cursor.price == 0
    assert cursor.ts.to_timestamp() == 0


def test_patch_price():
    cursor = Cursor()

    assert cursor.price == 0

    with cursor.patch_price(price=1):
        assert cursor.price == 1

    assert cursor.price == 0
