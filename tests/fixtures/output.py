import pytest
from decimal import Decimal

from cipher.models import (
    Meta,
    Session,
    Output,
    Sessions,
    Time,
    Transaction,
    Transactions,
)


@pytest.fixture
def output(df):
    sessions = Sessions(
        [
            Session(
                transactions=Transactions(
                    [
                        Transaction(
                            ts=Time(1578560400),
                            base=Decimal("47824.007651841224295"),
                            quote=Decimal("-100.00000000000000000"),
                        ),
                        Transaction(
                            ts=Time(1578564000),
                            base=Decimal("-23912.003825920612147"),
                            quote=Decimal("50.839311334289813486"),
                        ),
                        Transaction(
                            ts=Time(1578650400),
                            base=Decimal("-23912.003825920612148"),
                            quote=Decimal("51.678622668579626974"),
                        ),
                    ]
                ),
                take_profit=Decimal("0.0021612"),
                stop_loss=Decimal("0.0020910"),
                meta=Meta(
                    meta_dict={"next_take_profit": None, "next_stop_loss": 0.002091}
                ),
            )
        ]
    )

    return Output(
        df=df,
        sessions=sessions,
        signals=["entry"],
        title="A title",
        description=None,
    )
