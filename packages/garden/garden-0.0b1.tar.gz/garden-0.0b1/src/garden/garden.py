import asyncio
import inspect
import random
import signal
import sys
from collections.abc import Callable, Iterable
from enum import Enum
from typing import Any, cast

from .middleware import MiddlewareMixin, MiddlewareManager
from .mixins import DebugMixin, LoggingMixin, QueueMixin
from .util import universal_execute as ue


class HedgehogStatus(Enum):
    '''
    HedgehogStatus is an enumeration of the possible states of a Hedgehog.

    - CREATED: Hedgehog has been created.
    - RUNNING: Hedgehog is running.
    - PAUSED: Hedgehog is paused by Gardener.
    - TERMINATING: Hedgehog is preparing to be terminated.
    - TERMINATED: Hedgehog has been terminated.
    '''

    CREATED = 'CREATED'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    TERMINATING = 'TERMINATING'
    TERMINATED = 'TERMINATED'


class Hedgehog(DebugMixin, LoggingMixin, MiddlewareMixin):
    '''
    Hedgehog is a lightweight asynchronous worker for running tasks.

    Parameters:

    - name: str = 'Hedgehog'
        Name of the Hedgehog.
    - delay: tuple | int | float = 0
        Delay before the Hedgehog starts running.
            When tuple, it will be a random value between the two values.
    - interval: tuple | int | float = 0
        Interval between each run of the Hedgehog.
            When tuple, it will be a random value between the two values.
    - repeat: bool | int = True
        Whether the Hedgehog should repeat the task.
            When False, the Hedgehog will run the task only once.
    - error_tolerance: int = 0
        Number of errors the Hedgehog can tolerate before terminating.
    - task: Callable[..., None] | None = None,
        The task that the Hedgehog runs.
    '''

    def __init__(
        self,
        *,
        name: str = 'Hedgehog',
        delay: tuple | int | float = 0,
        interval: tuple | int | float = 0,
        repeat: bool | int = True,
        error_tolerance: int = 0,
        task: Callable[..., None] | None = None,
    ) -> None:
        self.name = name
        self.delay = delay
        self.interval = interval
        self.repeat = repeat
        self.error_tolerance = error_tolerance
        self.task = task

        self.run_count: int = 0
        self.error_count: int = 0
        self.gardener: Gardener | None = None
        self.status: HedgehogStatus = HedgehogStatus.CREATED

    def _propagate_status(self) -> None:
        '''
        Called upon Hedgehog's status change.
        '''
        self.log(self.status.value.lower())

    @property
    def gardener(self) -> 'Gardener | None':
        return self._gardener

    @gardener.setter
    def gardener(self, value: 'Gardener | None') -> None:
        self._gardener = value

    @property
    def status(self) -> HedgehogStatus:
        return self._status

    @status.setter
    def status(self, value: HedgehogStatus) -> None:
        if getattr(self, '_status', None) != value:
            self._status = value
            self._propagate_status()
        else:
            self._status = value

    @property
    def siblings(self) -> Iterable['Hedgehog']:
        '''
        Returns all siblings of the Hedgehog, i.e. the replicas.
        '''
        return filter(
            lambda h: h.task is self.task,
            cast(Gardener, self.gardener).hedgehogs,
        )

    def pause(self) -> None:
        self.status = HedgehogStatus.PAUSED

    def resume(self) -> None:
        self.status = HedgehogStatus.RUNNING

    def terminate(self) -> None:
        self.status = HedgehogStatus.TERMINATING

    async def run(self, *args, **kwargs) -> None:
        if isinstance(self.delay, tuple):
            delay = random.uniform(*self.delay)
        else:
            delay = max(0, self.delay)

        if delay > 0:
            self.status = HedgehogStatus.PAUSED

            self.log(f'starting to run in {delay:.2f} seconds')

            await asyncio.sleep(delay)

        self.status = HedgehogStatus.RUNNING

        while True:
            while self.error_count <= self.error_tolerance:
                try:
                    await ue(
                        cast(Gardener, self.gardener).before_each_run, self
                    )

                    if inspect.iscoroutinefunction(self.task):
                        await self.task(self.gardener, self, *args, **kwargs)
                    else:
                        cast(Callable, self.task)(
                            self.gardener, self, *args, **kwargs
                        )

                    self.run_count += 1

                    await ue(
                        cast(Gardener, self.gardener).after_each_run, self
                    )

                    if (
                        isinstance(self.repeat, int)
                        and self.run_count >= self.repeat
                    ):
                        break
                except Exception as e:
                    self.error_count += 1

                    self.log(
                        message=f'has encountered an error: {e}',
                        level='error',
                    )
                else:
                    break
            else:
                self.status = HedgehogStatus.TERMINATING

                self.log(
                    message='met error tolerance limit, terminating',
                    level='warning',
                )

            while self.status == HedgehogStatus.PAUSED:
                await asyncio.sleep(1)

            if isinstance(self.repeat, bool) and not self.repeat:
                self.status = HedgehogStatus.TERMINATED
                break
            if isinstance(self.repeat, int) and self.run_count >= self.repeat:
                self.status = HedgehogStatus.TERMINATED
                break

            if isinstance(self.interval, tuple):
                await asyncio.sleep(random.uniform(*self.interval))
            else:
                await asyncio.sleep(max(0, self.interval))

            if self.status == HedgehogStatus.TERMINATING:
                self.status = HedgehogStatus.TERMINATED
                break


class GardenerStatus(Enum):
    '''
    GardenerStatus is an enumeration of the possible states of a Gardener.

    - INITIATED: Gardener has been initialized.
    - PREPARING: Gardener is preparing for the necessary configurations.
    - READY: Gardener is ready to run.
    - RUNNING: Gardener is running.
    - PAUSED: Gardener is paused by the user or a signal.
    - SUSPENDED: Gardener is suspended by the program.
    - STOPPED: Gardener is preparing to be terminated.
    - TERMINATED: Gardener has been terminated.
    '''

    INITIATED = 'INITIATED'
    PREPARING = 'PREPARING'
    READY = 'READY'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    SUSPENDED = 'SUSPENDED'
    STOPPED = 'STOPPED'
    TERMINATED = 'TERMINATED'


class Gardener(DebugMixin, LoggingMixin, MiddlewareMixin, QueueMixin):
    '''
    Gardener is a manager for Hedgehog instances, a singleton class.
    It will automatically create the Hedgehog instances based on the tasks.
    And also manage the lifecycle of the Hedgehog instances.

    Attributes:

        - _hedgehogs: list[Hedgehog] = []
            The list of Hedgehog instances.
        - _instances: dict[type['Gardener'], 'Gardener'] = {}
            A dictionary to store the singleton instance of Gardener.
        - debug = False
            The global debug switch.
    '''

    _hedgehogs: list[Hedgehog] = []
    _instances: dict[type['Gardener'], 'Gardener'] = {}

    @classmethod
    def add_hedgehog(cls, hedgehog: Hedgehog) -> None:
        cls._hedgehogs.append(hedgehog)

    @classmethod
    def task(
        cls,
        name: str | None = None,
        *,
        delay: tuple | int | float = 0,
        interval: tuple | int | float = 0,
        repeat: bool | int = True,
        error_tolerance: int = 0,
        replica: int = 1,
    ) -> Callable:
        '''
        Decorator to add a task to the Gardener as a Hedgehog.
        '''

        def decorator(func: Callable[..., None]) -> None:
            if (task_name := name) is None:
                task_name = func.__name__

            for i in range(replica):
                task_name_ = task_name

                if replica > 1:
                    task_name_ = f'{task_name} [replica:{i + 1}]'

                cls.add_hedgehog(
                    Hedgehog(
                        name=task_name_,
                        delay=delay,
                        interval=interval,
                        repeat=repeat,
                        error_tolerance=error_tolerance,
                        task=func,
                    )
                )

        return decorator

    def __new__(cls, *args, **kwargs) -> 'Gardener':
        if cls not in cls._instances:
            cls._instances[cls] = super(Gardener, cls).__new__(cls)

        return cls._instances[cls]

    def __init__(self, name: str = 'Gardener') -> None:
        self.name = name
        self.status = GardenerStatus.INITIATED

        signal.signal(signal.SIGINT, self._handle_interrupt)

    def _handle_interrupt(self, *args, **kwargs) -> None:
        '''
        Handles the interrupt signal by pausing the Gardener.
        '''
        self.status = GardenerStatus.PAUSED

        self.log('interrupted, pausing...', level='warning')

        action = input('Press "c" to continue or any other key to exit:')

        if action.lower() == 'c':
            self.log('continuing...')
            self.status = GardenerStatus.RUNNING
        else:
            self.log('exiting program', level='warning')
            self.status = GardenerStatus.STOPPED

    def _propagate_status(self) -> None:
        '''
        Called upon Gardener's status change
        '''
        self.log(self.status.value.lower())

        match self.status:
            case GardenerStatus.RUNNING:
                for h in self.hedgehogs:
                    h.resume()
            case GardenerStatus.PAUSED:
                for h in self.hedgehogs:
                    h.pause()
            case GardenerStatus.STOPPED:
                for h in self.hedgehogs:
                    if h.status not in (
                        HedgehogStatus.TERMINATING,
                        HedgehogStatus.TERMINATED,
                    ):
                        h.terminate()

    async def _status_monitoring(self) -> None:
        '''
        Monitors the status of all Hedgehogs and updates the Gardener
        '''
        if all(
            [h.status == HedgehogStatus.TERMINATED for h in self.hedgehogs]
        ):
            self.status = GardenerStatus.STOPPED

            await self.add_task(self.stop())
        else:
            await asyncio.sleep(0.5)

            await self.add_task(self._status_monitoring())

    @property
    def hedgehogs(self) -> list[Hedgehog]:
        return self._hedgehogs

    @property
    def status(self) -> GardenerStatus:
        return self._status

    @status.setter
    def status(self, value: GardenerStatus) -> None:
        if getattr(self, '_status', None) != value:
            self._status = value
            self._propagate_status()
        else:
            self._status = value

    def start(self) -> None:
        '''
        Starts the garden routine.
        '''
        asyncio.run(self.run_until_complete())

    async def stop(self) -> None:
        '''
        Stops the garden routine and clean up.
        '''
        await ue(self.post_execution)

        try:
            await self.middleware_manager.deregister()
        except Exception as e:
            self.log(f'has encountered an error: {e}', level='error')

        await self.add_task(None)

    async def run_until_complete(self) -> None:
        self.status = GardenerStatus.PREPARING
        self.middleware_manager = MiddlewareManager()

        try:
            await self.middleware_manager.register()
        except Exception as e:
            self.log(f'has encountered an error: {e}', level='error')

            sys.exit(1)
        else:
            self.status = GardenerStatus.READY

        for h in self.hedgehogs:
            h.gardener = self

        await ue(self.pre_execution)

        self.status = GardenerStatus.RUNNING

        try:
            tasks = [h.run() for h in self.hedgehogs]

            await self.add_task(asyncio.gather(*tasks))
            await self.add_task(self._status_monitoring())
        except Exception as e:
            self.log(f'has encountered an error: {e}', level='error')

        while True:
            task = await self.queue.get()

            if task is None:
                self.status = GardenerStatus.TERMINATED
                self.queue.task_done()
                break

            if inspect.iscoroutine(task):
                await task

            self.queue.task_done()

        await self.queue.join()

        self.log('exited')

        sys.exit(0)

    def before_each_run(self, hedgehog: Hedgehog) -> Any: ...

    def after_each_run(self, hedgehog: Hedgehog) -> Any: ...

    def pre_execution(self) -> Any: ...

    def post_execution(self) -> Any: ...
