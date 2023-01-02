from typing import Optional

from decimal import Decimal

from cipher.models import Direction, Trade, Transaction, Time


class TradeFactory:
    def create(
        self,
        row: dict,
        base_quantity: Optional[Decimal] = None,
        quote_quantity: Optional[Decimal] = None,
        take_profit: Optional[Decimal] = None,
        stop_loss: Optional[Decimal] = None,
        take_profit_pt: Optional[Decimal] = None,  # percents from entry
        stop_loss_pt: Optional[Decimal] = None,
        direction: Direction = Direction.LONG,
    ) -> Trade:
        assert stop_loss or stop_loss_pt
        assert take_profit or take_profit_pt

        price = Decimal(row["close"])

        if not stop_loss:
            if direction == Direction.LONG:
                stop_loss = price * (1 - (stop_loss_pt / 100))
            else:
                stop_loss = price * (1 + (stop_loss_pt / 100))

        if not take_profit:
            if direction == Direction.LONG:
                take_profit = price * (1 + (take_profit_pt / 100))
            else:
                take_profit = price * (1 - (take_profit_pt / 100))

        if direction == Direction.LONG:
            assert take_profit > price
            assert stop_loss < price
        else:
            assert stop_loss > price
            assert take_profit < price

        assert base_quantity or quote_quantity

        if base_quantity is None:
            base_quantity = quote_quantity / price
        else:
            quote_quantity = base_quantity * price

        return Trade(
            direction=direction,
            take_profit=take_profit,
            stop_loss=stop_loss,
            transactions=[
                Transaction(
                    ts=Time.from_datetime(row["ts"]),
                    base_quantity=base_quantity,
                    quote_quantity=quote_quantity,
                )
            ],
        )
