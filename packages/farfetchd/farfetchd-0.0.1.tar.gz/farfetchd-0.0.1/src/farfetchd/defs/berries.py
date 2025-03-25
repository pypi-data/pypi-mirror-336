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


from ..models.berries import (
    Berry,
    BerryFirmness,
    BerryFlavor,
)


@defines(Berry)
def berries(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Berry] | CacheableResourceList[Berry]:
    """
    Berries are small fruits that can provide HP and status condition restoration, stat
    and even damage negation when eaten by Pokemon. Check out Bulbapedia for greater
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
            Berry, ResourceIdentifier("id", id), f"https://pokeapi.co/api/v2/berry/{id}"
        )

    if name is not None:
        return CacheableResource(
            Berry,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/berry/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Berry, pagination, "https://pokeapi.co/api/v2/berry/"
        )

    if url is not None:
        return CacheableResource(Berry, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(BerryFirmness)
def berry_firmnesses(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[BerryFirmness] | CacheableResourceList[BerryFirmness]:
    """
    Berries can be soft or hard. Check out Bulbapedia for greater detail.
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
            BerryFirmness,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/berry-firmness/{id}",
        )

    if name is not None:
        return CacheableResource(
            BerryFirmness,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/berry-firmness/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            BerryFirmness, pagination, "https://pokeapi.co/api/v2/berry-firmness/"
        )

    if url is not None:
        return CacheableResource(BerryFirmness, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(BerryFlavor)
def berry_flavors(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[BerryFlavor] | CacheableResourceList[BerryFlavor]:
    """
    Flavors determine whether a Pokemon will benefit or suffer from eating a berry based
    their nature. Check out Bulbapedia for greater detail.
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
            BerryFlavor,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/berry-flavor/{id}",
        )

    if name is not None:
        return CacheableResource(
            BerryFlavor,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/berry-flavor/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            BerryFlavor, pagination, "https://pokeapi.co/api/v2/berry-flavor/"
        )

    if url is not None:
        return CacheableResource(BerryFlavor, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
