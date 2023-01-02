from typing import List

from pydantic import BaseModel

from .trade import Trade


class Trades(BaseModel):
    trades: List[Trade] = []
