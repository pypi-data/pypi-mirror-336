import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s::%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger('garden')


class LoggingMixin:
    '''
    LoggingMixin is a mixin class that provides logging functionalities.
    '''

    def _get_debug(self) -> bool:
        '''
        Returns the debug value of the object.
        '''
        return getattr(self, 'debug', False)

    def get_logger(self) -> logging.Logger:
        '''
        Returns the logger object of the class.
        '''
        return logger

    def log(self, message: str, level: str = 'info') -> None:
        if name := getattr(self, 'name', None):
            name = f'[{name}]'

        if not (entity_type := getattr(self, 'entity_type', None)):
            entity_type = self.__class__.__name__

        if self._get_debug() and level == 'error':
            level = 'exception'

        if not isinstance(message, str):
            message = str(message)

        getattr(logger, level)(
            ' '.join(filter(bool, [entity_type, name, message]))
        )
