from decimal import Decimal

import pytest

from cipher.models import Time, Transaction, Wallet


def test_wallet():
    wallet = Wallet()

    assert wallet.base == 0
    assert wallet.quote == 0

    with pytest.raises(AttributeError):
        wallet.base += 1

    wallet.apply(
        Transaction(
            ts=Time.from_string("2020-01-01T01:01"), base=Decimal(1), quote=Decimal(-10)
        )
    )

    assert wallet.base == Decimal("1")
    assert wallet.quote == Decimal("-10")
