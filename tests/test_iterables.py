import time

from limitediterables import LimitedIterable


def test_rate_limit():

    # Create dummy range of numbers.
    target = range(100)

    slow_iter = LimitedIterable(target, limit=50)

    start_time = time.perf_counter()
    consumed_target = [i for i in slow_iter]
    end_time = time.perf_counter()

    expected = [i for i in target]

    assert consumed_target == expected, "Check to see results are correct."
    time_taken = end_time - start_time
    assert time_taken > 1.9, "Check to see rate limit works low."
    assert time_taken < 2.1, "Check to see rate limit works high."
