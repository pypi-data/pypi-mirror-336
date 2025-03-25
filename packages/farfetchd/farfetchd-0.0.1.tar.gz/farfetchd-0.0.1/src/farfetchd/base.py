from typing import Generic, List, TypeVar, Type
from urllib.parse import parse_qs, urljoin, urlparse


from ._farfetchd import Farfetchd
from .models.generic import NamedAPIResource
from .resources import CacheableResourceList, PaginationArguments


T = TypeVar("T")


class ObjectManager(Generic[T]):
    def __init__(self, model_type: Type[T]) -> None:
        self._model_type = model_type

    async def get(self, **kwargs: dict[str, str | int]) -> T:
        definer = Farfetchd.definers.get(self._model_type)
        definition = definer(**kwargs)

        return await Farfetchd.resolvers.resolve(definition)

    async def all(self, offset=None, limit=None) -> List[NamedAPIResource[T]]:
        definer = Farfetchd.definers.get(self._model_type)

        pagination_args = None
        if offset is not None or limit is not None:
            pagination_args = PaginationArguments(offset=offset, limit=limit)
            definition = definer(pagination=pagination_args)
            response = await Farfetchd.resolvers.resolve(definition)
            return [
                NamedAPIResource(i.name, i.url, self._model_type)
                for i in response.results
            ]
        else:
            items = []
            definition = definer(pagination=PaginationArguments())
            response = await Farfetchd.resolvers.resolve(definition)
            items.extend(
                [
                    NamedAPIResource(i.name, i.url, self._model_type)
                    for i in response.results
                ]
            )

            while len(items) < response.count:
                parsed_url = urlparse(response.next)
                url_without_args = urljoin(response.next, parsed_url.path)
                query_args = parse_qs(parsed_url.query, keep_blank_values=True)
                limit = query_args.get("limit")
                offset = query_args.get("offset")
                definition = CacheableResourceList(
                    self._model_type,
                    PaginationArguments(offset=offset, limit=limit),
                    url_without_args,
                )
                response = await Farfetchd.resolvers.resolve(definition)

                items.extend(
                    [
                        NamedAPIResource(i.name, i.url, self._model_type)
                        for i in response.results
                    ]
                )

            return items


class Meta(type):
    def __new__(cls, name, bases, dct):
        response = super().__new__(cls, name, bases, dct)
        response.objects = ObjectManager(response)
        return response


class Model(Generic[T], metaclass=Meta):
    objects: ObjectManager[T]
