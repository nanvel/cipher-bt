from typing import List

from pandas import DataFrame
from pydantic import BaseModel

from .sessions import Sessions


class Output(BaseModel):
    df: DataFrame
    sessions: Sessions
    signals: List[str]

    class Config:
        arbitrary_types_allowed = True
