import functools
import time
from typing import Callable, Any


def async_timed():
    def wrapper(func: Callable):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            print(f'Выполняется  {func} c аргументами {args}, {kwargs}')
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                total = end - start
                print(f'{func} завершилась за {total:.4f} (сек.)')

        return wrapped

    return wrapper


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {(end_time - start_time):.6f} seconds to run.")
        return result

    return wrapper
