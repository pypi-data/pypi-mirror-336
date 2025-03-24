import functools
import inspect
from collections.abc import Callable


def chainable(func: Callable) -> Callable:
    '''
    A decorator that makes a class method chainable.
    '''

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        if inspect.isawaitable(result):

            async def async_wrapper():
                res = await result

                if res is None or res is self:
                    return self
                else:
                    return res

            return async_wrapper()
        else:
            if result is None or result is self:
                return self
            else:
                return result

    return wrapper
