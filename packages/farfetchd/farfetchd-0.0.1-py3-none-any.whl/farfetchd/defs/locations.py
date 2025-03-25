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


from ..models.locations import (
    Location,
    LocationArea,
    PalParkArea,
    Region,
)


@defines(Location)
def locations(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Location] | CacheableResourceList[Location]:
    """
    Locations that can be visited within the games. Locations make up sizable portions
    regions, like cities or routes.
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
            Location,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/location/{id}",
        )

    if name is not None:
        return CacheableResource(
            Location,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/location/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Location, pagination, "https://pokeapi.co/api/v2/location/"
        )

    if url is not None:
        return CacheableResource(Location, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(LocationArea)
def location_areas(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[LocationArea] | CacheableResourceList[LocationArea]:
    """
    Location areas are sections of areas, such as floors in a building or cave. Each
    has its own set of possible Pokemon encounters.
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
            LocationArea,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/location-area/{id}",
        )

    if name is not None:
        return CacheableResource(
            LocationArea,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/location-area/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            LocationArea, pagination, "https://pokeapi.co/api/v2/location-area/"
        )

    if url is not None:
        return CacheableResource(LocationArea, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(PalParkArea)
def pal_park_areas(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[PalParkArea] | CacheableResourceList[PalParkArea]:
    """
    Areas used for grouping Pokemon encounters in Pal Park. They're like habitats that
    specific to Pal Park.
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
            PalParkArea,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/pal-park-area/{id}",
        )

    if name is not None:
        return CacheableResource(
            PalParkArea,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/pal-park-area/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            PalParkArea, pagination, "https://pokeapi.co/api/v2/pal-park-area/"
        )

    if url is not None:
        return CacheableResource(PalParkArea, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(Region)
def regions(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Region] | CacheableResourceList[Region]:
    """
    A region is an organized area of the Pokemon world. Most often, the main difference
    regions is the species of Pokemon that can be encountered within them.
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
            Region,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/region/{id}",
        )

    if name is not None:
        return CacheableResource(
            Region,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/region/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Region, pagination, "https://pokeapi.co/api/v2/region/"
        )

    if url is not None:
        return CacheableResource(Region, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
