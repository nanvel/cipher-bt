from functools import reduce
from operator import attrgetter
from typing import List, Iterator

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
