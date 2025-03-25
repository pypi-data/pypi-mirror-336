import functools
from typing import Callable, Dict, ParamSpec, TypeVar, Type

from .resources import CacheableResource, CacheableResourceList
from ._farfetchd import Farfetchd

T = TypeVar("T")
P = ParamSpec("P")

CachedT = CacheableResource[T] | CacheableResourceList[T]


def defines(defined_type: Type[T]):
    def decorator(function: Callable[P, CachedT]) -> Callable[P, CachedT]:
        @functools.wraps(function)
        def decorated(*args, **kwargs):
            return function(*args, **kwargs)

        Farfetchd.definers.register(defined_type, decorated)
        return decorated

    return decorator


def memoize(function: Callable[P, T]) -> Callable[P, T]:
    # todo: allow multiple arguments
    # todo: allow this to empty when memory is low
    usage_cache: Dict[str, T] = {}

    @functools.wraps(function)
    def decorated(arg):
        if arg in usage_cache:
            return usage_cache[arg]
        result = function(arg)

        # do not memoize None
        if result is not None:
            usage_cache[arg] = result

        return result

    return decorated
