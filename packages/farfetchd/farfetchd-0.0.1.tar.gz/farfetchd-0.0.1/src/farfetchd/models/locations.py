"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Location(Model["Location"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The region this location can be found in.
    region: NamedAPIResource
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of game indices relevent to this location by generation.
    game_indices: List[GenerationGameIndex]
    # Areas that can be found within this location.
    areas: List[NamedAPIResource[LocationArea]]


@dataclass
class LocationArea(Model["LocationArea"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The internal id of an API resource within game data.
    game_index: int
    # A list of methods in which Pokemon may be encountered in this area and how likely
    # method will occur depending on the version of the game.
    encounter_method_rates: List[EncounterMethodRate]
    # The region this location area can be found in.
    location: NamedAPIResource[Location]
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of Pokemon that can be encountered in this area along with version specific
    # about the encounter.
    pokemon_encounters: List[PokemonEncounter]


@dataclass
class EncounterMethodRate(Model["EncounterMethodRate"]):
    # The method in which Pokemon may be encountered in an area..
    encounter_method: NamedAPIResource
    # The chance of the encounter to occur on a version of the game.
    version_details: List[EncounterVersionDetails]


@dataclass
class EncounterVersionDetails(Model["EncounterVersionDetails"]):
    # The chance of an encounter to occur.
    rate: int
    # The version of the game in which the encounter can occur with the given chance.
    version: NamedAPIResource


@dataclass
class PokemonEncounter(Model["PokemonEncounter"]):
    # The Pokemon being encountered.
    pokemon: NamedAPIResource
    # A list of versions and encounters with Pokemon that might happen in the referenced
    # area.
    version_details: List[VersionEncounterDetail]


@dataclass
class PalParkArea(Model["PalParkArea"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of Pokemon encountered in thi pal park area along with details.
    pokemon_encounters: List[PalParkEncounterSpecies]


@dataclass
class PalParkEncounterSpecies(Model["PalParkEncounterSpecies"]):
    # The base score given to the player when this Pokemon is caught during a pal park
    base_score: int
    # The base rate for encountering this Pokemon in this pal park area.
    rate: int
    # The Pokemon species being encountered.
    pokemon_species: NamedAPIResource


@dataclass
class Region(Model["Region"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # A list of locations that can be found in this region.
    locations: List[NamedAPIResource[Location]]
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # The generation this region was introduced in.
    main_generation: NamedAPIResource
    # A list of pokedexes that catalogue Pokemon in this region.
    pokedexes: List[NamedAPIResource[Pokedex]]
    # A list of version groups where this region can be visited.
    version_groups: List[NamedAPIResource[VersionGroup]]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .games import (
    Pokedex,
    VersionGroup,
)

from .generic import (
    NamedAPIResource,
)

from .utility import (
    GenerationGameIndex,
    Name,
    VersionEncounterDetail,
)
