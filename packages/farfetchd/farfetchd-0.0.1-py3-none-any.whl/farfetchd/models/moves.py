"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Move(Model["Move"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The percent value of how likely this move is to be successful.
    accuracy: int
    # The percent value of how likely it is this moves effect will happen.
    effect_chance: int
    # Power points. The number of times this move can be used.
    pp: int  # pylint: disable=invalid-name
    # A value between -8 and 8. Sets the order in which moves are executed during
    # See Bulbapedia for greater detail.
    priority: int
    # The base power of this move with a value of 0 if it does not have a base power.
    power: int
    # A detail of normal and super contest combos that require this move.
    contest_combos: ContestComboSets
    # The type of appeal this move gives a Pokemon when used in a contest.
    contest_type: NamedAPIResource[ContestType]
    # The effect the move has when used in a contest.
    contest_effect: APIResource[ContestEffect]
    # The type of damage the move inflicts on the target, e.g. physical.
    damage_class: NamedAPIResource[MoveDamageClass]
    # The effect of this move listed in different languages.
    effect_entries: List[VerboseEffect]
    # The list of previous effects this move has had across version groups of the games.
    effect_changes: List[AbilityEffectChange]
    # List of Pokemon that can learn the move
    learned_by_pokemon: List[NamedAPIResource[Pokemon]]
    # The flavor text of this move listed in different languages.
    flavor_text_entries: List[MoveFlavorText]
    # The generation in which this move was introduced.
    generation: NamedAPIResource
    # A list of the machines that teach this move.
    machines: List[MachineVersionDetail]
    # Metadata about this move
    meta: MoveMetaData
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of move resource value changes across version groups of the game.
    past_values: List[PastMoveStatValues]
    # A list of stats this moves effects and how much it effects them.
    stat_changes: List[MoveStatChange]
    # The effect the move has when used in a super contest.
    super_contest_effect: APIResource
    # The type of target that will receive the effects of the attack.
    target: NamedAPIResource
    # The elemental type of this move.
    type: NamedAPIResource


@dataclass
class ContestComboSets(Model["ContestComboSets"]):
    # A detail of moves this move can be used before or after, granting additional
    # points in contests.
    normal: ContestComboDetail
    # A detail of moves this move can be used before or after, granting additional
    # points in super contests.
    super: ContestComboDetail


@dataclass
class ContestComboDetail(Model["ContestComboDetail"]):
    # A list of moves to use before this move.
    use_before: List[NamedAPIResource[Move]]
    # A list of moves to use after this move.
    use_after: List[NamedAPIResource[Move]]


@dataclass
class MoveFlavorText(Model["MoveFlavorText"]):
    # The localized flavor text for an api resource in a specific language.
    flavor_text: str
    # The language this name is in.
    language: NamedAPIResource[Language]
    # The version group that uses this flavor text.
    version_group: NamedAPIResource[VersionGroup]


@dataclass
class MoveMetaData(Model["MoveMetaData"]):
    # The status ailment this move inflicts on its target.
    ailment: NamedAPIResource
    # The category of move this move falls under, e.g. damage or ailment.
    category: NamedAPIResource
    # The minimum number of times this move hits. Null if it always only hits once.
    min_hits: int
    # The maximum number of times this move hits. Null if it always only hits once.
    max_hits: int
    # The minimum number of turns this move continues to take effect. Null if it always
    # lasts one turn.
    min_turns: int
    # The maximum number of turns this move continues to take effect. Null if it always
    # lasts one turn.
    max_turns: int
    # HP drain (if positive) or Recoil damage (if negative), in percent of damage done.
    drain: int
    # The amount of hp gained by the attacking Pokemon, in percent of it's maximum HP.
    healing: int
    # Critical hit rate bonus.
    crit_rate: int
    # The likelihood this attack will cause an ailment.
    ailment_chance: int
    # The likelihood this attack will cause the target Pokemon to flinch.
    flinch_chance: int
    # The likelihood this attack will cause a stat change in the target Pokemon.
    stat_chance: int


@dataclass
class MoveStatChange(Model["MoveStatChange"]):
    # The amount of change.
    change: int
    # The stat being affected.
    stat: NamedAPIResource


@dataclass
class PastMoveStatValues(Model["PastMoveStatValues"]):
    # The percent value of how likely this move is to be successful.
    accuracy: int
    # The percent value of how likely it is this moves effect will take effect.
    effect_chance: int
    # The base power of this move with a value of 0 if it does not have a base power.
    power: int
    # Power points. The number of times this move can be used.
    pp: int  # pylint: disable=invalid-name
    # The effect of this move listed in different languages.
    effect_entries: List[VerboseEffect]
    # The elemental type of this move.
    type: NamedAPIResource
    # The version group in which these move stat values were in effect.
    version_group: NamedAPIResource


@dataclass
class MoveAilment(Model["MoveAilment"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of moves that cause this ailment.
    moves: List[NamedAPIResource[Move]]
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class MoveBattleStyle(Model["MoveBattleStyle"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class MoveCategory(Model["MoveCategory"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of moves that fall into this category.
    moves: List[NamedAPIResource[Move]]
    # The description of this resource listed in different languages.
    descriptions: List[Description]


@dataclass
class MoveDamageClass(Model["MoveDamageClass"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The description of this resource listed in different languages.
    descriptions: List[Description]
    # A list of moves that fall into this damage class.
    moves: List[NamedAPIResource[Move]]
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class MoveLearnMethod(Model["MoveLearnMethod"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The description of this resource listed in different languages.
    descriptions: List[Description]
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of version groups where moves can be learned through this method.
    version_groups: List[NamedAPIResource[VersionGroup]]


@dataclass
class MoveTarget(Model["MoveTarget"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The description of this resource listed in different languages.
    descriptions: List[Description]
    # A list of moves that that are directed at this target.
    moves: List[NamedAPIResource[Move]]
    # The name of this resource listed in different languages.
    names: List[Name]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .contests import (
    ContestEffect,
    ContestType,
)

from .games import (
    VersionGroup,
)

from .generic import (
    APIResource,
    NamedAPIResource,
)

from .pokemon import (
    AbilityEffectChange,
    Pokemon,
)

from .utility import (
    Description,
    Language,
    MachineVersionDetail,
    Name,
    VerboseEffect,
)
