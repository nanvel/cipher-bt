import pytest
from decimal import Decimal

from cipher.models import Session, Output, Sessions, Time, Transaction, Transactions


@pytest.fixture
def output(df):
    sessions = Sessions(
        [
            Session(
                transactions=Transactions(
                    [
                        Transaction(
                            ts=Time(1643400000),
                            base=Decimal("0.0026503981693169764894"),
                            quote=Decimal("-100.00000000000000000"),
                        ),
                        Transaction(
                            ts=Time(1643886000),
                            base=Decimal("-0.0026503981693169764894"),
                            quote=Decimal("97.415358209263777698"),
                        ),
                    ]
                ),
                stop_loss=Decimal("35843.6710"),
            ),
            Session(
                transactions=Transactions(
                    [
                        Transaction(
                            ts=Time(1643990400),
                            base=Decimal("0.0024845306907864906128"),
                            quote=Decimal("-99.999999999999999999"),
                        ),
                        Transaction(
                            ts=Time(1644699600),
                            base=Decimal("-0.0024845306907864906128"),
                            quote=Decimal("104.00247956162940492"),
                        ),
                    ]
                ),
                stop_loss=Decimal("38236.5975"),
            ),
            Session(
                transactions=Transactions(
                    [
                        Transaction(
                            ts=Time(1644958800),
                            base=Decimal("0.0022740193291642978965"),
                            quote=Decimal("-99.999999999999999999"),
                        ),
                        Transaction(
                            ts=Time(1645110000),
                            base=Decimal("-0.0022740193291642978965"),
                            quote=Decimal("94.999999999999999999"),
                        ),
                    ]
                ),
                stop_loss=Decimal("41776.2500"),
            ),
            Session(
                transactions=Transactions(
                    [
                        Transaction(
                            ts=Time(1645869600),
                            base=Decimal("0.0025652141569038891212"),
                            quote=Decimal("-100"),
                        ),
                        Transaction(
                            ts=Time(1645995600),
                            base=Decimal("-0.0025652141569038891212"),
                            quote=Decimal("95.000000000000000001"),
                        ),
                    ]
                ),
                stop_loss=Decimal("37033.9450"),
            ),
        ]
    )

    return Output(
        df=df,
        sessions=sessions,
        signals=["entry", "death_cross"],
        title="A title",
        description=None,
    )
