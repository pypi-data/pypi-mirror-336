import abc
import collections
import dataclasses
from pydoc import locate

from typing import Any, Dict, TypeVar, Type

from .decorators import memoize


T = TypeVar("T")


class Deserializer(abc.ABC):
    @abc.abstractmethod
    def from_dict(
        self, model_type: Type[T], values: Dict[str, Any], generic_type: Type = None
    ) -> T:
        raise NotImplementedError()


@dataclasses.dataclass
class TypeHint:
    type: Type
    generic: "TypeHint | None"


class DataclassDeserializer(Deserializer):
    _primatives = {
        int,
        str,
        bool,
    }

    def from_dict(
        self, model_type: Type[T], values: Dict[str, Any], generic_type: Type = None
    ) -> T:
        if not dataclasses.is_dataclass(model_type):
            raise ValueError("provided type is not a dataclass")

        transformed = {}

        fields = dataclasses.fields(model_type)
        for field in fields:
            if field.name in values:
                parsed = DataclassDeserializer._parse_generic_type_hint(field.type)
                if parsed.type in self._primatives:
                    transformed[field.name] = values[field.name]
                    continue

                if parsed.type is list:
                    new_list = [
                        self.from_dict(
                            parsed.generic.type,
                            vals,
                            parsed.generic.generic.type
                            if parsed.generic.generic
                            else None,
                        )
                        for vals in values[field.name]
                    ]
                    transformed[field.name] = new_list
                    continue

                if dataclasses.is_dataclass(parsed.type):
                    sub_generic_type = parsed.generic.type if parsed.generic else None
                    converted = self.from_dict(
                        parsed.type, values[field.name], sub_generic_type
                    )
                    transformed[field.name] = converted
                else:
                    raise ValueError(
                        f"unsupported field in dataclass {model_type}: {field.name} ({field.type})"
                    )

        if generic_type:
            transformed["type"] = generic_type

        return model_type(**transformed)

    @staticmethod
    @memoize
    def _parse_generic_type_hint(type_hint: str) -> TypeHint:
        # todo: does NOT work with multi-type generics
        hint_stack = collections.deque()

        current = type_hint
        generic_index = current.find("[")
        while generic_index != -1:
            type_name = current[:generic_index]
            hint_stack.append(type_name)
            # remove ']' as well - this does not work with multipart generics
            current = current[generic_index + 1 : -1]
            generic_index = current.find("[")

        hint_stack.append(current)

        hint = None
        while hint_stack:
            type_name = hint_stack.pop()

            builtin_type = locate(type_name)
            if builtin_type:
                type_name = builtin_type
            elif type_name == "List":
                type_name = list
            else:
                # import needs to be done here in order to avoid circular dependencies
                from . import models  # pylint: disable=import-outside-toplevel

                model_type = locate(f"{models.__name__}.{type_name}")
                if model_type:
                    type_name = model_type
                else:
                    submodules = [sub for sub in dir(models) if not sub.startswith("_")]

                    found = None
                    for sub in submodules:
                        model_type = locate(f"{models.__name__}.{sub}.{type_name}")
                        if model_type:
                            found = model_type
                            break
                    if found:
                        type_name = found
                    else:
                        # import needs to be done here in order to avoid
                        # circular dependencies
                        from . import (  # pylint: disable=import-outside-toplevel
                            resources,
                        )

                        cache_type = locate(f"{resources.__name__}.{type_name}")
                        if cache_type:
                            type_name = cache_type
                        else:
                            lowered_t = type_name.lower()
                            builtin_type = locate(lowered_t)
                            if builtin_type:
                                type_name = builtin_type
                            else:
                                raise ValueError(f'could not locate type "{type_name}"')

            hint = TypeHint(type_name, hint)

        return hint
