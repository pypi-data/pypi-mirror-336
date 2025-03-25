"""
Exception classes for SpannerElixir.
"""


class SpannerElixirError(Exception):
    """Base exception class for all SpannerElixir errors."""

    pass


class ModelDefinitionError(SpannerElixirError):
    """Raised when there is an error in the model definition."""

    pass


class ValidationError(SpannerElixirError):
    """Raised when data validation fails."""

    pass


class RecordNotFoundError(SpannerElixirError):
    """Raised when a record cannot be found."""

    pass


class MultipleRecordsFoundError(SpannerElixirError):
    """Raised when multiple records are found but only one was expected."""

    pass


class TransactionError(SpannerElixirError):
    """Raised when there is an error with a transaction."""

    pass


class ConnectionError(SpannerElixirError):
    """Raised when there is an error connecting to the database."""

    pass
