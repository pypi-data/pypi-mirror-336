"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Item(Model["Item"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The price of this item in stores.
    cost: int
    # The power of the move Fling when used with this item.
    fling_power: int
    # The effect of the move Fling when used with this item.
    fling_effect: NamedAPIResource[ItemFlingEffect]
    # A list of attributes this item has.
    attributes: List[NamedAPIResource[ItemAttribute]]
    # The category of items this item falls into.
    category: NamedAPIResource[ItemCategory]
    # The effect of this ability listed in different languages.
    effect_entries: List[VerboseEffect]
    # The flavor text of this ability listed in different languages.
    flavor_text_entries: List[VersionGroupFlavorText]
    # A list of game indices relevent to this item by generation.
    game_indices: List[GenerationGameIndex]
    # The name of this item listed in different languages.
    names: List[Name]
    # A set of sprites used to depict this item in the game.
    sprites: ItemSprites
    # A list of Pokemon that might be found in the wild holding this item.
    held_by_pokemon: List[ItemHolderPokemon]
    # An evolution chain this item requires to produce a bay during mating.
    baby_trigger_for: APIResource[EvolutionChain]
    # A list of the machines related to this item.
    machines: List[MachineVersionDetail]


@dataclass
class ItemSprites(Model["ItemSprites"]):
    # The default depiction of this item.
    default: str


@dataclass
class ItemHolderPokemon(Model["ItemHolderPokemon"]):
    # The Pokemon that holds this item.
    pokemon: NamedAPIResource[Pokemon]
    # The details for the version that this item is held in by the Pokemon.
    version_details: List[ItemHolderPokemonVersionDetail]


@dataclass
class ItemHolderPokemonVersionDetail(Model["ItemHolderPokemonVersionDetail"]):
    # How often this Pokemon holds this item in this version.
    rarity: int
    # The version that this item is held in by the Pokemon.
    version: NamedAPIResource[Version]


@dataclass
class ItemAttribute(Model["ItemAttribute"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of items that have this attribute.
    items: List[NamedAPIResource[Item]]
    # The name of this item attribute listed in different languages.
    names: List[Name]
    # The description of this item attribute listed in different languages.
    descriptions: List[Description]


@dataclass
class ItemCategory(Model["ItemCategory"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of items that are a part of this category.
    items: List[NamedAPIResource[Item]]
    # The name of this item category listed in different languages.
    names: List[Name]
    # The pocket items in this category would be put in.
    pocket: NamedAPIResource[ItemPocket]


@dataclass
class ItemFlingEffect(Model["ItemFlingEffect"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The result of this fling effect listed in different languages.
    effect_entries: List[Effect]
    # A list of items that have this fling effect.
    items: List[NamedAPIResource[Item]]


@dataclass
class ItemPocket(Model["ItemPocket"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of item categories that are relevant to this item pocket.
    categories: List[NamedAPIResource[ItemCategory]]
    # The name of this resource listed in different languages.
    names: List[Name]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .evolution import (
    EvolutionChain,
)

from .games import (
    Version,
)

from .generic import (
    APIResource,
    NamedAPIResource,
)

from .pokemon import (
    Pokemon,
)

from .utility import (
    Description,
    Effect,
    GenerationGameIndex,
    MachineVersionDetail,
    Name,
    VerboseEffect,
    VersionGroupFlavorText,
)
