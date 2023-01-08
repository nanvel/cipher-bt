from decimal import Decimal

import pytest

from cipher.models import Cursor, Position, Time, Transactions, Wallet
from cipher.values import percent


@pytest.fixture
def position():
    cursor = Cursor()
    wallet = Wallet()
    transactions = Transactions()

    cursor.ts = Time.from_string("2020-01-01T01:01")
    cursor.price = 20

    return Position(
        cursor=cursor,
        wallet=wallet,
        transactions=transactions,
    )


def test_add_sub_mul(position):
    position += 1
    position -= "0.2"
    position += Decimal("0.4")
    position -= percent(50)
    position *= 5

    assert position.value == Decimal(3)
    assert len(position._transactions) == 5
    last_transaction = position._transactions[-1]
    assert last_transaction.base == Decimal("2.4")
    assert last_transaction.quote == -48
    assert position._wallet.base == Decimal(3)
    assert position._wallet.quote == Decimal("-60")


def test_liquidate(position):
    position += 1

    position.set(0)

    assert len(position._transactions) == 2
    assert position._wallet.base == 0
