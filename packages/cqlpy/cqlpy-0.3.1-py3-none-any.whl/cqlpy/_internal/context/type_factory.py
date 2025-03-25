from typing import Optional, Type

from cqlpy._internal.exceptions import CqlPyTypeError
from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.list import List
from cqlpy._internal.types.long import Long
from cqlpy._internal.types.string import String

from cqlpy._internal.context.fhir.fhir_cql_type import (
    FhirChoice,
    FhirCqlType,
    FhirList,
    FhirInterval,
)

NAME_TO_CQL_TYPE_MAP: dict[str, Type[CqlAny]] = {
    "Boolean": Boolean,
    "Code": Code,
    "Concept": Concept,
    "Date": Date,
    "DateTime": DateTime,
    "Decimal": Decimal,
    "Integer": Integer,
    "Interval": Interval,
    "List": List,
    "String": String,
    "Long": Long,
}


def _split_generic_name(name: str) -> tuple[str, Optional[str]]:
    if "<" in name:
        split_name = name.split("<")
        return split_name[0], split_name[1][:-1]
    else:
        return name, None


def _map_cql_type(type_name: Optional[str]) -> Optional[Type[CqlAny]]:
    if type_name is None:
        return None

    return NAME_TO_CQL_TYPE_MAP[type_name]


class TypeFactory:
    @staticmethod
    def get_type(type_name: str) -> tuple[Type[CqlAny], Optional[Type[CqlAny]]]:
        cql_name, subtype_name = _split_generic_name(type_name)
        cql_type, subtype = _map_cql_type(cql_name), _map_cql_type(subtype_name)

        if cql_type is None:
            raise CqlPyTypeError(f"Unknown CQL type: {type_name}")

        return cql_type, subtype

    @staticmethod
    def get_type_from_fhir_cql(
        fhir_cql_type: FhirCqlType,
    ) -> tuple[Type[CqlAny], Optional[Type[CqlAny]]]:
        if isinstance(fhir_cql_type, FhirChoice):
            raise ValueError("Cannot select single CQL type from FHIR choice")

        cql_type = _map_cql_type(fhir_cql_type.name)
        if cql_type is None:
            raise ValueError(f"Unknown CQL type: {fhir_cql_type.name}")

        if isinstance(fhir_cql_type, FhirList) or isinstance(
            fhir_cql_type, FhirInterval
        ):
            return (
                cql_type,
                TypeFactory.get_type_from_fhir_cql(fhir_cql_type.item_type)[0],
            )

        return cql_type, None
