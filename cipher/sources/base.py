from abc import ABC, abstractmethod
from pathlib import Path

from ..models import Time


class Source(ABC):
    @property
    @abstractmethod
    def slug(self):
        pass

    @abstractmethod
    def load(self, ts: Time, path: Path) -> (Time, Time):
        """Load 500 rows into path."""
        pass
