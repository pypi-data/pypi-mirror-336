import threading
from collections.abc import Callable
from json import loads, dumps
from pathlib import Path
from typing import Any, TypeAlias

from ..decorator import chainable
from ..middleware import MiddlewareBase
from ..mixins import DebugMixin, LoggingMixin


StateType: TypeAlias = dict[str, Any]
ListenerType: TypeAlias = Callable[[dict[str, Any]], None]


class State(DebugMixin, LoggingMixin):
    def config(
        self,
        initial_state: StateType | None = None,
        state_file: str | None = None,
    ) -> None:
        if initial_state is None:
            initial_state = {}

        self.initial_state = initial_state
        self.state_file = state_file

        self._state_lock: threading.Lock = threading.Lock()
        self._listener_lock: threading.Lock = threading.Lock()
        self._listeners: list[ListenerType] = []
        self._state: StateType = {**self.initial_state}

    def get_state(self) -> StateType:
        with self._state_lock:
            return self._state.copy()

    def set_state(self, partial_state: StateType) -> None:
        with self._state_lock:
            self._state = {**self._state, **partial_state}

            with self._listener_lock:
                listeners = self._listeners.copy()

        for listener in listeners:
            try:
                listener(self._state)
            except Exception as e:
                self.log(
                    f'error triggering listener[{listener.__name__}]: {e}',
                    level='error',
                )

    def add_listener(self, listener: ListenerType) -> None:
        with self._listener_lock:
            self._listeners.append(listener)

    def remove_listener(self, listener: ListenerType) -> None:
        with self._listener_lock:
            if listener in self._listeners:
                self._listeners.remove(listener)

    def load(self) -> None:
        if not self.state_file or not Path(self.state_file).exists():
            self._state = {**self.initial_state}

            return

        try:
            if content := Path(self.state_file).read_text():
                if self.initial_state:
                    self._state = {**self.initial_state, **loads(content)}
                else:
                    self._state = loads(content)
        except Exception as e:
            self.log(f'failed to load state from file: {e}', level='error')
            self._state = self.initial_state.copy()
        else:
            self.log(f'state loaded from file: {self.state_file}')

    def dump(self) -> None:
        if self.state_file:
            try:
                Path(self.state_file).write_text(dumps(self._state))
            except Exception as e:
                self.log(f'failed to save state to file: {e}', level='error')
            else:
                self.log(f'state saved to file: {self.state_file}')


class StateMiddleware(MiddlewareBase):
    '''
    StateMiddleware - middleware for managing a shared state across tasks.
    '''

    name = 'state'

    _config: dict[str, dict | str] = {}
    _state = State()

    @classmethod
    def config(
        cls,
        initial_state: StateType | None = None,
        state_file: str | None = None,
    ):
        cls._config = {
            'initial_state': initial_state,
            'state_file': state_file,
        }
        cls._state.config(**cls._config)

    @chainable
    async def create(self):
        self.bind_object(StateMiddleware.name, self._state)
        self._state.load()

    @chainable
    async def destroy(self):
        self._state.dump()
