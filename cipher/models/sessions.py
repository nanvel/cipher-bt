from decimal import Decimal
from functools import reduce
from operator import attrgetter
from typing import List, Optional

from .transaction import Transaction


class Sessions(list):
    @property
    def open_sessions(self):
        return list(filter(attrgetter("is_open"), self))

    @property
    def closed_sessions(self):
        return list(filter(attrgetter("is_closed"), self))

    def find_closest_sl_tp(self) -> (Optional[Decimal], Optional[Decimal]):
        """Find the closest prices at which we will need to check stop_loss/take_profit."""
        ups = []
        downs = []
        for session in self.open_sessions:
            if session.is_long:
                if session.take_profit:
                    ups.append(session.take_profit)
                if session.stop_loss:
                    downs.append(session.stop_loss)
            else:
                if session.take_profit:
                    downs.append(session.take_profit)
                if session.stop_loss:
                    ups.append(session.stop_loss)

        return max(downs) if downs else None, min(ups) if ups else None

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
