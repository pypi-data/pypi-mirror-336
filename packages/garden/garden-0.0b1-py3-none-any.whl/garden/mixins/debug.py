from ..decorator import chainable


class DebugMixin:
    '''
    DebugMixin is a mixin class that provides the common debug information.
    '''

    _debug: bool = False

    @property
    def debug(self) -> bool:
        return DebugMixin._debug

    @chainable
    def enable_debug(self) -> None:
        DebugMixin._debug = True

    @chainable
    def disable_debug(self) -> None:
        DebugMixin._debug = False
