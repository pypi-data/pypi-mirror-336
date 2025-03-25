"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Generation(Model["Generation"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of abilities that were introduced in this generation.
    abilities: List[NamedAPIResource[Ability]]
    # The name of this resource listed in different languages.
    names: List[Name]
    # The main region travelled in this generation.
    main_region: NamedAPIResource[Region]
    # A list of moves that were introduced in this generation.
    moves: List[NamedAPIResource[Move]]
    # A list of Pokemon species that were introduced in this generation.
    pokemon_species: List[NamedAPIResource[PokemonSpecies]]
    # A list of types that were introduced in this generation.
    types: List[NamedAPIResource[Type]]
    # A list of version groups that were introduced in this generation.
    version_groups: List[NamedAPIResource[VersionGroup]]


@dataclass
class Pokedex(Model["Pokedex"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # Whether or not this Pokedex originated in the main series of the video games.
    is_main_series: bool
    # The description of this resource listed in different languages.
    descriptions: List[Description]
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of Pokemon catalogued in this Pokedex and their indexes.
    pokemon_entries: List[PokemonEntry]
    # The region this Pokedex catalogues Pokemon for.
    region: NamedAPIResource[Region]
    # A list of version groups this Pokedex is relevant to.
    version_groups: List[NamedAPIResource[VersionGroup]]


@dataclass
class PokemonEntry(Model["PokemonEntry"]):
    # The index of this Pokemon species entry within the Pokedex.
    entry_number: int
    # The Pokemon species being encountered.
    pokemon_species: NamedAPIResource[PokemonSpecies]


@dataclass
class Version(Model["Version"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # The version group this version belongs to.
    version_group: NamedAPIResource[VersionGroup]


@dataclass
class VersionGroup(Model["VersionGroup"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # Order for sorting. Almost by date of release, except similar versions are grouped
    order: int
    # The generation this version was introduced in.
    generation: NamedAPIResource[Generation]
    # A list of methods in which Pokemon can learn moves in this version group.
    move_learn_methods: List[NamedAPIResource[MoveLearnMethod]]
    # A list of Pokedexes introduces in this version group.
    pokedexes: List[NamedAPIResource[Pokedex]]
    # A list of regions that can be visited in this version group.
    regions: List[NamedAPIResource[Region]]
    # The versions this version group owns.
    versions: List[NamedAPIResource[Version]]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .generic import (
    NamedAPIResource,
)

from .locations import (
    Region,
)

from .moves import (
    Move,
    MoveLearnMethod,
)

from .pokemon import (
    Ability,
    PokemonSpecies,
    Type,
)

from .utility import (
    Description,
    Name,
)
