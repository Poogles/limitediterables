# Limited Iterables

Basic library to rate limit how quickly you get the next value out of an iterable.

## Example

```python
target = range(100)
slow_iter = LimitedIterable(target, limit=50)  # This gives us 50 messages a second.

for i in slow_iter:
	print(i)

```

Should be useful for rate limiting against APIs or anything else that's sensitive to number of requests.
