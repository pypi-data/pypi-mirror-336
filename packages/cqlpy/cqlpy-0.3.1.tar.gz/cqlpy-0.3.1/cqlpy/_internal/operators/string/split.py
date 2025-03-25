from cqlpy._internal.types.string import String
from cqlpy._internal.types.list import List

from cqlpy._internal.types.null import Null, Some

from cqlpy._internal.operators.nullological.is_null import is_null


def split(string_to_split: String, separator: String) -> Some[List[String]]:
    """
    Splits the given string into a list of strings using the given separator.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#split)

    ## Parameters

    - `string_to_split`: The string to split.
    - `separator`: The separator to split on.

    ## Returns

    A `List` of `Strings`.

    ## Usage

    ```python
    split(String("Hello, world!"), String(", "))  # List([String("Hello"), String("world!")])
    ```
    """
    if is_null(string_to_split) or is_null(separator):
        return Null()
    return List([String(part) for part in string_to_split.split(separator)])
