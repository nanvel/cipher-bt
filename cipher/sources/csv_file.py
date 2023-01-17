import csv
import datetime
from pathlib import Path
from typing import Optional

from ..models import Time
from .base import Source


class CsvFileSource(Source):
    DEFAULT_TS_FORMAT = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d")

    def __init__(
        self, path: str, ts_format: Optional[str] = None, delimiter: str = ","
    ):
        path = Path() / path
        assert path.is_file()

        self.path = path
        self.delimiter = delimiter

        self.ts_format = ts_format or self._ts_format_from_file(
            path
        )  # s, ms, <datetime format>
        assert self.ts_format

    @property
    def slug(self) -> str:
        return f"csv_file/{self.path.stem}"

    def load(self, ts: Time, path: Path) -> (Time, Time, bool):
        first_ts = None
        last_ts = None
        with self.path.open("r", encoding="utf-8") as source_f:
            reader = csv.reader(source_f, delimiter=self.delimiter)
            with path.open("w", encoding="utf-8") as target_f:
                writer = csv.writer(target_f)
                for n, row in enumerate(reader):
                    if n == 0:
                        writer.writerow(["ts"] + row[1:])
                        continue
                    ts = self._to_ts(row[0])
                    first_ts = first_ts or ts
                    last_ts = ts
                    writer.writerow([int(ts)] + row[1:])

        if ts < first_ts or ts > last_ts:
            raise AssertionError("No data for the specified time.")

        return (
            first_ts,
            last_ts,
            True,
        )

    def _to_ts(self, ts_str):
        if self.ts_format == "ms":
            return int(ts_str) // 1000
        elif self.ts_format == "s":
            return int(ts_str)
        else:
            return Time.from_datetime(
                datetime.datetime.strptime(ts_str, self.ts_format)
            )

    def _detect_ts_format(self, ts_str: str) -> str:
        try:
            ts = int(ts_str)

            if ts > 157766400000:  # 1975 year, ms
                return "ms"
            return "s"
        except ValueError:
            pass

        for fmt in self.DEFAULT_TS_FORMAT:
            try:
                datetime.datetime.strptime(ts_str, fmt)
                return fmt
            except ValueError:
                continue

    def _ts_format_from_file(self, path: Path) -> str:
        with path.open("r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=self.delimiter)
            next(reader)
            row = next(reader)

        return self._detect_ts_format(row[0])
