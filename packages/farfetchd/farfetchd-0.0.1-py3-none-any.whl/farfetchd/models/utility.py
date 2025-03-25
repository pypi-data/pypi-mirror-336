"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Language(Model["Language"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # Whether or not the games are published in this language.
    official: bool
    # The two-letter code of the country where this language is spoken. Note that it is
    # unique.
    iso639: str
    # The two-letter code of the language. Note that it is not unique.
    iso3166: str
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class Description(Model["Description"]):
    # The localized description for an API resource in a specific language.
    description: str
    # The language this name is in.
    language: NamedAPIResource[Language]


@dataclass
class Effect(Model["Effect"]):
    # The localized effect text for an API resource in a specific language.
    effect: str
    # The language this effect is in.
    language: NamedAPIResource[Language]


@dataclass
class Encounter(Model["Encounter"]):
    # The lowest level the Pokemon could be encountered at.
    min_level: int
    # The highest level the Pokemon could be encountered at.
    max_level: int
    # A list of condition values that must be in effect for this encounter to occur.
    condition_values: List[NamedAPIResource[EncounterConditionValue]]
    # Percent chance that this encounter will occur.
    chance: int
    # The method by which this encounter happens.
    method: NamedAPIResource[EncounterMethod]


@dataclass
class FlavorText(Model["FlavorText"]):
    # The localized flavor text for an API resource in a specific language. Note that
    # text is left unprocessed as it is found in game files. This means that it contains
    # characters that one might want to replace with their visible decodable version.
    # check out this issue to find out more.
    flavor_text: str
    # The language this name is in.
    language: NamedAPIResource[Language]
    # The game version this flavor text is extracted from.
    version: NamedAPIResource[Version]


@dataclass
class GenerationGameIndex(Model["GenerationGameIndex"]):
    # The internal id of an API resource within game data.
    game_index: int
    # The generation relevent to this game index.
    generation: NamedAPIResource[Generation]


@dataclass
class MachineVersionDetail(Model["MachineVersionDetail"]):
    # The machine that teaches a move from an item.
    machine: APIResource
    # The version group of this specific machine.
    version_group: NamedAPIResource[VersionGroup]


@dataclass
class Name(Model["Name"]):
    # The localized name for an API resource in a specific language.
    name: str
    # The language this name is in.
    language: NamedAPIResource[Language]


@dataclass
class VerboseEffect(Model["VerboseEffect"]):
    # The localized effect text for an API resource in a specific language.
    effect: str
    # The localized effect text in brief.
    short_effect: str
    # The language this effect is in.
    language: NamedAPIResource[Language]


@dataclass
class VersionEncounterDetail(Model["VersionEncounterDetail"]):
    # The game version this encounter happens in.
    version: NamedAPIResource[Version]
    # The total percentage of all encounter potential.
    max_chance: int
    # A list of encounters and their specifics.
    encounter_details: List[Encounter]


@dataclass
class VersionGameIndex(Model["VersionGameIndex"]):
    # The internal id of an API resource within game data.
    game_index: int
    # The version relevent to this game index.
    version: NamedAPIResource[Version]


@dataclass
class VersionGroupFlavorText(Model["VersionGroupFlavorText"]):
    # The localized name for an API resource in a specific language.
    text: str
    # The language this name is in.
    language: NamedAPIResource[Language]
    # The version group which uses this flavor text.
    version_group: NamedAPIResource[VersionGroup]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .encounters import (
    EncounterConditionValue,
    EncounterMethod,
)

from .games import (
    Generation,
    Version,
    VersionGroup,
)

from .generic import (
    APIResource,
    NamedAPIResource,
)
