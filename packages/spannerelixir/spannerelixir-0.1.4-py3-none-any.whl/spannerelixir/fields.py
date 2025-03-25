"""
Field definitions for SpannerElixir models.
"""

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional


class Field:
    """Base field class for model attributes"""

    def __init__(
        self,
        primary_key: bool = False,
        nullable: bool = True,
        default: Any = None,
        index: bool = False,
        unique: bool = False,
        description: Optional[str] = None,
    ):
        """
        Initialize a Field instance.

        Args:
            primary_key: Whether this field is part of the primary key
            nullable: Whether this field can be NULL
            default: Default value or callable returning a default value
            index: Whether to create an index on this field
            unique: Whether this field's values must be unique
            description: Optional description of the field
        """
        self.primary_key = primary_key
        self.nullable = nullable
        self.default = default
        self.index = index
        self.unique = unique
        self.description = description
        self.name = None  # Will be set by the model metaclass

    def to_db_value(self, value: Any) -> Any:
        """Convert Python value to a Spanner-compatible value"""
        return value

    def from_db_value(self, value: Any) -> Any:
        """Convert Spanner value to a Python value"""
        return value

    def get_spanner_type(self) -> str:
        """Get the Spanner column type for this field"""
        raise NotImplementedError("Subclasses must implement get_spanner_type()")


class StringField(Field):
    """String field type, maps to Spanner STRING type."""

    def __init__(self, max_length: Optional[int] = None, **kwargs):
        """
        Initialize a StringField.

        Args:
            max_length: Maximum length for the string
            **kwargs: Additional field options
        """
        super().__init__(**kwargs)
        self.max_length = max_length

    def to_db_value(self, value: Any) -> Optional[str]:
        """Convert value to string for Spanner."""
        return str(value) if value is not None else None

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        if self.max_length is None:
            return "STRING(MAX)"
        return f"STRING({self.max_length})"


class NumericField(Field):
    """Numeric field type, maps to Spanner NUMERIC type."""

    def __init__(self, precision: Optional[int] = None, scale: Optional[int] = None, **kwargs):
        """
        Initialize a NumericField.

        Args:
            precision: Total digits (default: Spanner's maximum)
            scale: Decimal places (default: Spanner's maximum)
            **kwargs: Additional field options
        """
        super().__init__(**kwargs)
        self.precision = precision
        self.scale = scale

    def to_db_value(self, value: Any) -> Optional[Decimal]:
        """Convert value to Decimal for Spanner."""
        if value is None:
            return None
        return Decimal(str(value))

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        if self.precision is not None and self.scale is not None:
            return f"NUMERIC({self.precision}, {self.scale})"
        return "NUMERIC"


class IntegerField(Field):
    """Integer field type, maps to Spanner INT64 type."""

    def to_db_value(self, value: Any) -> Optional[int]:
        """Convert value to int for Spanner."""
        return int(value) if value is not None else None

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        return "INT64"


class BooleanField(Field):
    """Boolean field type, maps to Spanner BOOL type."""

    def to_db_value(self, value: Any) -> Optional[bool]:
        """Convert value to bool for Spanner."""
        return bool(value) if value is not None else None

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        return "BOOL"


class DateTimeField(Field):
    """
    DateTime field type, maps to Spanner TIMESTAMP type.

    NOTE: Spanner's TIMESTAMP type has microsecond precision.
    """

    def __init__(
        self,
        auto_now: bool = False,
        auto_now_add: bool = False,
        allow_commit_timestamp: bool = False,
        **kwargs,
    ):
        """
        Initialize a DateTimeField.

        Args:
            auto_now: Automatically set to current time on every save
            auto_now_add: Automatically set to current time on creation only
            allow_commit_timestamp: Allow setting to commit timestamp
            **kwargs: Additional field options
        """
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        self.allow_commit_timestamp = allow_commit_timestamp

        # If auto_now or auto_now_add is True and no default is provided,
        # set default to current time
        if (auto_now_add or auto_now) and kwargs.get("default") is None:
            self.default = lambda: datetime.now()

    def to_db_value(self, value: Any) -> Optional[datetime]:
        """Convert value to datetime for Spanner."""
        if value is None:
            return None
        if isinstance(value, str):
            # Parse string to datetime
            return datetime.fromisoformat(value)
        return value

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        if self.allow_commit_timestamp:
            return "TIMESTAMP OPTIONS (allow_commit_timestamp = true)"
        return "TIMESTAMP"


class DateField(Field):
    """Date field type, maps to Spanner DATE type."""

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        return "DATE"


class FloatField(Field):
    """Float field type, maps to Spanner FLOAT64 type."""

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        return "FLOAT64"


class BytesField(Field):
    """Bytes field type, maps to Spanner BYTES type."""

    def __init__(self, max_length: Optional[int] = None, **kwargs):
        """
        Initialize a BytesField.

        Args:
            max_length: Maximum length in bytes
            **kwargs: Additional field options
        """
        super().__init__(**kwargs)
        self.max_length = max_length

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        if self.max_length is None:
            return "BYTES(MAX)"
        return f"BYTES({self.max_length})"


class ArrayField(Field):
    """Array field type, maps to Spanner ARRAY type."""

    def __init__(self, item_field: Field, **kwargs):
        """
        Initialize an ArrayField.

        Args:
            item_field: Field type for array items
            **kwargs: Additional field options
        """
        super().__init__(**kwargs)
        self.item_field = item_field

    def to_db_value(self, value: Any) -> Optional[list]:
        """Convert value to list for Spanner, processing each item."""
        if value is None:
            return None
        return [self.item_field.to_db_value(item) for item in value]

    def get_spanner_type(self) -> str:
        """Get Spanner type definition."""
        return f"ARRAY<{self.item_field.get_spanner_type()}>"
