from functools import reduce
from operator import attrgetter
from typing import List, Iterator

from tabulate import tabulate

from .commission import Commission
from .session import Session
from .transaction import Transaction
from .wallet import Wallet


class Sessions(list):
    def filter(self, condition) -> Iterator[Session]:
        return self.__class__(filter(condition, self))

    @property
    def open_sessions(self):
        return self.filter(attrgetter("is_open"))

    @property
    def closed_sessions(self):
        return self.filter(attrgetter("is_closed"))

    @property
    def transactions(self) -> List[Transaction]:
        """Sorted chained transactions from closed sessions."""
        return list(
            sorted(
                reduce(
                    lambda a, b: a + b,
                    map(attrgetter("transactions"), self.closed_sessions),
                    [],
                ),
                key=attrgetter("ts"),
            )
        )

    def to_table(self, commission: Commission):
        rows = []

        for session in self.closed_sessions:
            wallet = Wallet()
            for transaction in session.transactions:
                wallet.apply(transaction, commission=commission)

            rows.append(
                [
                    f"{'long' if session.is_long else 'short'} {session.opened_ts}",
                    str(session.closed_ts - session.opened_ts),
                    str(wallet.quote),
                ]
            )

        return tabulate(rows, headers=["Session", "Period", "PnL"])
