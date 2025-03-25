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


from ..models.encounters import (
    EncounterCondition,
    EncounterConditionValue,
    EncounterMethod,
)


@defines(EncounterMethod)
def encounter_methods(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[EncounterMethod] | CacheableResourceList[EncounterMethod]:
    """
    Methods by which the player might can encounter Pokemon in the wild, e.g., walking
    tall grass. Check out Bulbapedia for greater detail.
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
            EncounterMethod,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/encounter-method/{id}",
        )

    if name is not None:
        return CacheableResource(
            EncounterMethod,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/encounter-method/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            EncounterMethod, pagination, "https://pokeapi.co/api/v2/encounter-method/"
        )

    if url is not None:
        return CacheableResource(EncounterMethod, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(EncounterCondition)
def encounter_conditions(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[EncounterCondition] | CacheableResourceList[EncounterCondition]:
    """
    Conditions which affect what pokemon might appear in the wild, e.g., day or night.
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
            EncounterCondition,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/encounter-condition/{id}",
        )

    if name is not None:
        return CacheableResource(
            EncounterCondition,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/encounter-condition/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            EncounterCondition,
            pagination,
            "https://pokeapi.co/api/v2/encounter-condition/",
        )

    if url is not None:
        return CacheableResource(
            EncounterCondition, ResourceIdentifier("url", url), url
        )
    raise ValueError("this exception should be impossible")


@defines(EncounterConditionValue)
def encounter_condition_values(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> (
    CacheableResource[EncounterConditionValue]
    | CacheableResourceList[EncounterConditionValue]
):
    """
    Encounter condition values are the various states that an encounter condition can
    i.e., time of day can be either day or night.
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
            EncounterConditionValue,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/encounter-condition-value/{id}",
        )

    if name is not None:
        return CacheableResource(
            EncounterConditionValue,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/encounter-condition-value/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            EncounterConditionValue,
            pagination,
            "https://pokeapi.co/api/v2/encounter-condition-value/",
        )

    if url is not None:
        return CacheableResource(
            EncounterConditionValue, ResourceIdentifier("url", url), url
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
