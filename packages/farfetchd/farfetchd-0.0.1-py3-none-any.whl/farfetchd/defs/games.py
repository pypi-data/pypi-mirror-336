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


from ..models.games import (
    Generation,
    Pokedex,
    Version,
    VersionGroup,
)


@defines(Generation)
def generations(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Generation] | CacheableResourceList[Generation]:
    """
    A generation is a grouping of the Pokemon games that separates them based on the
    they include. In each generation, a new set of Pokemon, Moves, Abilities and Types
    did not exist in the previous generation are released.
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
            Generation,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/generation/{id}",
        )

    if name is not None:
        return CacheableResource(
            Generation,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/generation/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Generation, pagination, "https://pokeapi.co/api/v2/generation/"
        )

    if url is not None:
        return CacheableResource(Generation, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(Pokedex)
def pokedexes(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Pokedex] | CacheableResourceList[Pokedex]:
    """
    A Pokedex is a handheld electronic encyclopedia device; one which is capable of
    and retaining information of the various Pokemon in a given region with the
    of the national dex and some smaller dexes related to portions of a region. See
    for greater detail.
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
            Pokedex,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/pokedex/{id}",
        )

    if name is not None:
        return CacheableResource(
            Pokedex,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/pokedex/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Pokedex, pagination, "https://pokeapi.co/api/v2/pokedex/"
        )

    if url is not None:
        return CacheableResource(Pokedex, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(Version)
def version(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Version] | CacheableResourceList[Version]:
    """
    Versions of the games, e.g., Red, Blue or Yellow.
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
            Version,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/version/{id}",
        )

    if name is not None:
        return CacheableResource(
            Version,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/version/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Version, pagination, "https://pokeapi.co/api/v2/version/"
        )

    if url is not None:
        return CacheableResource(Version, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(VersionGroup)
def version_groups(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[VersionGroup] | CacheableResourceList[VersionGroup]:
    """
    Version groups categorize highly similar versions of the games.
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
            VersionGroup,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/version-group/{id}",
        )

    if name is not None:
        return CacheableResource(
            VersionGroup,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/version-group/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            VersionGroup, pagination, "https://pokeapi.co/api/v2/version-group/"
        )

    if url is not None:
        return CacheableResource(VersionGroup, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
