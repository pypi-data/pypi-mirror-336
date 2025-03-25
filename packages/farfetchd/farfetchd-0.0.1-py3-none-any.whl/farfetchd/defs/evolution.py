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


from ..models.evolution import (
    EvolutionChain,
    EvolutionTrigger,
)


@defines(EvolutionChain)
def evolution_chains(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[EvolutionChain] | CacheableResourceList[EvolutionChain]:
    """
    Evolution chains are essentially family trees. They start with the lowest stage
    a family and detail evolution conditions for each as well as Pokemon they can evolve
    up through the hierarchy.
    """

    if id is not None:
        return CacheableResource(
            EvolutionChain,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/evolution-chain/{id}",
        )

    if pagination is not None:
        return CacheableResourceList(
            EvolutionChain, pagination, "https://pokeapi.co/api/v2/evolution-chain/"
        )

    if url is not None:
        return CacheableResource(EvolutionChain, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(EvolutionTrigger)
def evolution_triggers(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[EvolutionTrigger] | CacheableResourceList[EvolutionTrigger]:
    """
    Evolution triggers are the events and conditions that cause a Pokemon to evolve.
    out Bulbapedia for greater detail.
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
            EvolutionTrigger,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/evolution-trigger/{id}",
        )

    if name is not None:
        return CacheableResource(
            EvolutionTrigger,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/evolution-trigger/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            EvolutionTrigger, pagination, "https://pokeapi.co/api/v2/evolution-trigger/"
        )

    if url is not None:
        return CacheableResource(EvolutionTrigger, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
