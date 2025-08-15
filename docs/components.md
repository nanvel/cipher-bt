---
description: Detailed documentation for each component in the Cipher trading system.
---

# Components

## Session (Trading Session)

A session begins when you add to or reduce a position within the `on_entry` method.

A session closes when its position is adjusted to zero.

- A **long session** starts by adding to the position
- A **short session** starts by reducing the position

Multiple open sessions can exist simultaneously.

Each session contains these attributes:

- `position`
- `transactions` (read-only)
- `take_profit`
- `stop_loss`
- `meta`

Position adjustments create new `transactions` (which combine both base and quote asset movements).

`take_profit` and `stop_loss` define session brackets.

Brackets usage:
```python
from cipher import percent

session.take_profit = row['close'] * 1.015
session.take_profit = percent('1.5')  # +1.5% of current price for long sessions
session.stop_loss = percent('-1')     # -1% of current price for long sessions
session.stop_loss = None              # disable stop loss
```

`meta` is a dictionary-like object where you can store session state information.

## Position

Each new session starts with a position of 0.

You can add to or reduce a position (positions can be negative).

Each position change creates a transaction.

There are multiple ways to adjust position:
```python
from cipher import base, percent, quote

session.position = 1
session.position = base(1)           # same as above
session.position = '1'               # int, str, float are converted to Decimal
session.position = quote(100)        # sets position worth 100 quote asset units
session.position += 1                # adds to the position
session.position -= Decimal('1.25')  # reduces position by 1.25
session.position += percent(50)      # adds 50% more to the position
session.position *= 1.5              # same effect as above
session.position = session.position.value + Decimal(1)  # not recommended
```

## Signals

The `entry` signal is required. You can define as many additional signals as needed.

To add a new signal:
- Add a boolean column with the signal name to the dataframe returned by the `compose` method
- Add a signal handler to the strategy: `on_<signal_name>`

`on_entry` is called only once for each new session.

`on_<signal>` is called for each open session.

`on_step` is similar to `on_entry`, but is called for every row in the dataframe.

## Data Sources

![data flow](data_flow.png)

Cipher supports multiple time series as input. These must be combined into a single dataframe in the `compose` method.

To add data sources:
```python
cipher.add_source("binance_spot_ohlc", symbol="BTCUSDT", interval="1h")
cipher.add_source("binance_spot_ohlc", symbol="ETHUSDT", interval="1h")
```

Access data within the `compose` method:
```python
def compose(self):
    self.datas[0]   # BTCUSDT OHLC data
    self.datas[1]   # ETHUSDT OHLC data
    self.datas.df   # shortcut for self.datas[0]
```

## Sources

Sources read data from APIs, files, etc., in blocks and write them to files.

Several sources are included:

- `binance_futures_ohlc [symbol, interval]`
- `binance_spot_ohlc [symbol, interval]`
- `csv_file [path, ts_format]`
- `gateio_spot_ohlc [symbol, interval]`
- `yahoo_finance_ohlc [symbol, interval]`

## Strategy

The Strategy class tells Cipher when and how to adjust positions.

Interface:
```python
from pandas import DataFrame

from .models import Datas, Wallet
from .proxies import SessionProxy as Session

class Strategy:
    datas: Datas
    wallet: Wallet

    # def __init__(self, param1, param2):
    #     self.param1 = param1
    #     self.param2 = param2

    def compose(self) -> DataFrame:
        return self.datas.df

    def on_entry(self, row: dict, session: Session) -> None:
        pass

    # def on_<signal>(self, row: dict, session: Session) -> None:
    #     pass

    def on_take_profit(self, row: dict, session: Session) -> None:
        session.position = 0

    def on_stop_loss(self, row: dict, session: Session) -> None:
        session.position = 0

    def on_stop(self, row: dict, session: Session) -> None:
        pass
```

Strategies are stored in files. Generate a new strategy using:

```bash
cipher new my_strategy
```

To run it:
```bash
python my_strategy.py
```

## Cipher Instance

The Cipher instance connects all Cipher components together.

```python
# Pass settings as kwargs, otherwise settings load from .env or ENV variables
cipher = Cipher()
cipher.set_strategy(strategy_object)
cipher.set_commission(commission_or_commission_object)
cipher.add_source(source_name_or_source_object, **source_kwargs)

# Process data according to strategy and generate output
cipher.run(start_ts, stop_ts)

cipher.sessions  # returns sessions
cipher.stats     # builds and returns stats object
cipher.output    # raw output containing dataframe and sessions

# If plotter or rows aren't specified, values are automatically selected
cipher.plot(plotter_or_plotter_object_or_none, rows_or_none)
```

## Commission

Commission objects implement this interface:
```python
from abc import ABC, abstractmethod
from decimal import Decimal

from cipher.models.transaction import Transaction

class Commission(ABC):
    @abstractmethod
    def for_transaction(self, transaction: Transaction) -> Decimal:
        pass
```

The `for_transaction` method returns how much quote asset should be deducted.

By default, SimpleCommission is used, which returns the specified portion of the quote for each transaction.

Commission is only computed for stats and plotting—it doesn't apply to the output.

## Wallet

Access the wallet from a strategy:
```python
self.wallet
```

The Cipher wallet has two assets: base and quote, both starting at 0.

The wallet has no limits, and assets can go negative.

Transactions are applied to the wallet, adjusting the asset balances.

## Stats

Stats is the object returned by the `cipher.stats` property.

Use stats to evaluate strategy performance.

## Plotters

Plotters take Output and generate charts.

Two plotters are currently available:

- [finplot](https://github.com/highfestiva/finplot) (doesn't work in Jupyter notebooks)
- [mplfinance](https://github.com/matplotlib/mplfinance)

You can pass a custom plotter to `cipher.plot`.

Plotters accept rows that describe to the plotter how to group charts. Use this if the default layout doesn't fit your needs.

Rows can contain:

- `ohlc`
- `ohlcv`
- `signals`
- `position`
- `balance`
- `sessions`
- `brackets`
- `<indicator_name>`

Examples:
```python
rows = [['ohlc']]                          # show only OHLC
rows = [['ohlc', 'ema50']]                 # show EMA50 as well (must be in dataframe)
rows = [['ohlcv', 'sessions'], ['balance']] # show OHLCV with session marks on top chart and balance below
```

`plot` also accepts `limit` (number of rows to show) and `start` (where the plot begins).
`start` can be: datetime, offset, or negative offset.

Indicator names can include markers and colors. See markers [here](https://matplotlib.org/stable/api/markers_api.html).

Example:
```python
rows = [['ohlc', 'my_indicator|^', 'another_indicator|s|red']]
```

## Settings

Pass settings to Cipher as arguments, or use `.env` file or environment variables.

Available settings: `cache_root`, `log_level`.

**cache_root**: Contains the path to the cache folder. Default: `.cache`

If you have multiple directories with strategies and want to reuse one cache, specify the same `cache_root` for both.
