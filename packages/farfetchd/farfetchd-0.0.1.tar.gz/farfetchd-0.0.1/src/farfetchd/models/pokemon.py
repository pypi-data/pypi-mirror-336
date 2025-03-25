"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Ability(Model["Ability"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # Whether or not this ability originated in the main series of the video games.
    is_main_series: bool
    # The generation this ability originated in.
    generation: NamedAPIResource[Generation]
    # The name of this resource listed in different languages.
    names: List[Name]
    # The effect of this ability listed in different languages.
    effect_entries: List[VerboseEffect]
    # The list of previous effects this ability has had across version groups.
    effect_changes: List[AbilityEffectChange]
    # The flavor text of this ability listed in different languages.
    flavor_text_entries: List[AbilityFlavorText]
    # A list of Pokemon that could potentially have this ability.
    pokemon: List[AbilityPokemon]


@dataclass
class AbilityEffectChange(Model["AbilityEffectChange"]):
    # The previous effect of this ability listed in different languages.
    effect_entries: List[Effect]
    # The version group in which the previous effect of this ability originated.
    version_group: NamedAPIResource[VersionGroup]


@dataclass
class AbilityFlavorText(Model["AbilityFlavorText"]):
    # The localized name for an API resource in a specific language.
    flavor_text: str
    # The language this text resource is in.
    language: NamedAPIResource[Language]
    # The version group that uses this flavor text.
    version_group: NamedAPIResource[VersionGroup]


@dataclass
class AbilityPokemon(Model["AbilityPokemon"]):
    # Whether or not this a hidden ability for the referenced Pokemon.
    is_hidden: bool
    # Pokemon have 3 ability 'slots' which hold references to possible abilities they
    # have. This is the slot of this ability for the referenced pokemon.
    slot: int
    # The Pokemon this ability could belong to.
    pokemon: NamedAPIResource[Pokemon]


@dataclass
class Characteristic(Model["Characteristic"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The remainder of the highest stat/IV divided by 5.
    gene_modulo: int
    # The possible values of the highest stat that would result in a Pokemon recieving
    # characteristic when divided by 5.
    possible_values: List[int]
    # The stat which results in this characteristic.
    highest_stat: NamedAPIResource[Stat]
    # The descriptions of this characteristic listed in different languages.
    descriptions: List[Description]


@dataclass
class EggGroup(Model["EggGroup"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of all Pokemon species that are members of this egg group.
    pokemon_species: List[NamedAPIResource[PokemonSpecies]]


@dataclass
class Gender(Model["Gender"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of Pokemon species that can be this gender and how likely it is that they
    # be.
    pokemon_species_details: List[PokemonSpeciesGender]
    # A list of Pokemon species that required this gender in order for a Pokemon to
    # into them.
    required_for_evolution: List[NamedAPIResource[PokemonSpecies]]


@dataclass
class PokemonSpeciesGender(Model["PokemonSpeciesGender"]):
    # The chance of this Pokemon being female, in eighths; or -1 for genderless.
    rate: int
    # A Pokemon species that can be the referenced gender.
    pokemon_species: NamedAPIResource[PokemonSpecies]


@dataclass
class GrowthRate(Model["GrowthRate"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The formula used to calculate the rate at which the Pokemon species gains level.
    formula: str
    # The descriptions of this characteristic listed in different languages.
    descriptions: List[Description]
    # A list of levels and the amount of experienced needed to atain them based on this
    # rate.
    levels: List[GrowthRateExperienceLevel]
    # A list of Pokemon species that gain levels at this growth rate.
    pokemon_species: List[NamedAPIResource[PokemonSpecies]]


@dataclass
class GrowthRateExperienceLevel(Model["GrowthRateExperienceLevel"]):
    # The level gained.
    level: int
    # The amount of experience required to reach the referenced level.
    experience: int


@dataclass
class Nature(Model["Nature"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The stat decreased by 10% in Pokemon with this nature.
    decreased_stat: NamedAPIResource[Stat]
    # The stat increased by 10% in Pokemon with this nature.
    increased_stat: NamedAPIResource[Stat]
    # The flavor hated by Pokemon with this nature.
    hates_flavor: NamedAPIResource[BerryFlavor]
    # The flavor liked by Pokemon with this nature.
    likes_flavor: NamedAPIResource[BerryFlavor]
    # A list of Pokeathlon stats this nature effects and how much it effects them.
    pokeathlon_stat_changes: List[NatureStatChange]
    # A list of battle styles and how likely a Pokemon with this nature is to use them
    # the Battle Palace or Battle Tent.
    move_battle_style_preferences: List[MoveBattleStylePreference]
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class NatureStatChange(Model["NatureStatChange"]):
    # The amount of change.
    max_change: int
    # The stat being affected.
    pokeathlon_stat: NamedAPIResource[PokeathlonStat]


@dataclass
class MoveBattleStylePreference(Model["MoveBattleStylePreference"]):
    # Chance of using the move, in percent, if HP is under one half.
    low_hp_preference: int
    # Chance of using the move, in percent, if HP is over one half.
    high_hp_preference: int
    # The move battle style.
    move_battle_style: NamedAPIResource[MoveBattleStyle]


@dataclass
class PokeathlonStat(Model["PokeathlonStat"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # A detail of natures which affect this Pokeathlon stat positively or negatively.
    affecting_natures: NaturePokeathlonStatAffectSets


@dataclass
class NaturePokeathlonStatAffectSets(Model["NaturePokeathlonStatAffectSets"]):
    # A list of natures and how they change the referenced Pokeathlon stat.
    increase: List[NaturePokeathlonStatAffect]
    # A list of natures and how they change the referenced Pokeathlon stat.
    decrease: List[NaturePokeathlonStatAffect]


@dataclass
class NaturePokeathlonStatAffect(Model["NaturePokeathlonStatAffect"]):
    # The maximum amount of change to the referenced Pokeathlon stat.
    max_change: int
    # The nature causing the change.
    nature: NamedAPIResource[Nature]


@dataclass
class Pokemon(Model["Pokemon"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The base experience gained for defeating this Pokemon.
    base_experience: int
    # The height of this Pokemon in decimetres.
    height: int
    # Set for exactly one Pokemon used as the default for each species.
    is_default: bool
    # Order for sorting. Almost national order, except families are grouped together.
    order: int
    # The weight of this Pokemon in hectograms.
    weight: int
    # A list of abilities this Pokemon could potentially have.
    abilities: List[PokemonAbility]
    # A list of forms this Pokemon can take on.
    forms: List[NamedAPIResource[PokemonForm]]
    # A list of game indices relevent to Pokemon item by generation.
    game_indices: List[VersionGameIndex]
    # A list of items this Pokemon may be holding when encountered.
    held_items: List[PokemonHeldItem]
    # A link to a list of location areas, as well as encounter details pertaining to
    # versions.
    location_area_encounters: str
    # A list of moves along with learn methods and level details pertaining to specific
    # groups.
    moves: List[PokemonMove]
    # A list of details showing types this pokemon had in previous generations
    past_types: List[PokemonTypePast]
    # A set of sprites used to depict this Pokemon in the game. A visual representation
    # the various sprites can be found at PokeAPI/sprites
    sprites: PokemonSprites
    # A set of cries used to depict this Pokemon in the game. A visual representation of
    # various cries can be found at PokeAPI/cries
    cries: PokemonCries
    # The species this Pokemon belongs to.
    species: NamedAPIResource[PokemonSpecies]
    # A list of base stat values for this Pokemon.
    stats: List[PokemonStat]
    # A list of details showing types this Pokemon has.
    types: List[PokemonType]


@dataclass
class PokemonAbility(Model["PokemonAbility"]):
    # Whether or not this is a hidden ability.
    is_hidden: bool
    # The slot this ability occupies in this Pokemon species.
    slot: int
    # The ability the Pokemon may have.
    ability: NamedAPIResource[Ability]


@dataclass
class PokemonType(Model["PokemonType"]):
    # The order the Pokemon's types are listed in.
    slot: int
    # The type the referenced Pokemon has.
    type: NamedAPIResource[Type]


@dataclass
class PokemonFormType(Model["PokemonFormType"]):
    # The order the Pokemon's types are listed in.
    slot: int
    # The type the referenced Form has.
    type: NamedAPIResource[Type]


@dataclass
class PokemonTypePast(Model["PokemonTypePast"]):
    # The last generation in which the referenced pokemon had the listed types.
    generation: NamedAPIResource[Generation]
    # The types the referenced pokemon had up to and including the listed generation.
    types: List[PokemonType]


@dataclass
class PokemonHeldItem(Model["PokemonHeldItem"]):
    # The item the referenced Pokemon holds.
    item: NamedAPIResource[Item]
    # The details of the different versions in which the item is held.
    version_details: List[PokemonHeldItemVersion]


@dataclass
class PokemonHeldItemVersion(Model["PokemonHeldItemVersion"]):
    # The version in which the item is held.
    version: NamedAPIResource[Version]
    # How often the item is held.
    rarity: int


@dataclass
class PokemonMove(Model["PokemonMove"]):
    # The move the Pokemon can learn.
    move: NamedAPIResource[Move]
    # The details of the version in which the Pokemon can learn the move.
    version_group_details: List[PokemonMoveVersion]


@dataclass
class PokemonMoveVersion(Model["PokemonMoveVersion"]):
    # The method by which the move is learned.
    move_learn_method: NamedAPIResource[MoveLearnMethod]
    # The version group in which the move is learned.
    version_group: NamedAPIResource[VersionGroup]
    # The minimum level to learn the move.
    level_learned_at: int


@dataclass
class PokemonStat(Model["PokemonStat"]):
    # The stat the Pokemon has.
    stat: NamedAPIResource[Stat]
    # The effort points (EV) the Pokemon has in the stat.
    effort: int
    # The base value of the stat.
    base_stat: int


@dataclass
class PokemonSprites(Model["PokemonSprites"]):
    # The default depiction of this Pokemon from the front in battle.
    front_default: str
    # The shiny depiction of this Pokemon from the front in battle.
    front_shiny: str
    # The female depiction of this Pokemon from the front in battle.
    front_female: str
    # The shiny female depiction of this Pokemon from the front in battle.
    front_shiny_female: str
    # The default depiction of this Pokemon from the back in battle.
    back_default: str
    # The shiny depiction of this Pokemon from the back in battle.
    back_shiny: str
    # The female depiction of this Pokemon from the back in battle.
    back_female: str
    # The shiny female depiction of this Pokemon from the back in battle.
    back_shiny_female: str


@dataclass
class PokemonCries(Model["PokemonCries"]):
    # The latest depiction of this Pokemon's cry.
    latest: str
    # The legacy depiction of this Pokemon's cry.
    legacy: str


@dataclass
class LocationAreaEncounter(Model["LocationAreaEncounter"]):
    # The location area the referenced Pokemon can be encountered in.
    location_area: NamedAPIResource[LocationArea]
    # A list of versions and encounters with the referenced Pokemon that might happen.
    version_details: List[VersionEncounterDetail]


@dataclass
class PokemonColor(Model["PokemonColor"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of the Pokemon species that have this color.
    pokemon_species: List[NamedAPIResource[PokemonSpecies]]


@dataclass
class PokemonForm(Model["PokemonForm"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The order in which forms should be sorted within all forms. Multiple forms may
    # equal order, in which case they should fall back on sorting by name.
    order: int
    # The order in which forms should be sorted within a species' forms.
    form_order: int
    # True for exactly one form used as the default for each Pokemon.
    is_default: bool
    # Whether or not this form can only happen during battle.
    is_battle_only: bool
    # Whether or not this form requires mega evolution.
    is_mega: bool
    # The name of this form.
    form_name: str
    # The Pokemon that can take on this form.
    pokemon: NamedAPIResource[Pokemon]
    # A list of details showing types this Pokemon form has.
    types: List[PokemonFormType]
    # A set of sprites used to depict this Pokemon form in the game.
    sprites: PokemonFormSprites
    # The version group this Pokemon form was introduced in.
    version_group: NamedAPIResource[VersionGroup]
    # The form specific full name of this Pokemon form, or empty if the form does not
    # a specific name.
    names: List[Name]
    # The form specific form name of this Pokemon form, or empty if the form does not
    # a specific name.
    form_names: List[Name]


@dataclass
class PokemonFormSprites(Model["PokemonFormSprites"]):
    # The default depiction of this Pokemon form from the front in battle.
    front_default: str
    # The shiny depiction of this Pokemon form from the front in battle.
    front_shiny: str
    # The default depiction of this Pokemon form from the back in battle.
    back_default: str
    # The shiny depiction of this Pokemon form from the back in battle.
    back_shiny: str


@dataclass
class PokemonHabitat(Model["PokemonHabitat"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of the Pokemon species that can be found in this habitat.
    pokemon_species: List[NamedAPIResource[PokemonSpecies]]


@dataclass
class PokemonShape(Model["PokemonShape"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The "scientific" name of this Pokemon shape listed in different languages.
    awesome_names: List[AwesomeName]
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of the Pokemon species that have this shape.
    pokemon_species: List[NamedAPIResource[PokemonSpecies]]


@dataclass
class AwesomeName(Model["AwesomeName"]):
    # The localized "scientific" name for an API resource in a specific language.
    awesome_name: str
    # The language this "scientific" name is in.
    language: NamedAPIResource[Language]


@dataclass
class PokemonSpecies(Model["PokemonSpecies"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The order in which species should be sorted. Based on National Dex order, except
    # are grouped together and sorted by stage.
    order: int
    # The chance of this Pokemon being female, in eighths; or -1 for genderless.
    gender_rate: int
    # The base capture rate; up to 255. The higher the number, the easier the catch.
    capture_rate: int
    # The happiness when caught by a normal Pokeball; up to 255. The higher the number,
    # happier the Pokemon.
    base_happiness: int
    # Whether or not this is a baby Pokemon.
    is_baby: bool
    # Whether or not this is a legendary Pokemon.
    is_legendary: bool
    # Whether or not this is a mythical Pokemon.
    is_mythical: bool
    # Initial hatch counter: one must walk Y × (hatch_counter + 1) steps before this
    # egg hatches, unless utilizing bonuses like Flame Body's. Y varies per generation.
    # Generations II, III, and VII, Egg cycles are 256 steps long. In Generation IV, Egg
    # are 255 steps long. In Pokemon Brilliant Diamond and Shining Pearl, Egg cycles are
    # 255 steps long, but are shorter on special dates. In Generations V and VI, Egg
    # are 257 steps long. In Pokemon Sword and Shield, and in Pokemon Scarlet and
    # Egg cycles are 128 steps long.
    hatch_counter: int
    # Whether or not this Pokemon has visual gender differences.
    has_gender_differences: bool
    # Whether or not this Pokemon has multiple forms and can switch between them.
    forms_switchable: bool
    # The rate at which this Pokemon species gains levels.
    growth_rate: NamedAPIResource[GrowthRate]
    # A list of Pokedexes and the indexes reserved within them for this Pokemon species.
    pokedex_numbers: List[PokemonSpeciesDexEntry]
    # A list of egg groups this Pokemon species is a member of.
    egg_groups: List[NamedAPIResource[EggGroup]]
    # The color of this Pokemon for Pokedex search.
    color: NamedAPIResource[PokemonColor]
    # The shape of this Pokemon for Pokedex search.
    shape: NamedAPIResource[PokemonShape]
    # The Pokemon species that evolves into this Pokemon_species.
    evolves_from_species: NamedAPIResource[PokemonSpecies]
    # The evolution chain this Pokemon species is a member of.
    evolution_chain: APIResource[EvolutionChain]
    # The habitat this Pokemon species can be encountered in.
    habitat: NamedAPIResource[PokemonHabitat]
    # The generation this Pokemon species was introduced in.
    generation: NamedAPIResource[Generation]
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of encounters that can be had with this Pokemon species in pal park.
    pal_park_encounters: List[PalParkEncounterArea]
    # A list of flavor text entries for this Pokemon species.
    flavor_text_entries: List[FlavorText]
    # Descriptions of different forms Pokemon take on within the Pokemon species.
    form_descriptions: List[Description]
    # The genus of this Pokemon species listed in multiple languages.
    genera: List[Genus]
    # A list of the Pokemon that exist within this Pokemon species.
    varieties: List[PokemonSpeciesVariety]


@dataclass
class Genus(Model["Genus"]):
    # The localized genus for the referenced Pokemon species
    genus: str
    # The language this genus is in.
    language: NamedAPIResource[Language]


@dataclass
class PokemonSpeciesDexEntry(Model["PokemonSpeciesDexEntry"]):
    # The index number within the Pokedex.
    entry_number: int
    # The Pokedex the referenced Pokemon species can be found in.
    pokedex: NamedAPIResource[Pokedex]


@dataclass
class PalParkEncounterArea(Model["PalParkEncounterArea"]):
    # The base score given to the player when the referenced Pokemon is caught during a
    # park run.
    base_score: int
    # The base rate for encountering the referenced Pokemon in this pal park area.
    rate: int
    # The pal park area where this encounter happens.
    area: NamedAPIResource[PalParkArea]


@dataclass
class PokemonSpeciesVariety(Model["PokemonSpeciesVariety"]):
    # Whether this variety is the default variety.
    is_default: bool
    # The Pokemon variety.
    pokemon: NamedAPIResource[Pokemon]


@dataclass
class Stat(Model["Stat"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # ID the games use for this stat.
    game_index: int
    # Whether this stat only exists within a battle.
    is_battle_only: bool
    # A detail of moves which affect this stat positively or negatively.
    affecting_moves: MoveStatAffectSets
    # A detail of natures which affect this stat positively or negatively.
    affecting_natures: NatureStatAffectSets
    # A list of characteristics that are set on a Pokemon when its highest base stat is
    # stat.
    characteristics: List[APIResource[Characteristic]]
    # The class of damage this stat is directly related to.
    move_damage_class: NamedAPIResource[MoveDamageClass]
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class MoveStatAffectSets(Model["MoveStatAffectSets"]):
    # A list of moves and how they change the referenced stat.
    increase: List[MoveStatAffect]
    # A list of moves and how they change the referenced stat.
    decrease: List[MoveStatAffect]


@dataclass
class MoveStatAffect(Model["MoveStatAffect"]):
    # The maximum amount of change to the referenced stat.
    change: int
    # The move causing the change.
    move: NamedAPIResource[Move]


@dataclass
class NatureStatAffectSets(Model["NatureStatAffectSets"]):
    # A list of natures and how they change the referenced stat.
    increase: List[NamedAPIResource[Nature]]
    # A list of nature sand how they change the referenced stat.
    decrease: List[NamedAPIResource[Nature]]


@dataclass
class Type(Model["Type"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A detail of how effective this type is toward others and vice versa.
    damage_relations: TypeRelations
    # A list of details of how effective this type was toward others and vice versa in
    # generations
    past_damage_relations: List[TypeRelationsPast[Type]]
    # A list of game indices relevent to this item by generation.
    game_indices: List[GenerationGameIndex]
    # The generation this type was introduced in.
    generation: NamedAPIResource[Generation]
    # The class of damage inflicted by this type.
    move_damage_class: NamedAPIResource[MoveDamageClass]
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of details of Pokemon that have this type.
    pokemon: List[TypePokemon]
    # A list of moves that have this type.
    moves: List[NamedAPIResource[Move]]


@dataclass
class TypePokemon(Model["TypePokemon"]):
    # The order the Pokemon's types are listed in.
    slot: int
    # The Pokemon that has the referenced type.
    pokemon: NamedAPIResource[Pokemon]


@dataclass
class TypeRelations(Model["TypeRelations"]):
    # A list of types this type has no effect on.
    no_damage_to: List[NamedAPIResource[Type]]
    # A list of types this type is not very effect against.
    half_damage_to: List[NamedAPIResource[Type]]
    # A list of types this type is very effect against.
    double_damage_to: List[NamedAPIResource[Type]]
    # A list of types that have no effect on this type.
    no_damage_from: List[NamedAPIResource[Type]]
    # A list of types that are not very effective against this type.
    half_damage_from: List[NamedAPIResource[Type]]
    # A list of types that are very effective against this type.
    double_damage_from: List[NamedAPIResource[Type]]


@dataclass
class TypeRelationsPast(Model["TypeRelationsPast"]):
    # The last generation in which the referenced type had the listed damage relations
    generation: NamedAPIResource[Generation]
    # The damage relations the referenced type had up to and including the listed
    damage_relations: TypeRelations


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .berries import (
    BerryFlavor,
)

from .evolution import (
    EvolutionChain,
)

from .games import (
    Generation,
    Pokedex,
    Version,
    VersionGroup,
)

from .generic import (
    APIResource,
    NamedAPIResource,
)

from .items import (
    Item,
)

from .locations import (
    LocationArea,
    PalParkArea,
)

from .moves import (
    Move,
    MoveBattleStyle,
    MoveDamageClass,
    MoveLearnMethod,
)

from .utility import (
    Description,
    Effect,
    FlavorText,
    GenerationGameIndex,
    Language,
    Name,
    VerboseEffect,
    VersionEncounterDetail,
    VersionGameIndex,
)
