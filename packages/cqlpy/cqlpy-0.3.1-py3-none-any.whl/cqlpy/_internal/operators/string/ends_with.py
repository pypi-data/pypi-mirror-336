from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.string import String

from cqlpy._internal.types.null import Null, Some

from cqlpy._internal.operators.nullological.is_null import is_null


def ends_with(argument: String, suffix: String) -> Some[Boolean]:
    """
    Returns true if the argument ends with the given suffix, false otherwise.

    [Specification](https://cql.hl7.org/09-b-cqlreference.html#endswith)

    ## Parameters

    - `argument`: The string to check.
    - `suffix`: The suffix to check for.

    ## Returns

    True if the argument ends with the given suffix, false otherwise.

    ## Usage

    ```python
    ends_with(String("Hello, world!"), String("world!"))  # True
    ends_with(String("Hello, world!"), String("world"))  # False
    ```
    """
    if is_null(argument) or is_null(suffix):
        return Null()
    return Boolean(argument[-len(suffix) :] == suffix)
