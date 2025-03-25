"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from ..decorators import defines
from ..resources import (
    CacheableResource,
    CacheableResourceList,
    PaginationArguments,
    ResourceIdentifier,
)


from ..models.contests import (
    ContestEffect,
    ContestType,
    SuperContestEffect,
)


@defines(ContestType)
def contest_types(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[ContestType] | CacheableResourceList[ContestType]:
    """
    Contest types are categories judges used to weigh a Pokemon's condition in Pokemon
    Check out Bulbapedia for greater detail.
    """
    if not _exactly_one_non_none(
        id,
        name,
        pagination,
        url,
    ):
        raise ValueError(
            "Invalid arguments; "
            + "exactly one of [id, name, pagination, url] must not be None"
        )

    if id is not None:
        return CacheableResource(
            ContestType,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/contest-type/{id}",
        )

    if name is not None:
        return CacheableResource(
            ContestType,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/contest-type/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            ContestType, pagination, "https://pokeapi.co/api/v2/contest-type/"
        )

    if url is not None:
        return CacheableResource(ContestType, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(ContestEffect)
def contest_effects(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[ContestEffect] | CacheableResourceList[ContestEffect]:
    """
    Contest effects refer to the effects of moves when used in contests.
    """

    if id is not None:
        return CacheableResource(
            ContestEffect,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/contest-effect/{id}",
        )

    if pagination is not None:
        return CacheableResourceList(
            ContestEffect, pagination, "https://pokeapi.co/api/v2/contest-effect/"
        )

    if url is not None:
        return CacheableResource(ContestEffect, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(SuperContestEffect)
def super_contest_effects(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[SuperContestEffect] | CacheableResourceList[SuperContestEffect]:
    """
    Super contest effects refer to the effects of moves when used in super contests.
    """

    if id is not None:
        return CacheableResource(
            SuperContestEffect,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/super-contest-effect/{id}",
        )

    if pagination is not None:
        return CacheableResourceList(
            SuperContestEffect,
            pagination,
            "https://pokeapi.co/api/v2/super-contest-effect/",
        )

    if url is not None:
        return CacheableResource(
            SuperContestEffect, ResourceIdentifier("url", url), url
        )
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
