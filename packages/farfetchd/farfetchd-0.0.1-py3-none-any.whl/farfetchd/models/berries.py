"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Berry(Model["Berry"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # Time it takes the tree to grow one stage, in hours. Berry trees go through four of
    # growth stages before they can be picked.
    growth_time: int
    # The maximum number of these berries that can grow on one tree in Generation IV.
    max_harvest: int
    # The power of the move "Natural Gift" when used with this Berry.
    natural_gift_power: int
    # The size of this Berry, in millimeters.
    size: int
    # The smoothness of this Berry, used in making Pokeblocks or Poffins.
    smoothness: int
    # The speed at which this Berry dries out the soil as it grows. A higher rate means
    # soil dries more quickly.
    soil_dryness: int
    # The firmness of this berry, used in making Pokeblocks or Poffins.
    firmness: NamedAPIResource[BerryFirmness]
    # A list of references to each flavor a berry can have and the potency of each of
    # flavors in regard to this berry.
    flavors: List[BerryFlavorMap]
    # Berries are actually items. This is a reference to the item specific data for this
    item: NamedAPIResource[Item]
    # The type inherited by "Natural Gift" when used with this Berry.
    natural_gift_type: NamedAPIResource[Type]


@dataclass
class BerryFlavorMap(Model["BerryFlavorMap"]):
    # How powerful the referenced flavor is for this berry.
    potency: int
    # The referenced berry flavor.
    flavor: NamedAPIResource[BerryFlavor]


@dataclass
class BerryFirmness(Model["BerryFirmness"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of the berries with this firmness.
    berries: List[NamedAPIResource[Berry]]
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class BerryFlavor(Model["BerryFlavor"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A list of the berries with this flavor.
    berries: List[FlavorBerryMap]
    # The contest type that correlates with this berry flavor.
    contest_type: NamedAPIResource[ContestType]
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class FlavorBerryMap(Model["FlavorBerryMap"]):
    # How powerful the referenced flavor is for this berry.
    potency: int
    # The berry with the referenced flavor.
    berry: NamedAPIResource[Berry]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .contests import (
    ContestType,
)

from .generic import (
    NamedAPIResource,
)

from .items import (
    Item,
)

from .pokemon import (
    Type,
)

from .utility import (
    Name,
)
