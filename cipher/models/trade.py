from typing import List, Optional

from pydantic import BaseModel

from .direction import Direction
from .position import Position
from .time import Time


class Trade(BaseModel):
    direction: Direction
    positions: List[Position]

    @property
    def position(self) -> Position:
        return self.positions[-1]

    @property
    def is_open(self) -> bool:
        return self.position.quantity > 0

    @property
    def opened_ts(self) -> Time:
        return self.positions[0].ts

    @property
    def closed_ts(self) -> Optional[Time]:
        if self.is_open:
            return self.position.ts
        return None

    def liquidate(self):
        pass
