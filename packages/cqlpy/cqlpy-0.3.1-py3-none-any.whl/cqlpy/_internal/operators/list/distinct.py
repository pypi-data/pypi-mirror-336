from typing import TypeVar

from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.list import List

_DistinctType = TypeVar("_DistinctType", bound=CqlAny)


def distinct(argument: List[_DistinctType]) -> List[_DistinctType]:
    """
    Returns a list containing only the distinct elements of the given list.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#distinct)

    ## Parameters

    - `argument`: The list to get the distinct elements of.

    ## Returns

    A list containing only the distinct elements of the given list.

    ## Usage

    ```python
    distinct([1, 2, 3, 2, 1])  # [1, 2, 3]
    ```
    """
    result = []
    for item in argument:
        if not (item in result):
            result.append(item)
    return List(result)
