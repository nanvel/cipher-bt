from typing import List

from pandas import DataFrame
from pydantic import BaseModel


class Datas(BaseModel):
    data_frames: List[DataFrame]

    class Config:
        arbitrary_types_allowed = True

    @property
    def df(self):
        return self.data_frames[0]

    def __getitem__(self, item):
        return self.data_frames[item]
