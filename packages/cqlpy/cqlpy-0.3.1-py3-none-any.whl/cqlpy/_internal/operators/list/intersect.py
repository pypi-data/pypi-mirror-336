from typing import TypeVar, Union
from cqlpy._internal.operators.nullological.is_null import is_null
from cqlpy._internal.operators.interval.overlaps import overlaps
from cqlpy._internal.types.code import Code
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.null import Null

from cqlpy._internal.types.list import List

_IntersectType = TypeVar(
    "_IntersectType",
    bound=Union[
        list[Code],
        list[DateTime],
        list[Date],
        list[Integer],
        list[Decimal],
        Interval[DateTime],
        Interval[Date],
        Interval[Integer],
        Interval[Decimal],
    ],
)
_IntersectListTypes = Union[Code, DateTime, Date, Integer, Decimal]


def intersect(
    left: _IntersectType,
    right: _IntersectType,
) -> Union[_IntersectType, Null]:
    """
    Returns the set intersection of the given lists or intervals. Items in the
    arguments must be comparable and `DateTime`, `Date`, `Integer`, or `Decimal`
    for intervals. `Code`s can be used if both arguments are lists.

    If either argument is `Null`, the result is `Null`.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#intersect-1)

    ## Parameters

    - `left`: The first list or interval.
    - `right`: The second list or interval.

    ## Returns

    The common items of the given lists or intervals.

    ## Usage

    ```python
    intersect([1, 2, 3], [2, 3, 4])  # [2, 3]
    ```
    """
    if (is_null(left)) or (is_null(right)):
        return Null()

    if isinstance(left, Interval) and isinstance(right, Interval):
        if not (
            isinstance(left.low, DateTime)
            and isinstance(right.low, DateTime)
            and isinstance(left.high, DateTime)
            and isinstance(right.high, DateTime)
        ):
            return Null()
        if overlaps(left, right):
            return Interval(  # type: ignore
                DateTime.parse_datetime(max(left.low.value, right.low.value)),
                False,
                DateTime.parse_datetime(min(left.high.value, right.high.value)),
                False,
            )
        return Null()

    if isinstance(left, list) and isinstance(right, list):
        return_list: list[_IntersectListTypes] = []
        for left_item in left:
            for right_item in right:
                if isinstance(left_item, Code) and isinstance(right_item, Code):
                    if left_item.code == right_item.code:
                        return_list.append(left_item)

                else:
                    if left_item == right_item:
                        return_list.append(left_item)

        return List(return_list)  # type: ignore

    return Null()
