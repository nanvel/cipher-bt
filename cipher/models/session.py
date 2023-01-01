from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from .meta import Meta
from .time import Time
from .transactions import Transactions


class Session(BaseModel):
    transactions: Transactions = Field(default_factory=Transactions)
    take_profit: Optional[Decimal] = None
    stop_loss: Optional[Decimal] = None
    meta: Meta = Field(default_factory=Meta)

    @property
    def base(self):
        return sum(t.base for t in self.transactions)

    @property
    def quote(self) -> Decimal:
        return sum(t.quote for t in self.transactions)

    @property
    def is_long(self) -> bool:
        return self.transactions[0].base > 0

    @property
    def is_open(self) -> bool:
        return self.base != 0

    @property
    def is_closed(self) -> bool:
        return not self.is_open

    @property
    def opened_ts(self) -> Time:
        return self.transactions[0].ts

    @property
    def closed_ts(self) -> Optional[Time]:
        if self.is_open:
            return None
        return self.transactions[-1].ts
