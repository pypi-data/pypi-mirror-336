from typing import Optional, Type
from cqlpy._internal.types.any import CqlAny

from cqlpy._internal.types.datetime import DateTime


class Date(DateTime):
    """
    Represents a CQL date.

    [Specification](http://cql.hl7.org/09-b-cqlreference.html#date)
    """

    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
    ):
        """
        Creates a new Date.

        ## Parameters

        - `year`: The year of the Date.
        - `month`: The month of the Date.
        - `day`: The day of the Date.
        """
        super().__init__(year, month, day)

    @classmethod
    def parse_fhir_json(
        cls, fhir_json: object, subtype: Optional[Type["CqlAny"]] = None
    ) -> "Date":
        super_time = DateTime.parse_fhir_json(fhir_json, subtype)
        return cls(
            year=super_time.value.year,
            month=super_time.value.month,
            day=super_time.value.day,
        )

    @classmethod
    def parse_cql(cls, cql: str, subtype: Optional[Type[CqlAny]] = None) -> "Date":
        super_time = DateTime.parse_cql(cql, subtype)
        return cls(
            year=super_time.value.year,
            month=super_time.value.month,
            day=super_time.value.day,
        )
