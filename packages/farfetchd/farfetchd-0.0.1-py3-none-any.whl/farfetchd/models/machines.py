"""
!!Generated code!!

Do not modify directly.

Generation script is located @ //farfetchd/bin/generate.py
"""

from __future__ import annotations
from dataclasses import dataclass


from ..base import Model


@dataclass
class Machine(Model["Machine"]):
    # The identifier for this resource.
    id: int  # pylint: disable=invalid-name
    # The TM or HM item that corresponds to this machine.
    item: NamedAPIResource[Item]
    # The move that is taught by this machine.
    move: NamedAPIResource[Move]
    # The version group that this machine applies to.
    version_group: NamedAPIResource[VersionGroup]


# import all type hints at of file to ensure no circular reference issues
# pylint: disable=wrong-import-position,wrong-import-order

from .games import (
    VersionGroup,
)

from .generic import (
    NamedAPIResource,
)

from .items import (
    Item,
)

from .moves import (
    Move,
)
