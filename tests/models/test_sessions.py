from cipher.models import Cursor, Session, Sessions, Time, Wallet
from cipher.proxies import SessionProxy


def create_session():
    cursor = Cursor()
    wallet = Wallet()

    cursor.ts = Time.from_string("2020-01-01T01:01")
    cursor.price = 20

    return SessionProxy(Session(), cursor=cursor, wallet=wallet)


def test_sessions():
    session1 = create_session()
    session2 = create_session()

    session1.position += 1
    session1.position = 0
    session2.position += 1

    sessions = Sessions()
    sessions.append(session1)
    sessions.append(session2)

    assert sessions.open_sessions == [session2]


def test_transactions():
    session1 = create_session()
    session1._cursor.ts = Time.from_string("2020-01-01T01:01")
    session1.position += 1
    session1._cursor.ts = Time.from_string("2020-01-01T02:01")
    session1.position = 0

    session2 = create_session()
    session2._cursor.ts = Time.from_string("2020-01-01T01:05")
    session2.position += 2
    session2._cursor.ts = Time.from_string("2020-01-01T03:00")
    session2.position = 0

    session3 = create_session()
    session3.position += 1

    sessions = Sessions([session1, session2, session3])

    assert [t.ts for t in sessions.transactions] == [
        Time(1577840460),
        Time(1577840700),
        Time(1577844060),
        Time(1577847600),
    ]
