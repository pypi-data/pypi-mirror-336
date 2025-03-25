import threading
import logging

from typing import TypeVar, overload

import aiohttp


from .resolver import Resolver
from ..models.generic import NamedAPIResourceList
from ..resources import CacheableResource, CacheableResourceList
from ..serialization import Deserializer

T = TypeVar("T")


logger = logging.getLogger(__name__)


class ApiResolver(Resolver):
    def __init__(self, deserializer: Deserializer) -> None:
        self.__session_lock = threading.Lock()
        self.__session: aiohttp.ClientSession | None = None
        self._deserializer = deserializer

    async def _session(self) -> aiohttp.ClientSession:
        if not self.__session:
            with self.__session_lock:
                if not self.__session:
                    logger.info("initializing session")
                    self.__session = aiohttp.ClientSession()
        return self.__session

    @overload
    async def resolve(self, to_resolve: CacheableResource[T]) -> T | None:
        ...

    @overload
    async def resolve(
        self, to_resolve: CacheableResourceList[T]
    ) -> NamedAPIResourceList[T] | None:
        ...

    async def resolve(
        self, to_resolve: CacheableResource[T] | CacheableResourceList[T]
    ) -> T | NamedAPIResourceList[T] | None:

        session = await self._session()

        query = {}
        data_type = to_resolve.resource_type
        if isinstance(to_resolve, CacheableResourceList):
            query = {
                "offset": to_resolve.pagination.offset,
                "limit": to_resolve.pagination.limit,
            }
            data_type = NamedAPIResourceList
        query = {k: v for k, v in query.items() if v is not None}
        logger.info("fetching %s w/ args %s", to_resolve.resource_url, query)
        async with session.get(to_resolve.resource_url, params=query) as resp:
            data = await resp.json()
            return self._deserializer.from_dict(data_type, data)
