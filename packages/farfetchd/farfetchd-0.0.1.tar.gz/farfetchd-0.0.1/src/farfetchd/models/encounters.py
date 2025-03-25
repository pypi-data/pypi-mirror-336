"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class EncounterMethod(Model["EncounterMethod"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # A good value for sorting.
    order: int
    # The name of this resource listed in different languages.
    names: List[Name]


@dataclass
class EncounterCondition(Model["EncounterCondition"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The name of this resource listed in different languages.
    names: List[Name]
    # A list of possible values for this encounter condition.
    values: List[NamedAPIResource[EncounterConditionValue]]


@dataclass
class EncounterConditionValue(Model["EncounterConditionValue"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The name for this resource.
    name: str
    # The condition this encounter condition value pertains to.
    condition: NamedAPIResource[EncounterCondition]
    # The name of this resource listed in different languages.
    names: List[Name]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from typing import (
    List,
)

from .generic import (
    NamedAPIResource,
)

from .utility import (
    Name,
)
