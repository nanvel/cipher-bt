import logging
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from ..models import Time
from ..sources import Source


logger = logging.getLogger(__name__)


class DataService:
    def __init__(self, cache_root: Path):
        if cache_root.exists():
            assert cache_root.is_dir()
        else:
            assert cache_root.parent.exists()
            cache_root.mkdir()

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
                first_ts, last_ts, p, completed = self._load_from_source(
                    source=source, ts=ts
                )

            paths.append(p)

            if not completed:
                break

            if last_ts >= stop_ts:
                break
            else:
                ts = last_ts + (last_ts - first_ts) / 2

        df = pd.concat(
            (pd.read_csv(p) for p in paths), ignore_index=True
        ).drop_duplicates(subset=["ts"])

        return (
            df[(df.ts >= start_ts) & (df.ts < stop_ts)]
            .astype({"ts": "datetime64[s]"})
            .set_index("ts")
        )

    def _load_from_source(self, source: Source, ts: Time) -> (Time, Time, Path, bool):
        temp_path = self.cache_root / self._build_temp_path(prefix=source.slug, ts=ts)
        temp_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            first_ts, last_ts, completed = source.load(ts=ts, path=temp_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise

        if completed:
            incomplete_path = self.cache_root / self._build_path(
                prefix=source.slug,
                first_ts=first_ts,
                last_ts=last_ts,
                completed=False,
            )
            if incomplete_path.exists():
                incomplete_path.unlink()

        logger.info(f"Loaded from {source.slug} {first_ts}..{last_ts}")

        return (
            first_ts,
            last_ts,
            temp_path.rename(
                self.cache_root
                / self._build_path(
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
        second = ts
        for p in (self.cache_root / prefix).glob("*.csv"):
            try:
                first_ts, last_ts = p.stem.split("_")

                if not last_ts:
                    continue

                first_ts = int(first_ts)
                last_ts = int(last_ts)

                if first_ts <= second <= last_ts:
                    return (
                        Time(first_ts),
                        Time(last_ts),
                        p,
                    )
            except ValueError:
                pass

    def _build_temp_path(self, prefix: str, ts: Time):
        return prefix + f"/{int(ts)}.csv"

    def _build_path(self, prefix: str, first_ts: Time, last_ts: Time, completed: bool):
        return (
            prefix
            + f"/{int(first_ts)}_"
            + (f"{int(last_ts)}.csv" if completed else ".csv")
        )
