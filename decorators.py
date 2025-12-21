from __future__ import annotations

import time
from functools import wraps
from typing import Callable


def measure_time[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    """関数の実行時間を計測し、標準出力するデコレータ"""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Finished '{func.__name__}' in {end_time - start_time:.4f} secs")
        return result

    return wrapper
