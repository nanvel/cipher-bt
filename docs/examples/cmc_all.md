# Run the CoinMarketCap rank strategy for multiple assets

Run [CoinMarketCap rank](cmc.md) strategy for multiple assets and write stats into a csv file:
```python
import csv
import json

import numpy as np
import pandas_ta as ta

from cipher import Cipher, Session, Strategy, quote


class CmcStrategy(Strategy):
    def compose(self):
        df = self.datas.df

        # close price is required
        df["close"] = df["price"]
        df["rank"] = df["cmc_rank"].fillna(method="ffill")
        df = df.drop(columns=["price", "cmc_rank"])

        df["rank_ema21"] = ta.ema(df["rank"], length=21)
        df["rank_ema7"] = ta.ema(df["rank"], length=7)

        df["difference"] = df["rank_ema7"] - df["rank_ema21"]
        df["entry"] = np.sign(df["difference"].shift(1)) != np.sign(df["difference"])

        df["cross_up"] = df["entry"] & (df["difference"] > 0)
        df["cross_down"] = df["entry"] & (df["difference"] < 0)

        return df[df["difference"].notnull()]

    def on_entry(self, row: dict, session: Session):
        if row["cross_down"]:
            session.position += quote(100)
        else:
            session.position -= quote(100)

    def on_cross_up(self, row, session: Session):
        if session.is_long:
            session.position = 0

    def on_cross_down(self, row, session: Session):
        if not session.is_long:
            session.position = 0


def run_for_asset(asset_id, asset_slug):
    cipher = Cipher()
    cipher.add_source("csv_file", path=f"data/{asset_id}_{asset_slug}.csv")
    cipher.set_strategy(CmcStrategy())
    cipher.run(start_ts="2021-11-20", stop_ts="2022-01-20")
    cipher.set_commission("0.0025")
    return cipher.stats


def main():
    with open("data/cmc_results.csv", "w") as fo:
        writer = csv.writer(fo)
        writer.writerow(["slug", "sessions", "pnl", "drawdown"])
        with open("data/ids.json", "r") as f:
            data = json.load(f)
            for i, slug, symbol, name in data["data"]:
                stats = run_for_asset(i, slug)
                writer.writerow(
                    [slug, stats.sessions_n, stats.pnl, stats.balance_drawdown_max]
                )


if __name__ == "__main__":
    main()
```

Stats:
```python
import pandas as pd


pd.set_option("display.float_format", lambda x: '%.3f' % x)

df = pd.read_csv("data/cmc_results.csv")

print(df[df.pnl > 10000])
#                slug  trades         pnl  drawdown
# 2793  uberstate-inc       6 2626781.549    27.372

print(df[df.pnl < -10000])
#                   slug  trades           pnl     drawdown
# 456              aeron       4    -10656.038    10655.839
# 1136          hyperion       1   -155835.789   155855.572
# 1198       fidex-token      15    -20737.524    28933.483
# 1619           onlexpa       2    -43243.517    43257.982
# 2117    kimchi-finance       4    -31278.215    31277.971
# 5422  galaxygoggle-dao       2    -14924.211    15785.439
# 5493           pumpeth       4 -79166174.958 93672953.625

df = df[(df.pnl != 0) & (df.pnl > -200) & (df.pnl < 200)]

df["pnl"].describe()
# count   3638.000
# mean     -21.617
# std       46.315
# min     -199.955
# 25%      -41.490
# 50%      -13.245
# 75%        2.371
# max      180.636
# Name: pnl, dtype: float64

df["pnl"].sum()
# -78641.39720448424
```
