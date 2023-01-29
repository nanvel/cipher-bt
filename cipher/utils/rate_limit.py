import time

from contextlib import contextmanager


class RateLimiter:
    def __init__(self, calls_per_seconds: float):
        self.last_call_ts = time.monotonic() - (1 / calls_per_seconds) * 2
        self.calls_per_second = calls_per_seconds

    @contextmanager
    def __call__(self):
        now = time.monotonic()
        to_wait = self.last_call_ts - now + (1 / self.calls_per_second)
        if to_wait > 0:
            time.sleep(to_wait)
            now = time.monotonic()
        try:
            yield
        finally:
            self.last_call_ts = now
