import time
from unittest.mock import MagicMock

import limitediterables.iterables as iterables


def test_rate_limit():
    """Test the rate limiting returns the same values as the parent."""

    # Create dummy range of numbers.
    target = range(100)

    slow_iter = iterables.LimitedIterable(target, limit=50)

    start_time = time.perf_counter()
    consumed_target = [i for i in slow_iter]
    end_time = time.perf_counter()

    expected = [i for i in target]

    assert consumed_target == expected, "Check to see results are correct."
    time_taken = end_time - start_time
    assert time_taken > 1.9, "Check to see rate limit works low."
    assert time_taken < 2.1, "Check to see rate limit works high."


def test_rate_limit_negative():
    """Test the rate limiting returns the same values as the parent."""

    # Create dummy range of numbers.
    target = range(100)

    slow_iter = iterables.LimitedIterable(target, limit=-50)

    start_time = time.perf_counter()
    consumed_target = [i for i in slow_iter]
    end_time = time.perf_counter()

    expected = [i for i in target]

    assert consumed_target == expected, "Check to see results are correct."
    time_taken = end_time - start_time
    assert time_taken > 1.9, "Check to see rate limit works low."
    assert time_taken < 2.1, "Check to see rate limit works high."


def test_actual_rate_slower_than_rate_limit():
    """Test to check we don't limit a iterator if it's slower already."""

    # Create dummy range of numbers.
    target = range(10)

    # Limit is set to be 100 second, with a range of 10
    # that would result in the list being consumed in 0.1s
    slow_iter = iterables.LimitedIterable(target, limit=100)

    start_time = time.perf_counter()
    # For each iteration sleep 0.3, for 10 iterations thats
    # 3 seconds total sleep time.
    consumed_target = []
    for i in slow_iter:
        time.sleep(0.3)
        consumed_target.append(i)
    end_time = time.perf_counter()

    expected = [i for i in target]
    time_taken = end_time - start_time
    assert consumed_target == expected, "Check to see results are correct."
    assert time_taken > 2.9, "Check to see rate limit works low."
    assert time_taken < 3.1, "Check to see rate limit works high."


def test_no_limit():
    """Test passing in no rate limit works."""

    target = range(10000)
    slow_iter = iterables.LimitedIterable(target)

    expected = [i for i in target]
    iterables.time.sleep = MagicMock()
    consumed_target = [i for i in slow_iter]

    assert consumed_target == expected, "Check to see results are correct."
    assert iterables.time.sleep.call_count == 0, "Sleep not called."
