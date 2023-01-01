from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from ..models import Time
from ..sources import Source


class DataService:
    def __init__(self, cache_root: Path):
        self.cache_root = cache_root

    def load_df(self, source: Source, start_ts: Time, stop_ts: Time):
        ts = start_ts
        paths = []

        for i in range(20):
            result = self._load_from_cache(prefix=source.slug, ts=ts)
            if result:
                first_ts, last_ts, p = result
                completed = True
            else:
                first_ts, last_ts, p, completed = self._load_from_source(source=source, ts=ts)

            paths.append(p)

            if not completed:
                break

            if last_ts >= stop_ts:
                break
            else:
                ts = last_ts + (last_ts - first_ts) / 2

        return pd.concat((pd.read_csv(p) for p in paths), ignore_index=True)

    def _load_from_source(self, source: Source, ts: Time) -> (Time, Time, Path, bool):
        temp_path = self.cache_root / self._temp_path(prefix=source.slug, ts=ts)
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            first_ts, last_ts, completed = source.load(ts=ts, path=temp_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

        return (
            first_ts,
            last_ts,
            temp_path.rename(
                self.cache_root
                / self._full_path(
                    prefix=source.slug,
                    first_ts=first_ts,
                    last_ts=last_ts,
                    completed=completed,
                )
            ),
            completed,
        )

    def _load_from_cache(
        self, prefix: str, ts: Time
    ) -> Optional[Tuple[Time, Time, Path]]:
        second = int(ts.to_timestamp() / 1000)
        for p in (self.cache_root / prefix).glob("*_c.csv"):
            try:
                first_ts, last_ts, _ = p.stem.split("_")
                first_ts = int(first_ts)
                last_ts = int(last_ts)

                print("...", first_ts, second, last_ts)

                if first_ts <= second <= last_ts:
                    return (
                        Time.from_timestamp(first_ts * 1000),
                        Time.from_timestamp(last_ts * 1000),
                        p,
                    )
            except ValueError:
                pass

    def _temp_path(self, prefix: str, ts: Time):
        return prefix + f"/{ts.to_timestamp() // 1000}.csv"

    def _full_path(self, prefix: str, first_ts: Time, last_ts: Time, completed: bool):
        completed = "c" if completed else "i"
        return (
            prefix
            + f"/{first_ts.to_timestamp() // 1000}_{last_ts.to_timestamp() // 1000}_{completed}.csv"
        )