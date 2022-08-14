def python_work() -> int:
    x = 0
    for _ in range(10_000_000):
        x += 1
    return x
