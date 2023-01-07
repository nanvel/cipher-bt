from decimal import Decimal

from cipher.models import Cursor, Session, Time, Wallet
from cipher.values import percent


def test_session():
    cursor = Cursor()
    wallet = Wallet()

    cursor.ts = Time.from_string('2020-01-01T01:01')
    cursor.price = 20

    session = Session(cursor=cursor, wallet=wallet)

    p = session.position

    p += 1

    assert wallet.base == 1
    assert wallet.quote == -20

    p -= percent(50)

    assert wallet.base == Decimal(0.5)
    assert wallet.quote == -10
