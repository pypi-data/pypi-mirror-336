from typing import Any
from ..decorator import chainable
from ..middleware import MiddlewareBase


class MongoMiddleware(MiddlewareBase):
    '''
    MongoMiddleware - middleware for connecting to Mongo.
    '''

    name = 'mongo'
    dependency = ['pymongo']

    _config: dict[str, Any] = {}

    @classmethod
    def config(
        cls, *, host: str = 'localhost', port: int = 27017, **kwargs
    ) -> type['MongoMiddleware']:
        cls._config = {'host': host, 'port': port, **kwargs}

        return cls

    @chainable
    async def create(self) -> 'MongoMiddleware':
        try:
            from pymongo import AsyncMongoClient
        except ImportError:
            self.log('Mongo package not found, please install it')
        else:
            self._client: AsyncMongoClient = AsyncMongoClient(**self._config)

            self.bind_object(MongoMiddleware.name, self._client)

            info = await self._client.server_info()

            self.log(f'Mongo initialized: {info['version']}')

    @chainable
    async def destroy(self) -> 'MongoMiddleware':
        await self._client.close()

        self.log('Mongo connection closed')
