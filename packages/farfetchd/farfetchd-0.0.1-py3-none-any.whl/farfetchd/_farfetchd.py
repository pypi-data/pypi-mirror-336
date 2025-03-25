from threading import Lock

import aiohttp

from .registry import Registry, ResolverRegistry


class Farfetchd:
    _session_lock = Lock()
    _session: aiohttp.ClientSession | None = None
    definers = Registry()
    resolvers = ResolverRegistry()

    @classmethod
    async def session(cls) -> aiohttp.ClientSession:
        if cls._session is None:
            with cls._session_lock:
                if cls._session is None:
                    cls._session = aiohttp.ClientSession()
        return cls._session
