# Cipher - Trading Strategy Backtesting Framework

![Tests](https://github.com/nanvel/cipher-bt/actions/workflows/tests.yaml/badge.svg)
[![PyPI version](https://badge.fury.io/py/cipher-bt.svg)](https://badge.fury.io/py/cipher-bt)
[![Python Versions](https://img.shields.io/pypi/pyversions/cipher-bt.svg)](https://pypi.python.org/pypi/cipher-bt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![cipher](https://github.com/nanvel/cipher-bt/raw/master/docs/cipher.jpeg)

- [Usage](#usage)  
- [Development](#development)
- [Disclaimer](#disclaimer)

Documentation: https://cipher.nanvel.com

**Features:**

- Well-structured, intuitive, and easily extensible design
- Support for multiple concurrent trading sessions
- Sophisticated exit strategies including trailing take profits
- Multi-source data integration (exchanges, symbols, timeframes)
- Clean separation between signal generation and handling
- Simple execution - just run `python my_strategy.py`
- Compatibility with [Google Colab](https://colab.research.google.com/)
- Built-in visualization with [finplot](https://github.com/highfestiva/finplot) and [mplfinance](https://github.com/matplotlib/mplfinance) plotters

## Usage

Set up a new strategies workspace and create your first strategy:
```shell
mkdir strategies
cd strategies
uv init
uv add 'cipher-bt[finplot,talib]'

uv run cipher init
uv run cipher new my_strategy
uv run python my_strategy.py
```

Complete EMA crossover strategy example:
```python
import numpy as np
import talib

from cipher import Cipher, Session, Strategy


class EmaCrossoverStrategy(Strategy):
    def __init__(self, fast_ema_length=9, slow_ema_length=21, trend_ema_length=200):
        self.fast_ema_length = fast_ema_length
        self.slow_ema_length = slow_ema_length
        self.trend_ema_length = trend_ema_length

    def compose(self):
        df = self.datas.df
        df["fast_ema"] = talib.EMA(df["close"], timeperiod=self.fast_ema_length)
        df["slow_ema"] = talib.EMA(df["close"], timeperiod=self.slow_ema_length)
        df["trend_ema"] = talib.EMA(df["close"], timeperiod=self.trend_ema_length)

        df["difference"] = df["fast_ema"] - df["slow_ema"]

        # Signal columns must be boolean type
        df["entry"] = np.sign(df["difference"].shift(1)) != np.sign(df["difference"])

        df["max_6"] = df["high"].rolling(window=6).max()
        df["min_6"] = df["low"].rolling(window=6).min()

        return df

    def on_entry(self, row: dict, session: Session):
        if row["difference"] > 0 and row["close"] > row["trend_ema"]:
            # Open a new long position
            session.position += "0.01"
            session.stop_loss = row["min_6"]
            session.take_profit = row["close"] + 1.5 * (row["close"] - row["min_6"])

        elif row["difference"] < 0 and row["close"] < row["trend_ema"]:
            # Open a new short position
            session.position -= "0.01"
            session.stop_loss = row["max_6"]
            session.take_profit = row["close"] - 1.5 * (row["max_6"] - row["close"])

    # def on_<signal>(self, row: dict, session: Session) -> None:
    #     """Custom signal handler called for each active session.
    #     Adjust or close positions and modify brackets here."""
    #     # session.position = 1
    #     # session.position = base(1)  # equivalent to the above
    #     # session.position = '1'  # int, str, float are converted to Decimal
    #     # session.position = quote(100)  # position worth 100 quote asset
    #     # session.position += 1  # add to the position
    #     # session.position -= Decimal('1.25')  # reduce position by 1.25
    #     # session.position += percent(50)  # add 50% more to position
    #     # session.position *= 1.5  # equivalent to the above
    #     pass
    #
    # def on_take_profit(self, row: dict, session: Session) -> None:
    #     """Called when take profit is hit. Default action closes the position.
    #     Modify position and brackets here to continue the session."""
    #     session.position = 0
    #
    # def on_stop_loss(self, row: dict, session: Session) -> None:
    #     """Called when stop loss is hit. Default action closes the position.
    #     Modify position and brackets here to continue the session."""
    #     session.position = 0
    #
    # def on_stop(self, row: dict, session: Session) -> None:
    #     """Called for each active session when dataframe ends.
    #     Close open sessions here, otherwise they will be ignored."""
    #     session.position = 0


def main():
    cipher = Cipher()
    cipher.add_source("binance_spot_ohlc", symbol="BTCUSDT", interval="1h")
    cipher.set_strategy(EmaCrossoverStrategy())
    cipher.run(start_ts="2020-01-01", stop_ts="2020-04-01")
    cipher.set_commission("0.00075")
    print(cipher.sessions)
    print(cipher.stats)
    cipher.plot()


if __name__ == "__main__":
    main()
```

![ema_crossover_plot](https://github.com/nanvel/cipher-bt/raw/master/docs/plotter.png)

## Development

```shell
brew install uv
uv sync
source .venv/bin/activate

pytest tests
cipher --help
```

## Disclaimer

This software is for educational purposes only. Do not risk money you cannot afford to lose.
USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS.
