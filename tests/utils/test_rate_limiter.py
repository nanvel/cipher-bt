import time

from cipher.utils import RateLimiter


def test_rate_limiter():
    rate_limiter = RateLimiter(calls_per_seconds=4.0)

    times = []
    for i in range(3):
        start_time = time.monotonic()
        with rate_limiter():
            pass
        times.append(time.monotonic() - start_time)

    assert times[1] > times[0]
    assert times[0] < 0.1
    assert times[1] > 0.2
    assert times[2] > 0.2
