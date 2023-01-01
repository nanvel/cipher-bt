import tempfile
from pathlib import Path
from typing import List

from ..models import Datas, Time
from ..sources import Source


class DatasFactory:
    def __init__(self, cache_root: Path):
        self.cache_root = cache_root

    def from_sources(self, sources: List[Source], start_ts: Time, stop_ts: Time):
        """Load what is missing in cache, create dataframes from csvs and concat, truncate."""
        # datas = Datas()

        for source in sources:
            with tempfile.TemporaryDirectory() as path:
                tmp_path = Path(path) / "example.csv"
                first_ts, last_ts = source.load(ts=start_ts, path=tmp_path)
                print(tmp_path, first_ts, last_ts)

        # pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)
        # assert datas.data_frames

        # return datas

    def _find_cached(self, ts: Time):
        """Find what we already have cached for the time range."""
        pass
