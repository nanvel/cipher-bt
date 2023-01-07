from decimal import Decimal
from operator import attrgetter
from typing import Optional


class Sessions(list):
    @property
    def open_sessions(self):
        return list(filter(attrgetter("is_open"), self))

    def closest_sl_tp(self) -> (Optional[Decimal], Optional[Decimal]):
        """Find the closest prices at which we will need to check stop_loss/take_profit."""
        ups = []
        downs = []
        for session in self.open_sessions:
            if session.is_long:
                if session.take_profit:
                    ups.append(session.take_profit)
                if session.stop_loss:
                    downs.append(session.stop_loss)
            else:
                if session.take_profit:
                    downs.append(session.take_profit)
                if session.stop_loss:
                    ups.append(session.stop_loss)

        return max(downs) if downs else None, min(ups) if ups else None
