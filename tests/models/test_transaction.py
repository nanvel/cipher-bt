from decimal import Decimal

import pytest

from cipher.models import Time, Transaction


def test_transaction():
    transaction = Transaction(
        ts=Time.from_string("2020-01-01T01:01"), base=Decimal(1), quote=Decimal(20)
    )

    with pytest.raises(TypeError):
        transaction.base = Decimal(2)

    assert transaction.price == Decimal(20)
