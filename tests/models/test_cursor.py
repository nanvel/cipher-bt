from cipher.models import Cursor


def test_default():
    cursor = Cursor()

    assert cursor.price == 0
    assert cursor.ts.to_timestamp() == 0
