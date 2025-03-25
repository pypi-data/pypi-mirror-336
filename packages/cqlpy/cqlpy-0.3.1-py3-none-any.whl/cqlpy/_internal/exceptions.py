class CqlPyError(Exception):
    """
    Base class for all CQLPy exceptions.
    """

    ...


class CqlPyValueError(CqlPyError, ValueError):
    """
    A CQLPy exception for when a value is invalid.
    """

    ...


class CqlPyTypeError(CqlPyError, TypeError):
    """
    A CQLPy exception for when a type is invalid.
    """

    ...


class CqlPyKeyError(CqlPyError, KeyError):
    """
    A CQLPy exception for when a key is invalid.
    """

    ...


class CqlPyUnsupportedError(CqlPyError):
    """
    A CQLPy exception for when a feature is unsupported.
    """

    ...


class CqlParseError(CqlPyValueError):
    """
    Appears when a CQL expression cannot be parsed.
    """

    ...


class ValuesetProviderError(CqlPyError):
    """
    Appears when a valueset provider cannot be used.
    """

    ...


class ValuesetReadError(CqlPyError):
    """
    Appears when a valueset cannot be read, usually from disk.
    """

    ...


class ValuesetInterpretationError(ValuesetReadError):
    """
    Appears when a valueset cannot be interpreted, usually because it is
    invalid. This can also sometimes occur due to invalid encoding.
    """

    ...
