from decimal import Decimal
from operator import attrgetter
from typing import Optional


class Sessions(list):
    @property
    def open_sessions(self):
        return list(filter(attrgetter("is_open"), self))

    def prices_of_interest(self) -> (Optional[Decimal], Optional[Decimal]):
        """Find the closest prices at which we will need to check stop_loss/take_profit."""
        closest_up = None
        closest_down = None
        for trade in self.open_sessions:
            min_price = min(trade.take_profit, trade.stop_loss)
            max_price = max(trade.take_profit, trade.stop_loss)

            if closest_up is None or closest_up > max_price:
                closest_up = max_price
            if closest_down is None or closest_down < min_price:
                closest_down = min_price

        return closest_down, closest_up
