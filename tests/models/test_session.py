from decimal import Decimal

import pytest

from cipher.models import Session, Time, Transaction, Transactions


@pytest.fixture(scope="module")
def transaction_open():
    return Transaction(
        ts=Time(1643400000),
        base=Decimal("0.002"),
        quote=Decimal("-100"),
    )


@pytest.fixture(scope="module")
def transaction_close():
    return Transaction(
        ts=Time(1643886000),
        base=Decimal("-0.002"),
        quote=Decimal("97.415"),
    )


def test_open(transaction_open):
    session = Session(transactions=Transactions([transaction_open]))

    assert session.is_open is True


def test_closed(transaction_open, transaction_close):
    session = Session(transactions=Transactions([transaction_open, transaction_close]))

    assert session.base == 0
    assert session.is_open is False
    assert session.closed_ts
    assert len(session.transactions) == 2


def test_properties(transaction_open):
    session = Session(
        transactions=Transactions([transaction_open]), take_profit=Decimal(1)
    )

    assert session.base == Decimal("0.002")
    assert session.quote == -100
    assert session.is_long
    assert session.is_open
    assert session.opened_ts
    assert session.closed_ts is None
    assert session.take_profit == Decimal(1)
    assert session.stop_loss is None
