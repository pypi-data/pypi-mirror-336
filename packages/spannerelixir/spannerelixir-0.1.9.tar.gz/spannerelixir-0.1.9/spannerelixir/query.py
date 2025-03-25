"""
Query builder for SpannerElixir.
"""

from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from google.cloud.spanner_v1.database import Database

from spannerelixir.exceptions import RecordNotFoundError
from spannerelixir.model import SpannerModel
from spannerelixir.utils import get_model_class

T = TypeVar("T", bound=SpannerModel)


class JoinType:
    """Enum-like class for JOIN types."""

    INNER = "INNER JOIN"
    LEFT = "LEFT JOIN"
    RIGHT = "RIGHT JOIN"
    FULL = "FULL JOIN"


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

        # With join:
        user_orgs = (
            session.query(OrganizationUser)
            .join("Users", "UserID", "UserID", join_type=JoinType.INNER)
            .filter(Status="ACTIVE")
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
        self.join_clauses = []
        self.table_aliases = {model_class._table_name: "t0"}
        self.next_alias_index = 1
        self.joined_models = {}  # Maps joined model classes to their aliases

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

    def join(
        self,
        related_model: Union[str, Type[SpannerModel]],
        from_field: str,
        to_field: str,
        join_type: str = JoinType.INNER,
        alias: Optional[str] = None,
    ) -> "Query[T]":
        """
        Add a JOIN clause to the query.

        Args:
            related_model: Related model class or name to join with
            from_field: Field name in the base model
            to_field: Field name in the related model
            join_type: Type of join (INNER, LEFT, RIGHT, FULL)
            alias: Optional alias for the joined table

        Returns:
            Query: Self for method chaining
        """
        # Get the related model class if a string was provided
        if isinstance(related_model, str):
            related_model_class = get_model_class(related_model)
        else:
            related_model_class = related_model

        # Generate table alias if not provided
        if alias is None:
            alias = f"t{self.next_alias_index}"
            self.next_alias_index += 1

        # Store the joined model class with its alias
        self.joined_models[related_model_class] = alias
        self.table_aliases[related_model_class._table_name] = alias

        # Add the join clause
        base_table_alias = self.table_aliases[self.model_class._table_name]
        join_clause = f"{join_type} {related_model_class._table_name} AS {alias} ON {base_table_alias}.{from_field} = {alias}.{to_field}"
        self.join_clauses.append(join_clause)

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

            # Qualify fields with table aliases
            base_alias = self.table_aliases[self.model_class._table_name]
            qualified_fields = [f"{base_alias}.{field}" for field in fields_to_select]
            fields_clause = ", ".join(qualified_fields)
        else:
            # Select all fields from base table, qualified with alias
            base_alias = self.table_aliases[self.model_class._table_name]
            fields_clause = f"{base_alias}.*"

            # If we have joins, we might want to select fields from joined tables as well
            # This is more complex as we need to handle field name conflicts
            # For simplicity, we'll leave it as is for now

        base_table = self.model_class._table_name
        base_alias = self.table_aliases[base_table]
        sql = f"SELECT {fields_clause} FROM {base_table} AS {base_alias}"

        # Add joins if any
        if self.join_clauses:
            sql += " " + " ".join(self.join_clauses)

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

                    # Qualify field with table alias
                    qualified_field = f"{base_alias}.{field}"
                    conditions.append(f"{qualified_field} IN ({', '.join(placeholders)})")
                else:
                    # For other operators
                    param_name = f"p{i}"

                    # Qualify field with table alias
                    qualified_field = f"{base_alias}.{field}"
                    conditions.append(f"{qualified_field} {op} @{param_name}")
                    params[param_name] = self.model_class._fields[field].to_db_value(value)
                    # Would set param_types here based on field type

            sql += f" WHERE {' AND '.join(conditions)}"

        if self.order_by_clauses:
            # Qualify field names with table aliases
            qualified_order_by = []
            for clause in self.order_by_clauses:
                field, direction = clause.rsplit(" ", 1)
                qualified_order_by.append(f"{base_alias}.{field} {direction}")

            sql += f" ORDER BY {', '.join(qualified_order_by)}"

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
            List[T]: List of model instances
        """
        sql, params, param_types = self._build_query()

        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(sql, params=params, param_types=param_types)

            # Handle potential empty results or None metadata
            if not results or not hasattr(results, "fields") or results.fields is None:
                return []

            # Get the field names in the same order as the query results
            field_names = []
            for column in results.fields:
                # Column might be qualified with table alias (t0.field_name)
                # Extract just the field name
                if "." in column.name:
                    field_names.append(column.name.split(".")[-1])
                else:
                    field_names.append(column.name)

            # Convert rows to model instances
            instances = []
            for row in results:
                instance = self.model_class.from_query_result(row, field_names)
                instances.append(instance)

        return instances

    def first(self) -> Optional[T]:
        """
        Get first result or None.

        Returns:
            Optional[T]: First matching model instance or None
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
            T: First matching model instance

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
