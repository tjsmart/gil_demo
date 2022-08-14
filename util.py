# https://www.youtube.com/watch?v=6g79qGQo2-Q
from __future__ import annotations

from concurrent.futures import as_completed
from functools import wraps
from time import monotonic
from typing import Callable
from typing import TYPE_CHECKING
from typing import TypeVar

if TYPE_CHECKING:
    from typing import ParamSpec

    _In = ParamSpec("_In")

_Out = TypeVar("_Out")


def _time_it(func: Callable[_In, _Out]) -> Callable[_In, _Out]:
    @wraps(func)
    def wrapper(*args: _In.args, **kwargs: _In.kwargs) -> _Out:
        t0 = monotonic()
        rslt = func(*args, **kwargs)
        print(f"{func.__name__} finished in {monotonic() - t0}")
        return rslt

    return wrapper


@_time_it
def execute(executor, work: Callable) -> int:
    timed_work = _time_it(work)
    with executor(4) as pool:
        futures = [pool.submit(timed_work) for _ in range(20)]

        for future in as_completed(futures):
            print(f"{future.result()=}")

    return 0
