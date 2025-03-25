from collections.abc import Iterable
from typing import Any, Generic, Type, TypeVar, Optional
from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.null import Some
from cqlpy._internal.types.string import String

_ListItemType = TypeVar("_ListItemType", bound=Some[CqlAny])


class List(Generic[_ListItemType], CqlAny[list[Any], list[_ListItemType]], list):
    def __init__(self, value: list[_ListItemType]):
        self.__value = value

    def __hash__(self) -> int:  # type: ignore
        return hash(tuple(self.value))

    def __len__(self) -> int:
        return len(self.value)

    def __getitem__(self, index):
        return self.value[index]

    def __setitem__(self, index, value) -> None:
        self.value[index] = value

    def __delitem__(self, index) -> None:
        del self.value[index]

    def append(self, value) -> None:
        self.value.append(value)

    def extend(self, value) -> None:
        self.value.extend(value)

    def __contains__(self, value) -> bool:
        return value in self.value

    def __iter__(self):
        return iter(self.value)

    def __reversed__(self):
        return List(reversed(self.value))

    def __iadd__(self, __value: Iterable[Any]) -> "List[_ListItemType]":
        addable = __value.value if isinstance(__value, List) else __value
        return List(self.value.__iadd__(addable))

    def __add__(self, __value: list) -> "List[_ListItemType]":
        addable = __value.value if isinstance(__value, List) else __value
        return List(self.value.__add__(addable))

    @property
    def value(self) -> list[_ListItemType]:
        return self.__value

    @classmethod
    def parse_fhir_json(
        cls,
        fhir_json: list[Any],
        subtype: Optional[Type[CqlAny]] = None,
    ) -> "List[_ListItemType]":
        type_ = subtype or String
        return cls([type_.parse_fhir_json(item) for item in fhir_json])

    @classmethod
    def parse_cql(
        cls, cql: str, subtype: Optional[Type[CqlAny]] = None
    ) -> "List[_ListItemType]":
        type_ = subtype or String
        stripped_cql = cql.strip("{}")
        return cls([type_.parse_cql(item.strip()) for item in stripped_cql.split(",")])
