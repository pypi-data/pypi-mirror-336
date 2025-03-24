from ..decorator import chainable
from ..middleware import MiddlewareBase


class RedisMiddleware(MiddlewareBase):
    '''
    RedisMiddleware - middleware for connecting to Redis.
    '''

    name = 'redis'
    dependency = ['redis']

    _config: dict[str, int | str | None] = {}

    @classmethod
    def config(
        cls, *, host: str = 'localhost', port: int = 6379, **kwargs
    ) -> type['RedisMiddleware']:
        cls._config = {'host': host, 'port': port, **kwargs}

        return cls

    @chainable
    async def create(self) -> 'RedisMiddleware':
        try:
            import redis.asyncio as redis
        except ImportError:
            self.log('Redis package not found, please install it')
        else:
            self._client: redis.Redis = await redis.Redis(**self._config)

            self.bind_object(RedisMiddleware.name, self._client)

            self.log(f'Redis initialized: {await self._client.ping()}')

    @chainable
    async def destroy(self) -> 'RedisMiddleware':
        await self._client.aclose()

        self.log('Redis connection closed')
