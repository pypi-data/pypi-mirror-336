from typing import TypeVar

from cqlpy._internal.operators.list.distinct import distinct
from cqlpy._internal.types.list import List
from cqlpy._internal.types.any import CqlAny


_UnionType = TypeVar("_UnionType", bound=CqlAny)


def union(left: List[_UnionType], right: List[_UnionType]) -> list[_UnionType]:
    """
    Returns a list containing the elements of both the left and right
    lists with duplicates removed.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#union-1)

    ## Parameters

    - `left`: The left list.
    - `right`: The right list.

    ## Returns

    A list containing the elements of both the left and right lists.

    ## Usage

    ```python
    union([1, 2], [3, 4])  # [1, 2, 3, 4]
    ```
    """
    return distinct(left + right)
