import inspect

from typing import List


class StrategyWrapper:
    def __init__(self, strategy):
        self.strategy = strategy

    def find_signal_handlers(self) -> List[str]:
        skip_handler = {"on_take_profit", "on_stop_loss"}

        handlers = []
        for key, _ in inspect.getmembers(self.strategy.__class__):
            if key.startswith("on_") and key not in skip_handler:
                handlers.append(key[3:])

        return handlers
