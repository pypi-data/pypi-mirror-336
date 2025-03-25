import asyncio
import collections
import threading

from typing import (
    Callable,
    Deque,
    List,
    ParamSpec,
    Tuple,
    Type,
    TypeVar,
    TypedDict,
    overload,
)

from .models.generic import NamedAPIResourceList
from .resolvers import Resolver
from .resources import CacheableResource, CacheableResourceList

T = TypeVar("T")
P = ParamSpec("P")


class Registry:
    def __init__(self) -> None:
        self._registry_lock = threading.Lock()
        self._registry: TypedDict[Type, Callable] = {}

    def register(
        self,
        registered_type: Type[T],
        provider: Callable[P, CacheableResource[T] | CacheableResourceList[T]],
    ) -> None:
        with self._registry_lock:
            if registered_type in self._registry:
                raise ValueError(
                    f"provider for type {registered_type} already registered"
                )
            self._registry[registered_type] = provider

    def get(
        self, type_to_get: Type[T]
    ) -> Callable[P, CacheableResource[T] | CacheableResourceList[T]] | None:
        with self._registry_lock:
            return self._registry.get(type_to_get)


class ResolverRegistry:
    def __init__(self) -> None:
        self._registry_lock = threading.Lock()
        self._registry: List[Tuple[int, Resolver]] = []

    def register(self, priority: int, resolver: Resolver):
        with self._registry_lock:
            # this can be more efficient since the list is already sorted,
            # but the size of this should be in the single digits, so should
            # not matter
            self._registry.append((priority, resolver))
            self._registry.sort(key=lambda kv: kv[0], reverse=True)

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
        with self._registry_lock:
            resolvers = self._registry[:]

        to_cache: Deque[Resolver] = collections.deque()
        for _, resolver in resolvers:
            result = await resolver.resolve(to_resolve)
            if result is not None:
                break

            to_cache.appendleft(resolver)

        if result is not None:
            await asyncio.gather(*[cache.store(result) for cache in to_cache])

        return result
