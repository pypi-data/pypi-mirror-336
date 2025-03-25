import dataclasses
import logging
import threading

from datetime import datetime, timedelta
from typing import Dict, Generic, List, Type, TypeVar, overload


from .resolver import Resolver
from ..base import Model
from ..models.generic import NamedAPIResourceList
from ..resources import CacheableResource, CacheableResourceList

T = TypeVar("T")

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class CacheEntry(Generic[T]):
    obj: T
    expires_at: datetime


class MemoryCacheResolver(Resolver):
    """
    Very simple in-memory cache implementation.

    Does NOT respond to system low memory notifications. Should be added.
    Also does NOT clean up expired entries until they are accessed.
    Needs to be addressed.
    """

    def __init__(self, ttl: timedelta) -> None:
        super().__init__()
        self._ttl = ttl

        # write lock - used only when inserting new items.
        # Could be narrowed down to smaller scopes
        self._insertion_lock = threading.Lock()
        # type -> key-name -> key -> entry
        self._cache: Dict[Type, Dict[str, Dict[str, CacheEntry[Model]]]] = {}

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
        obj_type = to_resolve.resource_type
        obj_cache = self._cache.get(obj_type)
        if obj_cache is None:
            return None

        if isinstance(to_resolve, CacheableResourceList):
            # CacheableResourceList not supported currently
            return None

        resource_id = to_resolve.resource_id
        id_type = resource_id.id_name
        id_value = resource_id.value

        resource_type_cache = obj_cache.get(id_type)
        if resource_type_cache is None:
            return None

        obj_entry = resource_type_cache.get(id_value)
        if obj_entry is None:
            return None

        now = datetime.now()
        if now > obj_entry.expires_at:
            logger.info(
                "expire cache entry (%s / %s / %s)", obj_type, id_type, id_value
            )
            try:
                del resource_type_cache[id_value]
            except KeyError:
                # key already deleted, possibly by another thread. This is fine
                logger.warning(
                    "failed to clear cache entry (%s / %s / %s) - most likely already deleted",
                    obj_type,
                    id_type,
                    id_value,
                )
            return None
        return obj_entry.obj

    async def store(
        self,
        to_store: T | List[T],
    ):
        if isinstance(to_store, list):
            # do not support lists yet...
            return

        obj_type = type(to_store)

        # possible keys currently are id and name
        obj_id = name = None
        if hasattr(to_store, "id"):
            obj_id = to_store.id
        if hasattr(to_store, "name"):
            name = to_store.name

        expire_at = datetime.now() + self._ttl
        cache_entry = CacheEntry(to_store, expire_at)

        if not obj_id and not name:
            # nothing to cache
            return

        with self._insertion_lock:
            if obj_type not in self._cache:
                self._cache[obj_type] = {}
            obj_cache = self._cache[obj_type]
            if obj_id:
                if "id" not in obj_cache:
                    obj_cache["id"] = {}
                id_cache = obj_cache["id"]
                id_cache[obj_id] = cache_entry
            if name:
                if "name" not in obj_cache:
                    obj_cache["name"] = {}
                name_cache = obj_cache["name"]
                name_cache[name] = cache_entry
