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


from ..models.utility import (
    Language,
)


@defines(Language)
def languages(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Language] | CacheableResourceList[Language]:
    """
    Languages for translations of API resource information.
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
            Language,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/language/{id}",
        )

    if name is not None:
        return CacheableResource(
            Language,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/language/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Language, pagination, "https://pokeapi.co/api/v2/language/"
        )

    if url is not None:
        return CacheableResource(Language, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
