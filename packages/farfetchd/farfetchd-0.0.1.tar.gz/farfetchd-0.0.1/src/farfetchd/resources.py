from dataclasses import dataclass
from typing import Generic, TypeVar, Type

T = TypeVar("T")


@dataclass
class PaginationArguments:
    limit: int | None = None
    offset: int | None = None


@dataclass
class ResourceIdentifier(Generic[T]):
    id_name: str
    value: T


@dataclass
class CacheableResource(Generic[T]):
    resource_type: Type[T]
    resource_id: ResourceIdentifier[str] | ResourceIdentifier[int]
    resource_url: str


@dataclass
class CacheableResourceList(Generic[T]):
    resource_type: Type[T]
    pagination: PaginationArguments
    resource_url: str
