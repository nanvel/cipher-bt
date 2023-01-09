from decimal import Decimal
from functools import reduce
from operator import attrgetter
from typing import List, Optional, Iterator

from .session import Session
from .transaction import Transaction


class Sessions(list):
    def filter(self, condition) -> Iterator[Session]:
        return self.__class__(filter(condition, self))

    @property
    def open_sessions(self):
        return self.filter(attrgetter("is_open"))

    @property
    def closed_sessions(self):
        return self.filter(attrgetter("is_closed"))

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

    def to_base(self):
        return self.__class__((s.to_base() for s in self if isinstance(s, Session)))
