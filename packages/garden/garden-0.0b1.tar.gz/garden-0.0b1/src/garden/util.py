import inspect
from collections.abc import Callable, Coroutine
from typing import Any, TypeVar, TypeAlias


T = TypeVar('T')

AsyncOrSyncReturns: TypeAlias = T | Coroutine[Any, Any, T]


async def universal_execute(
    func: Callable[..., AsyncOrSyncReturns], *args, **kwargs
) -> AsyncOrSyncReturns:
    '''
    Execute a function asynchronously or synchronously.
    '''
    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    else:
        return func(*args, **kwargs)
