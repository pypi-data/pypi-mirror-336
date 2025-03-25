from datetime import timedelta

from .resolvers.memory import MemoryCacheResolver
from .resolvers.network import ApiResolver
from .serialization import DataclassDeserializer
from ._farfetchd import Farfetchd

# import has side effects (registers all definition providers)
# should not be removed
from .defs import * # pylint: disable=wildcard-import,unused-wildcard-import


def default():
    Farfetchd.resolvers.register(-1, ApiResolver(DataclassDeserializer()))
    Farfetchd.resolvers.register(100, MemoryCacheResolver(timedelta(hours=2)))
