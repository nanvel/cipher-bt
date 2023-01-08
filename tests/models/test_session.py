from decimal import Decimal

import pytest

from cipher.models import Cursor, Session, Time, Wallet
from cipher.values import percent


@pytest.fixture
def session():
    cursor = Cursor()
    wallet = Wallet()

    cursor.ts = Time.from_string("2020-01-01T01:01")
    cursor.price = 20

    return Session(cursor=cursor, wallet=wallet)


def test_closed(session):
    session.position += 1

    assert session.is_open is True

    session.position = 0

    assert session.is_open is False
    assert session.closed_ts


def test_properties(session):
    session.position = 1
    session.position += percent(50)

    assert session.position.value == Decimal("1.5")
    assert session.quote == -30
    assert session.is_long
    assert session.is_open
    assert session.opened_ts
    assert session.closed_ts is None


def test_should_tp_sl(session):
    session.position += 1
    session.take_profit = 25
    session.stop_loss = 15

    assert session.should_tp_sl(low=Decimal(19), high=Decimal(21)) == (False, False)
    assert session.should_tp_sl(low=Decimal(14), high=Decimal(21)) == (False, True)
    assert session.should_tp_sl(low=Decimal(19), high=Decimal(30)) == (True, False)
    assert session.should_tp_sl(low=Decimal(14), high=Decimal(30)) == (False, True)


def test_take_profit_long(session):
    session.position += 1

    with pytest.raises(AssertionError):
        session.take_profit = 10

    session.take_profit = "25"
    assert session.take_profit == 25

    session.take_profit = percent(1)
    assert session.take_profit == Decimal("20.2")


def test_take_profit_short(session):
    session.position -= 1

    with pytest.raises(AssertionError):
        session.take_profit = 25

    session.take_profit = "15"
    assert session.take_profit == 15


def test_stop_loss_long(session):
    session.position += 1

    with pytest.raises(AssertionError):
        session.stop_loss = 25

    session.stop_loss = "15"
    assert session.stop_loss == 15

    session.stop_loss = percent(-1)
    assert session.stop_loss == Decimal("19.8")


def test_stop_loss_short(session):
    session.position -= 1

    with pytest.raises(AssertionError):
        session.stop_loss = 15

    session.stop_loss = "25"
    assert session.stop_loss == 25
