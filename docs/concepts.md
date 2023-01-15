# Concepts

Ciphers is distinct from the most of the other backtesting frameworks.
It focuses on position adjustments, in scope of a session.

## Session (trading session)

Session starts from adding or reducing position inside `on_entry` method.

Session is considered closed when position is adjusted to zero.

Long sessions is a session that starts from adding position, and short session - starts from reducing position.

Multiple open sessions can coexist at the same time.

Each session carries these attributes:
- `position`
- `transactions` (read only)
- `take_profit`
- `stop_loss`
- `meta`

`position` adjustment creates a new `transaction` (combines both base and quote assets move).

`take_profit` and `stop_loss` - session brackets.

Brackets can use `percent` similar to position:
```python
session.take_profit = row['close'] * 1.015
session.take_profit = percent('1.5')  # +1.5% of current price for long session
session.stop_loss = percent('-1')  # -1% of current price for long session
session.stop_loss = None  # disable stop loss
```

`meta` - a dict-like object where we can store session specific state.

## Position adjustment

There are multiple ways to adjust position:
```python
from cipher import base, percent, quote

session.position = 1
session.position = base(1)  # same as the previous one
session.position = '1'  # int, str, float is being converted to Decimal
session.position = quote(100)  # sets position worth 100 quote asset
session.position += 1  # adds to the position
session.position -= Decimal('1.25')  # reduces position by 1.25
session.position += percent(50)  # adds 50% more position
session.position *= 1.5  # has the same effect as the previous one
```

## Signals

There is one signal that is required - `entry`. We can define as many as we want.

To add a new signal:
- a bool column, with name equal the signal name, have to be present in the dataframe returned by compose method
- a signal handler have to be added to the strategy: `on_<signal name>`

on_entry is called only once for a new session.

`on_<signal>` is being called for each open session.

## Datas

Cipher supports multiple time series as input, they have to be combined into a single dataframe in the `compose` method.

To add datas:
```python
cipher.add_source("binance_spot_ohlc", symbol="BTCUSDT", interval="1h")
cipher.add_source("binance_spot_ohlc", symbol="ETHUSDT", interval="1h")
```

Then we can access data inside `compose`:
```python
def compose(self):
    self.datas[0]  # btcusdt ohlc
    self.datas[1]  # ethusdt ohlc
    self.datas.df  # shortcut for self.datas[0]
```
