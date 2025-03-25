"""
Query builder for SpannerElixir.
"""

from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from google.cloud.spanner_v1.database import Database

from spannerelixir.exceptions import RecordNotFoundError
from spannerelixir.model import SpannerModel

T = TypeVar("T", bound=SpannerModel)


class Query(Generic[T]):
    """
    Query builder for SpannerElixir models.

    Example:
        products = (
            session.query(Product)
            .filter(Active=True, Category="Electronics")
            .order_by("Price", desc=True)
            .limit(10)
            .all()
        )
    """

    def __init__(self, model_class: Type[T], database: Database):
        """
        Initialize a query builder.

        Args:
            model_class: The model class to query
            database: Spanner database instance
        """
        self.model_class = model_class
        self.database = database
        self.filters = []
        self.order_by_clauses = []
        self.limit_value = None
        self.offset_value = None
        self.select_fields = None  # None means select all fields

    def select(self, *fields) -> "Query[T]":
        """
        Select specific fields from the model.

        Args:
            *fields: Field names to select

        Returns:
            Query: Self for method chaining
        """
        self.select_fields = list(fields)
        return self

    def filter(self, **kwargs) -> "Query[T]":
        """
        Add equality filter conditions.

        Args:
            **kwargs: Field=value pairs for filtering

        Returns:
            Query: Self for method chaining
        """
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.filters.append((key, "=", value))
        return self

    def filter_lt(self, **kwargs) -> "Query[T]":
        """Add less-than filter conditions."""
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.filters.append((key, "<", value))
        return self

    def filter_lte(self, **kwargs) -> "Query[T]":
        """Add less-than-or-equal filter conditions."""
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.filters.append((key, "<=", value))
        return self

    def filter_gt(self, **kwargs) -> "Query[T]":
        """Add greater-than filter conditions."""
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.filters.append((key, ">", value))
        return self

    def filter_gte(self, **kwargs) -> "Query[T]":
        """Add greater-than-or-equal filter conditions."""
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.filters.append((key, ">=", value))
        return self

    def filter_in(self, field: str, values: List[Any]) -> "Query[T]":
        """
        Add IN filter condition.

        Args:
            field: Field name to filter on
            values: List of values to match against

        Returns:
            Query: Self for method chaining
        """
        if field in self.model_class._fields and values:
            self.filters.append((field, "IN", values))
        return self

    def filter_not(self, **kwargs) -> "Query[T]":
        """Add inequality filter conditions."""
        for key, value in kwargs.items():
            if key in self.model_class._fields:
                self.filters.append((key, "!=", value))
        return self

    def order_by(self, field_name: str, desc: bool = False) -> "Query[T]":
        """
        Add ordering clause.

        Args:
            field_name: Field to order by
            desc: If True, order in descending order

        Returns:
            Query: Self for method chaining
        """
        if field_name in self.model_class._fields:
            direction = "DESC" if desc else "ASC"
            self.order_by_clauses.append(f"{field_name} {direction}")
        return self

    def limit(self, limit_value: int) -> "Query[T]":
        """
        Add LIMIT clause.

        Args:
            limit_value: Maximum number of records to return

        Returns:
            Query: Self for method chaining
        """
        self.limit_value = limit_value
        return self

    def offset(self, offset_value: int) -> "Query[T]":
        """
        Add OFFSET clause.

        Args:
            offset_value: Number of records to skip

        Returns:
            Query: Self for method chaining
        """
        self.offset_value = offset_value
        return self

    def _build_query(self) -> Tuple[str, Dict[str, Any], Dict[str, Any]]:
        """
        Build SQL query, params and param types.

        Returns:
            Tuple[str, Dict, Dict]: SQL query, parameters, and parameter types
        """
        # Handle field selection
        if self.select_fields:
            # Ensure we include primary keys even if not explicitly selected
            fields_to_select = set(self.select_fields)
            for name, field in self.model_class._fields.items():
                if field.primary_key:
                    fields_to_select.add(name)
            fields_clause = ", ".join(fields_to_select)
        else:
            fields_clause = "*"

        sql = f"SELECT {fields_clause} FROM {self.model_class._table_name}"

        params = {}
        param_types = {}

        if self.filters:
            conditions = []
            for i, (field, op, value) in enumerate(self.filters):
                # Handle different operators
                if op == "IN":
                    # For IN operator, we need to create multiple parameters
                    placeholders = []
                    for j, item in enumerate(value):
                        param_name = f"p{i}_{j}"
                        placeholders.append(f"@{param_name}")
                        params[param_name] = self.model_class._fields[field].to_db_value(item)
                        # Would set param_types here based on field type
                    conditions.append(f"{field} IN ({', '.join(placeholders)})")
                else:
                    # For other operators
                    param_name = f"p{i}"
                    conditions.append(f"{field} {op} @{param_name}")
                    params[param_name] = self.model_class._fields[field].to_db_value(value)
                    # Would set param_types here based on field type

            sql += f" WHERE {' AND '.join(conditions)}"

        if self.order_by_clauses:
            sql += f" ORDER BY {', '.join(self.order_by_clauses)}"

        if self.limit_value is not None:
            sql += f" LIMIT {self.limit_value}"

        if self.offset_value is not None:
            sql += f" OFFSET {self.offset_value}"

        return sql, params, param_types

    def count(self) -> int:
        """
        Count the number of records matching the query.

        Returns:
            int: Count of matching records
        """
        # Start with the filters and WHERE clause from the current query
        sql, params, param_types = self._build_query()

        # Extract just the WHERE clause if it exists
        where_clause = ""
        if " WHERE " in sql:
            where_clause = (
                "WHERE " + sql.split(" WHERE ")[1].split(" ORDER BY ")[0].split(" LIMIT ")[0]
            )

        # Build the count query
        count_sql = f"SELECT COUNT(*) FROM {self.model_class._table_name}"
        if where_clause:
            count_sql += f" {where_clause}"

        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(count_sql, params=params, param_types=param_types)
            row = list(results)[0]
            return row[0]

    def all(self) -> List[T]:
        """
        Execute query and return all results.

        Returns:
            List[Model]: List of model instances
        """
        sql, params, param_types = self._build_query()

        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql, params=params, param_types=param_types)

            instances = []
            for row in results:
                # Use the model's helper method to create an instance from the row
                instance = self.model_class.from_query_result(row, results.fields)
                instances.append(instance)

            return instances

    def first(self) -> Optional[T]:
        """
        Get first result or None.

        Returns:
            Optional[Model]: First matching model instance or None
        """
        # Add limit if not already set
        if self.limit_value is None:
            self.limit(1)

        results = self.all()
        return results[0] if results else None

    def first_or_404(self) -> T:
        """
        Get first result or raise RecordNotFoundError.

        Returns:
            Model: First matching model instance

        Raises:
            RecordNotFoundError: If no matching record is found
        """
        result = self.first()
        if result is None:
            # Construct a useful error message based on the filters
            filter_strs = []
            for field, op, value in self.filters:
                filter_strs.append(f"{field} {op} {value}")

            filter_msg = " AND ".join(filter_strs) if filter_strs else "no filters"
            raise RecordNotFoundError(
                f"{self.model_class.__name__} matching {filter_msg} not found"
            )
        return result
