import pkg_resources
from typing import Any, cast

from .decorator import chainable
from .mixins import DebugMixin, LoggingMixin, QueueMixin


class MiddlewareObject: ...


class MiddlewareMixin:
    '''
    MiddlewareMixin is a mixin class that provides middleware functionalities.
    '''

    _objects = MiddlewareObject()

    @property
    def objects(self) -> MiddlewareObject:
        return self._objects

    def bind_object(self, key: str, obj: Any) -> None:
        '''
        Binds the given object to the MiddlewareObject.
        '''
        if hasattr(self.objects, key):
            raise AttributeError(
                f"Attribute {key} already exists in MiddlewareObject."
            )

        setattr(self.objects, key, obj)


class MiddlewareMeta(type):
    '''
    MiddlewareMeta is where it keeps all the middlewares.
    '''

    middlewares: dict[str, type['MiddlewareBase']] = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)

        if cls.name is None:
            cls.name = cls.__name__

        if not cast(str, name).strip():
            name = cls.name

        if (
            cls.__name__ != 'MiddlewareBase'
            and name not in MiddlewareMeta.middlewares
        ):
            MiddlewareMeta.middlewares[name] = cls


class MiddlewareBase(
    DebugMixin, LoggingMixin, MiddlewareMixin, metaclass=MiddlewareMeta
):
    '''
    MiddlewareBase is the template of all middlewares.
    All middlewares should have inherit from this class.

    Attributes:

        - name: str | None = None
            The name of the middleware.
        - entity_type: str = 'Middleware'
            The entity type of the middleware.
        - dependencies: list[str] = []
            Any dependencies this middleware might need. Accept all pip formats:

            e.g.

            ```python
            dependencies = ['pip', 'wheel==10.2.3']
            ```

            The app will check whether `pip` and `wheel` with version equal
                to `10.2.3` are installed, if not, it will message in the logs.
            If the middleware has no dependencies, you can simply ignore it.
    '''

    name: str | None = None
    entity_type: str = 'Middleware'
    dependencies: list[str] = []

    @classmethod
    def config(cls, *args, **kwargs) -> None:
        '''
        Accepts anything that you would like to pass to the middleware
            as configurations.
        '''

    @chainable
    async def create(self) -> 'MiddlewareBase':
        '''
        Creates the middleware instance.
        '''

    @chainable
    async def destroy(self) -> 'MiddlewareBase':
        '''
        Destroys the middleware instance.
        '''


class MiddlewareManager(DebugMixin, LoggingMixin, MiddlewareMixin, QueueMixin):
    '''
    MiddlewareManager is the bridge between the Gardener and all middlewares.

    Attributes:

        - _instances: dict[str, MiddlewareBase] = {}
            Stores all the middleware instances.
    '''

    _instances: dict[str, MiddlewareBase] = {}

    @property
    def middlewares(self) -> dict[str, type[MiddlewareBase]]:
        return MiddlewareMeta.middlewares

    def check_dependency(self) -> None:
        has_missing_dependency = False
        version_match_phrase = {
            '<=': 'less than or equal to',
            '>=': 'greater than or equal to',
            '!=': 'not equal to',
            '==': 'equal to',
            '~=': 'compatible version limit',
            '<': 'less than',
            '>': 'greater than',
        }

        for name, cls in self.middlewares.items():
            missing_dependency: list[str] = []

            for dependency in cls.dependencies:
                version_cmp: str | None = None
                package_version: str | None | pkg_resources.parse_version

                for cmp in version_match_phrase.keys():
                    if cmp in dependency:
                        package_name, package_version = (
                            dependency.split(cmp)
                            if cmp in dependency
                            else (dependency, None)
                        )
                        version_cmp = cmp

                        break
                    else:
                        package_name, package_version = dependency, None

                try:
                    __import__(package_name)

                    if package_version is not None:
                        version = pkg_resources.get_distribution(
                            package_name
                        ).version
                        version = pkg_resources.parse_version(version)
                        package_version = pkg_resources.parse_version(
                            cast(str, package_version)
                        )

                        if version_cmp is not None and (
                            eval(f'{version} {version_cmp} {package_version}')
                        ):
                            missing_dependency.append(
                                f'Package "{package_name}" version ({version})'
                                f' is {version_match_phrase[version_cmp]} '
                                f'the required version ({package_version}).'
                            )
                except ImportError:
                    missing_dependency.append(
                        f'Package "{package_name}" is not installed.'
                    )
                except pkg_resources.DistributionNotFound:
                    missing_dependency.append(
                        f'Package "{package_name}" is not found'
                        ' in the current environment.'
                    )

            if missing_dependency:
                has_missing_dependency = True

                self.log(
                    f'Missing dependencies for middlewares[{name}]', 'error'
                )

                for message in missing_dependency:
                    self.log(message, 'error')

        if has_missing_dependency:
            raise ImportError('Dependency unresolved')

    async def register(self) -> None:
        self.check_dependency()

        try:
            for name, cls in MiddlewareMeta.middlewares.items():
                self.log(f'registering middlewares[{name}]')

                self._instances[name] = await cls().create()
        except Exception as e:
            self.log('encountered error while registering middlewares')

            await self.deregister()

            raise e

    async def deregister(self) -> None:
        try:
            for name, ins in self._instances.items():
                self.log(f'deregistering middlewares[{name}]')

                await ins.destroy()
        except Exception as e:
            self.log('encountered error while deregistering middlewares')

            raise e
