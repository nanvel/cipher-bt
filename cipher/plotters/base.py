from abc import ABC, abstractmethod


class Plotter(ABC):
    @abstractmethod
    def run(self):
        pass
