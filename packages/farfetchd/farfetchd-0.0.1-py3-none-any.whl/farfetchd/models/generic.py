"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from typing import Generic, Type, TypeVar

T = TypeVar("T")


@dataclass
class NamedAPIResourceList(Generic[T]):
    # The total number of resources available from this API.
    count: int
    # The URL for the next page in the list.
    next: str
    # The URL for the previous page in the list.
    previous: str
    # A list of named API resources.
    results: List[NamedAPIResource[T]]

    # The type that this NamedAPIResourceList resolves to
    type: Type[T] | None = None


@dataclass
class APIResourceList(Generic[T]):
    # The total number of resources available from this API.
    count: int
    # The URL for the next page in the list.
    next: str
    # The URL for the previous page in the list.
    previous: str
    # A list of unnamed API resources.
    results: List[APIResource]

    # The type that this APIResourceList resolves to
    type: Type[T] | None = None


@dataclass
class APIResource(Generic[T]):
    # The URL of the referenced resource.
    url: str

    # The type that this APIResource resolves to
    type: Type[T] | None = None

    async def resolve(self) -> T:
        return await self.type.objects.get(url=self.url)


@dataclass
class NamedAPIResource(Generic[T]):
    # The name of the referenced resource.
    name: str
    # The URL of the referenced resource.
    url: str

    # The type that this NamedAPIResource resolves to
    type: Type[T] | None = None

    async def resolve(self) -> T:
        return await self.type.objects.get(name=self.name)


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)
