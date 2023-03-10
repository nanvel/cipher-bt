from decimal import Decimal

import pytest

from cipher.models import Cursor, Session, Time, Wallet
from cipher.proxies import SessionProxy
from cipher.values import percent


@pytest.fixture
def session():
    cursor = Cursor()
    wallet = Wallet()

    cursor.ts = Time.from_string("2020-01-01T01:01")
    cursor.price = 20

    return SessionProxy(Session(), cursor=cursor, wallet=wallet)


def test_closed(session):
    session.position += 1

    assert session.is_open is True

    session.position = 0

    assert session.is_open is False
    assert session.session.closed_ts
    assert len(session.transactions) == 2


def test_properties(session):
    session.position = 1
    session.position += percent(50)

    assert session.position.value == Decimal("1.5")
    assert session.session.quote == -30
    assert session.session.is_long
    assert session.is_open
    assert session.session.opened_ts
    assert session.session.closed_ts is None


def test_should_tp_sl(session):
    session.position += 1
    session.take_profit = 25
    session.stop_loss = 15

    assert session.should_tp_sl(low=Decimal(19), high=Decimal(21)) == (None, None)
    assert session.should_tp_sl(low=Decimal(14), high=Decimal(21)) == (None, 15)
    assert session.should_tp_sl(low=Decimal(19), high=Decimal(30)) == (25, None)
    assert session.should_tp_sl(low=Decimal(14), high=Decimal(30)) == (None, 15)


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


def test_meta(session):
    session.meta["a"] = 1

    assert session.meta["a"] == 1
