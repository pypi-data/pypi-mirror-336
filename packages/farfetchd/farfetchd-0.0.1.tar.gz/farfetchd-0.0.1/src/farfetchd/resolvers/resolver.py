import abc

from typing import List, TypeVar, overload

from ..models.generic import NamedAPIResourceList
from ..resources import CacheableResource, CacheableResourceList


T = TypeVar("T")


class Resolver(abc.ABC):
    @overload
    async def resolve(self, to_resolve: CacheableResource[T]) -> T | None:
        ...

    @overload
    async def resolve(
        self, to_resolve: CacheableResourceList[T]
    ) -> NamedAPIResourceList[T] | None:
        ...

    @abc.abstractmethod
    async def resolve(
        self, to_resolve: CacheableResource[T] | CacheableResourceList[T]
    ) -> T | NamedAPIResourceList[T] | None:
        raise NotImplementedError()

    async def store(self, to_store: T | List[T]):
        pass
