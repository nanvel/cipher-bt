from typing import List, Optional

from pandas import DataFrame
from pydantic import BaseModel

from .sessions import Sessions


class Output(BaseModel):
    df: DataFrame
    sessions: Sessions
    signals: List[str]
    title: str
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
