from typing import List

from .models import Time
from .sources import Source


class Engine:
    def __init__(self, sources: List[Source], start_ts: Time, stop_ts: Time):
        self.sources = sources

    def run(self):
        pass
