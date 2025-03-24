import asyncio
from typing import Any


class QueueMixin:
    '''
    QueueMixin is a mixin class that provides the common queue instance.
    '''

    _queue: asyncio.Queue = asyncio.Queue()

    @property
    def queue(self) -> asyncio.Queue:
        return self._queue

    async def add_task(self, task: Any) -> None:
        await self._queue.put(task)
