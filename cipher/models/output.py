from typing import List

from pandas import DataFrame
from pydantic import BaseModel

from .transactions import Transactions


class Output(BaseModel):
    df: DataFrame
    transactions: Transactions
    signals: List[str]
