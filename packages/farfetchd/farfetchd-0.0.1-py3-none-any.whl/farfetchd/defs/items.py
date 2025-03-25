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


from ..models.items import (
    Item,
    ItemAttribute,
    ItemCategory,
    ItemFlingEffect,
    ItemPocket,
)


@defines(Item)
def item(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[Item] | CacheableResourceList[Item]:
    """
    An item is an object in the games which the player can pick up, keep in their bag,
    use in some manner. They have various uses, including healing, powering up, helping
    Pokemon, or to access a new area.
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
            Item, ResourceIdentifier("id", id), f"https://pokeapi.co/api/v2/item/{id}"
        )

    if name is not None:
        return CacheableResource(
            Item,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/item/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            Item, pagination, "https://pokeapi.co/api/v2/item/"
        )

    if url is not None:
        return CacheableResource(Item, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(ItemAttribute)
def item_attributes(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[ItemAttribute] | CacheableResourceList[ItemAttribute]:
    """
    Item attributes define particular aspects of items, e.g. "usable in battle" or
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
            ItemAttribute,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/item-attribute/{id}",
        )

    if name is not None:
        return CacheableResource(
            ItemAttribute,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/item-attribute/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            ItemAttribute, pagination, "https://pokeapi.co/api/v2/item-attribute/"
        )

    if url is not None:
        return CacheableResource(ItemAttribute, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(ItemCategory)
def item_categories(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[ItemCategory] | CacheableResourceList[ItemCategory]:
    """
    Item categories determine where items will be placed in the players bag.
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
            ItemCategory,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/item-category/{id}",
        )

    if name is not None:
        return CacheableResource(
            ItemCategory,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/item-category/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            ItemCategory, pagination, "https://pokeapi.co/api/v2/item-category/"
        )

    if url is not None:
        return CacheableResource(ItemCategory, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(ItemFlingEffect)
def item_fling_effects(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[ItemFlingEffect] | CacheableResourceList[ItemFlingEffect]:
    """
    The various effects of the move "Fling" when used with different items.
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
            ItemFlingEffect,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/item-fling-effect/{id}",
        )

    if name is not None:
        return CacheableResource(
            ItemFlingEffect,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/item-fling-effect/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            ItemFlingEffect, pagination, "https://pokeapi.co/api/v2/item-fling-effect/"
        )

    if url is not None:
        return CacheableResource(ItemFlingEffect, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


@defines(ItemPocket)
def item_pockets(
    id: int | None = None,  # pylint: disable=invalid-name,redefined-builtin
    name: str | None = None,
    pagination: PaginationArguments | None = None,
    url: str | None = None,
) -> CacheableResource[ItemPocket] | CacheableResourceList[ItemPocket]:
    """
    Pockets within the players bag used for storing items by category.
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
            ItemPocket,
            ResourceIdentifier("id", id),
            f"https://pokeapi.co/api/v2/item-pocket/{id}",
        )

    if name is not None:
        return CacheableResource(
            ItemPocket,
            ResourceIdentifier("name", name),
            f"https://pokeapi.co/api/v2/item-pocket/{name}",
        )

    if pagination is not None:
        return CacheableResourceList(
            ItemPocket, pagination, "https://pokeapi.co/api/v2/item-pocket/"
        )

    if url is not None:
        return CacheableResource(ItemPocket, ResourceIdentifier("url", url), url)
    raise ValueError("this exception should be impossible")


def _exactly_one_non_none(*args) -> bool:
    has_non_none = False
    for arg in args:
        if arg is not None:
            if has_non_none:
                return False
            has_non_none = True
    return has_non_none
