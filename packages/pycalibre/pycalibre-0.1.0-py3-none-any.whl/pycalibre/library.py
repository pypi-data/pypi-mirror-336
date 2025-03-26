"""Library interface for Calibre databases."""

from pathlib import Path
import sqlite3
from typing import Union, Optional, List, Any, Dict, Tuple, Set
import weakref
import re
from datetime import datetime

from sqlalchemy import ColumnElement, Engine, Integer, create_engine, and_, false, or_, not_, Column, Table, text, MetaData, join, select, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import operators
from sqlalchemy.sql.expression import ColumnClause

# Import from refactored models
from .models.base import Base
from .models.book import Book, parse_calibre_datetime
from .models.entities import Author, Tag, Language, Publisher, Series, Rating
from .models.custom import CustomColumn
from .models.format import Format
from .models.comment import Comment
from .models.identifier import Identifier
from .models.enums import FilterOperator
from .models.associations import (
    book_author_association,
    book_tag_association,
    book_language_association,
    book_publisher_association,
    book_series_association,
    book_rating_association
)


def title_sort(title: str) -> str:
    """
    Normalize a book title for sorting purposes.
    
    Args:
        title: The book title to normalize
        
    Returns:
        str: Normalized version of the title suitable for sorting
    """
    if not title:
        return ""
    
    # Convert to lowercase for case-insensitive comparison
    title = title.lower()
    
    # Remove leading articles
    articles = ["the ", "a ", "an "]
    for article in articles:
        if title.startswith(article):
            title = title[len(article):]
            break
    
    # Replace punctuation with spaces
    title = re.sub(r'[^\w\s]', ' ', title)
    
    # Normalize whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title

class Library:
    """ A Calibre library.

    Parameters:
    - path: The file path to the library.
    
    """

    _path: Path
    _db_path: Path
    _engine: Optional[Engine]
    _session_factory: Optional[sessionmaker]
    _session: Optional[Session]

    def __init__(self, path: Union[str, Path]) -> None:
        """Initialize a Library instance.
        
        Args:
            path: Path to the Calibre library directory
            
        Raises:
            ValueError: If the path does not exist
            ValueError: If the path does not contain a metadata.db file
        """
        self._path = Path(path)
        self._db_path = self._path / "metadata.db"
        self._engine = None
        self._session_factory = None 
        self._session = None
        
        # Check if the path exists
        if not self._path.exists():
            raise FileNotFoundError(f"Library path does not exist: {self._path}")
        
        # Check if the metadata.db file exists
        if not self._db_path.exists():
            raise FileNotFoundError(f"Library does not contain a metadata.db file: {self._db_path}")

    @property
    def path(self) -> Path:
        """Get the path to the library.
        
        Returns:
            Path: The path to the library
        """
        return self._path

    @property
    def book_count(self) -> int:
        """Get the number of books in the library.
        
        Returns:
            int: The number of books in the library
            
        Raises:
            RuntimeError: If the library is not open
        """
        if not self._session:
            raise RuntimeError("Library must be opened using a context manager before accessing book count.")
        
        return self._session.query(Book).count()

    @property
    def custom_columns(self) -> List[CustomColumn]:
        """Get all custom columns defined in the library.
        
        Returns:
            List[CustomColumn]: A list of custom column objects.
            
        Raises:
            RuntimeError: If the library is not open.
        """
        if not self._session:
            raise RuntimeError("Library must be opened using a context manager before accessing custom columns.")
        
        return self._session.query(CustomColumn).filter(CustomColumn.mark_for_delete == 0).all()

    @property
    def authors(self) -> List[Author]:
        """Return all authors in the library.
        
        Returns:
            List[Author]: A list of all authors in the library.
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before accessing authors.")
            
        return self._session.query(Author).all()

    @property
    def publishers(self) -> List[Publisher]:
        """Return all publishers in the library.
        
        Returns:
            List[Publisher]: A list of all publishers in the library.
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before accessing publishers.")
            
        return self._session.query(Publisher).all()

    @property
    def series(self) -> List[Series]:
        """Return all series in the library.
        
        Returns:
            List[Series]: A list of all series in the library.
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before accessing series.")
            
        return self._session.query(Series).all()

    @property
    def tags(self) -> List[Tag]:
        """Return all tags in the library.
        
        Returns:
            List[Tag]: A list of all tags in the library.
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before accessing tags.")
            
        return self._session.query(Tag).all()

    def open(self) -> None:
        """Open the library for use when not using a context manager."""
        self.__enter__()

    def close(self) -> None:
        """Close the library when not using a context manager."""
        self.__exit__(None, None, None)
        
    def __enter__(self) -> "Library":
        """Open the library for use.

        Returns:
            Library: The library object.
        """
        # SQLite connection string
        db_uri = f"sqlite:///{self._db_path}"
        
        # Create engine and session factory
        self._engine = create_engine(db_uri)
        self._session_factory = sessionmaker(bind=self._engine)
        
        # Create session
        self._session = self._session_factory()
        
        # Create a connection and register user-defined functions
        @event.listens_for(self._engine, "connect")
        def connect(conn, rec):
            conn.create_function("title_sort", 1, title_sort)
        
        return self

    def __exit__(self, exc_type: Optional[type], exc_value: Optional[Exception], traceback: Optional[type]) -> None:
        """Close the library."""
        if self._session:
            self._session.close()
            self._session = None

    def query_books(
        self, 
        filters: Optional[List[Tuple[str, FilterOperator, Any]]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
        order_by: Optional[List[Tuple[str, bool]]] = None
    ) -> List[Book]:
        """Query books in the library with filters and ordering.
        
        This is a flexible method for querying books with various filters
        and ordering options.
        
        Args:
            filters: List of (column_name, operator, value) tuples
            limit: Maximum number of books to return
            offset: Number of books to skip
            order_by: List of (column_name, is_descending) tuples
            
        Returns:
            List[Book]: A list of Book objects matching the criteria.
            
        Raises:
            RuntimeError: If the library is not open.
            ValueError: If an invalid filter is provided.
        
        Examples:
            Get all books by Jane Austen:
            >>> books = library.query_books([("authors", FilterOperator.CONTAINS, "Jane Austen")])
            
            Get books with rating > 4:
            >>> books = library.query_books([
            ...    ("custom:example_rating_column", FilterOperator.GREATER_THAN, 4)
            ... ])
            
            Get books published after 2020, limit to 10, sorted by title:
            >>> books = library.query_books(
            ...    [("pubdate", FilterOperator.GREATER_THAN, "2020-01-01")],
            ...    limit=10,
            ...    order_by=[("title", False)]
            ... )
        """
        if not self._session:
            raise RuntimeError("Library must be opened using a context manager before querying books.")
        
        # Start with a base query for all books
        query = self._session.query(Book)
        
        # Apply filters if provided
        if filters:
            for column_name, operator, value in filters:
                query = self._apply_filter(query, column_name, operator, value)
        
        # Apply ordering
        if order_by:
            for column_name, is_descending in order_by:
                query = self._apply_ordering(query, column_name, is_descending)
        
        # Apply limit and offset
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        
        books = query.all()
        return self._set_library_reference(books)

    def _apply_filter(self, query, column_name: str, operator: FilterOperator, value: Any):
        """Apply a filter to a query.
        
        Args:
            query: SQLAlchemy query to filter
            column_name: Name of the column or relationship to filter on
            operator: FilterOperator to use
            value: Value to filter by
            
        Returns:
            The modified query
            
        Raises:
            ValueError: If the column name is invalid
        """
        custom_column_names = {col.label for col in self.custom_columns}
        
        # Handle relationships
        if column_name in {'authors', 'tags', 'languages', 'publishers', 'series', 'ratings'}:
            return self._apply_relationship_filter(query, column_name, operator, value)
        
        # Handle direct attributes of Book
        elif hasattr(Book, column_name) and not column_name.startswith('_') and not column_name in custom_column_names:
            return self._apply_direct_attribute_filter(query, column_name, operator, value)
        
        # Handle special case for identifiers (they're not a many-to-many relationship)
        elif column_name == 'identifier':
            return self._apply_identifier_filter(query, operator, value)
        
        # Check if it's a custom column by name directly
        elif column_name in custom_column_names:
            return self._apply_custom_column_filter(query, column_name, operator, value)
        
        # Support legacy "custom:" prefix format
        elif column_name.startswith("custom:"):
            return self._apply_custom_column_filter(query, column_name[7:], operator, value)
        
        # If we get here, it's an unknown column
        else:
            raise ValueError(f"Unknown column: {column_name}")

    def _apply_custom_column_filter(self, query, label: str, operator: FilterOperator, value: Any):
        """Apply a filter for a custom column.
        
        Args:
            query: SQLAlchemy query to filter
            label: Custom column label
            operator: FilterOperator to use
            value: Value to filter by
            
        Returns:
            The modified query
            
        Raises:
            ValueError: If the custom column doesn't exist
        """
        # Find the custom column
        custom_column = self._get_custom_column_by_label(label)
        if not custom_column:
            raise ValueError(f"Custom column with label '{label}' not found")
        
        # Create table objects for the custom column
        metadata = MetaData()
        value_table_name = f"custom_column_{custom_column.id}"
        value_table = Table(value_table_name, metadata, autoload_with=self._engine)
        
        # Create filter expression
        filter_expr = self._create_filter_expression(
            value_table.c.value, operator, value
        )
        
        # For multi-value columns, we need to join through the link table
        if custom_column.is_multiple or custom_column.datatype in {"text", "rating"}:
            link_table_name = f"books_custom_column_{custom_column.id}_link"
            link_table = Table(link_table_name, metadata, autoload_with=self._engine)
            
            # Join the tables
            joined_table = join(
                link_table, value_table,
                link_table.c.value == value_table.c.id
            )
            
            # Apply the filter
            return query.join(
                joined_table,
                Book.id == link_table.c.book
            ).filter(filter_expr)
        
        # For single-value columns, we can filter directly
        else:
            return query.join(
                value_table,
                Book.id == value_table.c.book
            ).filter(filter_expr)

    def _apply_identifier_filter(self, query, operator: FilterOperator, value: Any):
        """Apply a filter for book identifiers.
        
        Args:
            query: SQLAlchemy query to filter
            operator: FilterOperator to use
            value: Value to filter by
            
        Returns:
            The modified query
        """
        # If the value is a list, build a filter for each value
        if isinstance(value, (list, tuple)):
            filters = []
            for val in value:
                # Handle "type:value" format
                if ":" in val:
                    id_type, id_value = val.split(":", 1)
                    filters.append(
                        and_(
                            Book.identifiers.any(identifier_type=id_type),
                            Book.identifiers.any(val=id_value)
                        )
                    )
                # Handle value only (matches any identifier type)
                else:
                    filters.append(Book.identifiers.any(val=val))
            
            # Combine filters based on operator
            if operator in {FilterOperator.EQUALS, FilterOperator.CONTAINS, FilterOperator.IN}:
                return query.filter(or_(*filters))
            else:
                return query.filter(and_(*[not_(f) for f in filters]))
        
        # For a single value
        else:
            # Handle "type:value" format
            if isinstance(value, str) and ":" in value:
                id_type, id_value = value.split(":", 1)
                filter_expr = and_(
                    Book.identifiers.any(identifier_type=id_type),
                    Book.identifiers.any(val=id_value)
                )
            # Handle value only (matches any identifier type)
            else:
                filter_expr = Book.identifiers.any(val=value)
            
            # Apply the operator
            if operator in {FilterOperator.NOT_EQUALS, FilterOperator.NOT_CONTAINS, FilterOperator.NOT_IN}:
                filter_expr = not_(filter_expr)
            
            return query.filter(filter_expr)

    def _apply_relationship_filter(self, query, relationship_name: str, operator: FilterOperator, value: Any):
        """Apply a filter for a book relationship.
        
        Args:
            query: SQLAlchemy query to filter
            relationship_name: Name of the relationship to filter (authors, tags, etc.)
            operator: FilterOperator to use
            value: Value to filter by
            
        Returns:
            The modified query
            
        Raises:
            ValueError: If the operator is not supported for the relationship
        """
        # Map relationship names to model classes and field names
        relationship_mapping = {
            "authors": (Author, "name"),
            "tags": (Tag, "name"),
            "languages": (Language, "lang_code"),
            "publishers": (Publisher, "name"),
            "series": (Series, "name"),
            "ratings": (Rating, "rating")
        }
        
        model_class, field_name = relationship_mapping[relationship_name]
        model_field = getattr(model_class, field_name)
        
        # Create the filter expression based on the operator
        if operator == FilterOperator.EQUALS:
            filter_expr = model_field == value
        elif operator == FilterOperator.NOT_EQUALS:
            filter_expr = model_field != value
        elif operator == FilterOperator.CONTAINS:
            filter_expr = model_field.contains(value)
        elif operator == FilterOperator.NOT_CONTAINS:
            filter_expr = ~model_field.contains(value)
        elif operator == FilterOperator.IN:
            filter_expr = model_field.in_(value if isinstance(value, (list, tuple)) else [value])
        elif operator == FilterOperator.NOT_IN:
            filter_expr = ~model_field.in_(value if isinstance(value, (list, tuple)) else [value])
        elif operator == FilterOperator.GREATER_THAN:
            filter_expr = model_field > value
        elif operator == FilterOperator.LESS_THAN:
            filter_expr = model_field < value
        elif operator == FilterOperator.GREATER_EQUAL:
            filter_expr = model_field >= value
        elif operator == FilterOperator.LESS_EQUAL:
            filter_expr = model_field <= value
        else:
            raise ValueError(f"Unsupported operator {operator} for relationship {relationship_name}")
        
        return query.filter(getattr(Book, relationship_name).any(filter_expr))

    def _apply_direct_attribute_filter(self, query, column_name: str, operator: FilterOperator, value: Any):
        """Apply a filter for a direct attribute of Book.
        
        Args:
            query: SQLAlchemy query to filter
            column_name: Name of the column to filter on
            operator: FilterOperator to use
            value: Value to filter by
            
        Returns:
            The modified query
            
        Raises:
            ValueError: If the operator is not supported for the column
        """
        column = getattr(Book, column_name)
        
        # Create the filter expression
        filter_expr = self._create_filter_expression(column, operator, value)
        
        return query.filter(filter_expr)

    def _create_filter_expression(self, column: Column, operator: FilterOperator, value: Any) -> ColumnElement[bool]:
        """Create a filter expression for a column.
        
        Args:
            column: The column to filter on
            operator: The operator to use
            value: The value to filter by
            
        Returns:
            ColumnElement[bool]: SQLAlchemy filter expression
            
        Raises:
            ValueError: If the operator is not supported
        """
        if operator == FilterOperator.EQUALS:
            return column == value
        elif operator == FilterOperator.NOT_EQUALS:
            return column != value
        elif operator == FilterOperator.GREATER_THAN:
            return column > value
        elif operator == FilterOperator.LESS_THAN:
            return column < value
        elif operator == FilterOperator.GREATER_EQUAL:
            return column >= value
        elif operator == FilterOperator.LESS_EQUAL:
            return column <= value
        elif operator == FilterOperator.CONTAINS:
            if isinstance(value, (list, tuple)):
                return column.in_(value)
            return column.contains(value)
        elif operator == FilterOperator.NOT_CONTAINS:
            if isinstance(value, (list, tuple)):
                return ~column.in_(value)
            return ~column.contains(value)
        elif operator == FilterOperator.IN:
            return column.in_(value if isinstance(value, (list, tuple)) else [value])
        elif operator == FilterOperator.NOT_IN:
            return ~column.in_(value if isinstance(value, (list, tuple)) else [value])
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def _apply_ordering(self, query, column_name: str, is_descending: bool):
        """Apply ordering to a query.
        
        Args:
            query: SQLAlchemy query to order
            column_name: Name of the column to order by
            is_descending: Whether to order in descending order
            
        Returns:
            The modified query
            
        Raises:
            ValueError: If the column name is invalid
        """
        # Handle direct attributes of Book
        if hasattr(Book, column_name) and not column_name.startswith('_'):
            column = getattr(Book, column_name)
            if is_descending:
                return query.order_by(column.desc())
            else:
                return query.order_by(column.asc())
        
        # If we get here, it's an unknown column
        else:
            raise ValueError(f"Unknown column for ordering: {column_name}")

    def find_books(
        self, 
        title: Optional[str] = None,
        author: Optional[Union[str, List[str]]] = None,
        tags: Optional[Union[str, List[str]]] = None,
        identifier: Optional[Union[str, List[str]]] = None,
        language: Optional[str] = None,
        publisher: Optional[str] = None,
        series: Optional[str] = None,
        rating: Optional[int] = None,
        custom_columns: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = 0
    ) -> List[Book]:
        """Find books in the library using a simplified interface.
        
        This is a convenience method that builds filters from the parameters
        and passes them to query_books().
        
        Args:
            title: Find books with this text in the title.
            author: Find books by this author (can be a list for multiple authors).
            tags: Find books with these tags (can be a list for multiple tags).
            identifier: Find books with this identifier (can be a list).
            language: Filter by language code (exact match).
            publisher: Filter by publisher name (contains match).
            series: Filter by series name (contains match).
            rating: Filter by rating (exact match).
            custom_columns: Dictionary mapping custom column labels to values.
            limit: Maximum number of books to return.
            offset: Number of books to skip.
        
        Returns:
            List[Book]: A list of Book objects matching the criteria.
            
        Raises:
            RuntimeError: If the library is not open.
        
        Examples:
            Find books by Jane Austen

            >>> books = library.find_books(author="Jane Austen")
            
            Find books with a specific tag and custom column value

            >>> books = library.find_books(
            ...    tags=["fantasy"],
            ...    custom_columns={"example_rating_column": 5}
            ... )
        """
        # Build a list of filters for query_books
        filters: list[tuple[str, FilterOperator, str | list[str] | int | datetime]] = []
        
        if title:
            filters.append(("title", FilterOperator.CONTAINS, title))

        # Handle identifier filtering
        if identifier:
            if isinstance(identifier, str):
                identifier = [identifier]
            for id_value in identifier:
                filters.append(("identifier", FilterOperator.CONTAINS, id_value))

        if author:
            filters.append(("authors", FilterOperator.CONTAINS, author))
        
        if tags:
            if isinstance(tags, str):
                tags = [tags]
            for tag in tags:
                filters.append(("tags", FilterOperator.CONTAINS, tag))

        if language:
            filters.append(("languages", FilterOperator.EQUALS, language))

        if publisher:
            filters.append(("publishers", FilterOperator.EQUALS, publisher))

        if series:
            filters.append(("series", FilterOperator.CONTAINS, series))
        
        if rating:
            filters.append(("ratings", FilterOperator.EQUALS, rating))
        
        if custom_columns:
            for label, value in custom_columns.items():
                filters.append((f"custom:{label}", FilterOperator.EQUALS, value))
        
        # Use the more flexible query_books method
        books = self.query_books(
            filters=filters,
            limit=limit,
            offset=offset
        )
        return self._set_library_reference(books)

    def _get_custom_column_by_label(self, label: str) -> Optional[CustomColumn]:
        """Get a custom column by its label.
        
        Args:
            label: The label of the custom column
            
        Returns:
            Optional[CustomColumn]: The custom column, or None if it doesn't exist
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before accessing custom columns")
        
        return self._session.query(CustomColumn).filter(
            CustomColumn.label == label,
            CustomColumn.mark_for_delete == 0
        ).first()

    def get_custom_column_value(self, book: Book, column_label: str) -> Any:
        """Get the value of a custom column for a book.
        
        Args:
            book: The book to get the value for
            column_label: The label of the custom column
            
        Returns:
            Any: The value of the custom column
            
        Raises:
            ValueError: If the custom column doesn't exist
            RuntimeError: If the library is not open
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before accessing custom columns")
        
        # Find the custom column
        custom_column = self._get_custom_column_by_label(column_label)
        if not custom_column:
            raise ValueError(f"Custom column with label '{column_label}' not found")
        
        # Create table objects for the custom column
        metadata = MetaData()
        value_table_name = f"custom_column_{custom_column.id}"
        value_table = Table(value_table_name, metadata, autoload_with=self._engine)
        
        # For multi-value columns, we need to join through the link table
        if custom_column.is_multiple or custom_column.datatype in {"text", "rating"}:
            link_table_name = f"books_custom_column_{custom_column.id}_link"
            link_table = Table(link_table_name, metadata, autoload_with=self._engine)
            
            # Get the values through the link table
            query = select(value_table.c.value).select_from(
                link_table.join(value_table, link_table.c.value == value_table.c.id)
            ).where(link_table.c.book == book.id)
            
            result = self._session.execute(query).fetchall()
            values = [row[0] for row in result]
            
            # Handle different data types
            # if custom_column.datatype == "datetime":
            #     values = [parse_calibre_datetime(val) for val in values if val]
            
            return values
        
        # For single-value columns, we can query directly
        else:
            query = select(value_table.c.value).where(value_table.c.book == book.id)
            result_row = self._session.execute(query).fetchone()
            
            if result_row is None:
                # Return a default value based on datatype
                if custom_column.datatype == "bool":
                    return False
                elif custom_column.datatype == "int" or custom_column.datatype == "float":
                    return 0
                else:
                    return None
            
            # Handle different data types
            value = result_row[0]
            # if custom_column.datatype == "datetime" and value:
            #     return parse_calibre_datetime(str(value))
            
            return value

    def _set_library_reference(self, books):
        """Set the library reference on books using a weak reference.
        
        Args:
            books: A book or list of books
            
        Returns:
            The book or list of books with the library reference set
        """
        if isinstance(books, list):
            for book in books:
                book.set_library_reference(self)
        else:
            books.set_library_reference(self)
        
        return books

    def update_book_properties(self, book: Book, **kwargs) -> Book:
        """Update book properties, relationships, and custom column values.
        
        This is the implementation for Book.update() that processes updates to:
        - Basic properties (title, isbn, etc.)
        - Relationship additions (add_authors, add_tags, etc.)
        - Relationship removals (remove_authors, remove_tags, etc.)
        - Identifier additions (add_identifiers=["isbn:1234567890"] or ["1234567890"])
        - Identifier removals (remove_identifiers=["isbn:1234567890"] or ["google:abc123"])
        - Custom column additions (add_example_tag_column, etc.) for multi-value columns
        - Custom column removals (remove_example_tag_column, etc.) for multi-value columns
        - Custom columns (any parameters not matching the above)
        
        Args:
            book: The book to update
            **kwargs: Arbitrary keyword arguments for updates
            
        Returns:
            Book: The updated book
        
        Raises:
            RuntimeError: If the library is not open
            ValueError: If an invalid property is provided
        """
        if not self._session:
            raise RuntimeError("Library must be opened before updating books")
        
        # Categorize updates
        basic_properties = {}
        relationship_additions = {}
        relationship_removals = {}
        custom_column_additions = {}
        custom_column_removals = {}
        custom_columns = {}
        identifier_additions = []
        identifier_removals = []
        
        # Valid types of relationships we can modify
        valid_relationships = {"authors", "tags", "languages", "publishers", "series"}
        
        # Get all custom column labels
        custom_column_labels = {col.label for col in self.custom_columns}
        
        # Identify multi-value custom columns
        multi_value_custom_columns = {
            col.label for col in self.custom_columns 
            if col.is_multiple or col.datatype in {"text", "rating"}
        }
        
        for key, value in kwargs.items():
            # Check if it's adding to a relationship
            if key.startswith('add_') and key[4:] in valid_relationships:
                rel_name = key[4:]  # Extract relationship name (e.g., 'authors')
                relationship_additions[rel_name] = value
            
            # Special handling for identifiers
            elif key == 'add_identifiers':
                identifier_additions = value if isinstance(value, list) else [value]
            
            elif key == 'remove_identifiers':
                identifier_removals = value if isinstance(value, list) else [value]
            
            # Check if it's removing from a relationship
            elif key.startswith('remove_') and key[7:] in valid_relationships:
                rel_name = key[7:]
                relationship_removals[rel_name] = value
            
            # Check if it's adding to a multi-value custom column
            elif key.startswith('add_') and key[4:] in multi_value_custom_columns:
                column_label = key[4:]
                custom_column_additions[column_label] = value
            
            # Check if it's removing from a multi-value custom column
            elif key.startswith('remove_') and key[7:] in multi_value_custom_columns:
                column_label = key[7:]
                custom_column_removals[column_label] = value
            
            # Check if it's a direct attribute of Book
            elif hasattr(Book, key) and not key.startswith('_'):
                basic_properties[key] = value
            
            # Otherwise, assume it's a custom column
            elif key in custom_column_labels:
                custom_columns[key] = value
            
            else:
                raise ValueError(f"Unknown property: {key}")
        
        # Update basic properties
        if basic_properties:
            self._update_book_basic_properties(book, basic_properties)
        
        # Update relationship additions
        for rel_name, values in relationship_additions.items():
            self._add_book_relationship_items(book, rel_name, values)
        
        # Update relationship removals
        for rel_name, values in relationship_removals.items():
            self._remove_book_relationship_items(book, rel_name, values)
        
        # Update identifiers
        if identifier_additions:
            self._add_book_identifiers(book, identifier_additions)
        
        if identifier_removals:
            self._remove_book_identifiers(book, identifier_removals)
        
        # Update custom column additions
        for column_label, values in custom_column_additions.items():
            self._add_multi_value_custom_column_items(book, column_label, values)
        
        # Update custom column removals
        for column_label, values in custom_column_removals.items():
            self._remove_multi_value_custom_column_items(book, column_label, values)
        
        # Update custom columns
        if custom_columns:
            self._update_book_custom_columns(book, custom_columns)
        
        # Commit changes
        self._session.commit()
        
        return book

    def _update_book_basic_properties(self, book: Book, properties: Dict[str, Any]) -> None:
        """Update basic properties of a book.
        
        Args:
            book: The book to update
            properties: Dictionary of properties to update
            
        Raises:
            ValueError: If an invalid property is provided
        """
        valid_properties = {
            "title", "sort", "author_sort", "isbn", "lccn", 
            "path", "flags", "uuid", "has_cover", "series_index",
            "timestamp", "pubdate", "last_modified"
        }
        
        for prop, value in properties.items():
            if prop not in valid_properties and not prop.endswith('_raw'):
                raise ValueError(f"Invalid basic property: {prop}")
            
            # Special handling for datetime properties
            setattr(book, prop, value)

    def _add_book_relationship_items(self, book: Book, relationship_name: str, values: List[str]) -> None:
        """Add items to a book's relationship.
        
        Args:
            book: The book to update
            relationship_name: Name of the relationship to update
            values: List of values to add
            
        Raises:
            ValueError: If an invalid relationship is provided
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
        
        relationship_mapping = {
            "authors": (Author, "name"),
            "tags": (Tag, "name"),
            "languages": (Language, "lang_code"),
            "publishers": (Publisher, "name"),
            "series": (Series, "name")
        }
        
        if relationship_name not in relationship_mapping:
            raise ValueError(f"Invalid relationship: {relationship_name}")
        
        if not values:
            return
            
        model_class, field_name = relationship_mapping[relationship_name]
        current_items = getattr(book, relationship_name)
        current_values = {getattr(item, field_name) for item in current_items}
        
        # Create new entities for values that don't exist
        for value in values:
            if value not in current_values:
                entity = self._session.query(model_class).filter(
                    getattr(model_class, field_name) == value
                ).first()
                
                if not entity:
                    entity = model_class(**{field_name: value})
                    self._session.add(entity)
                
                current_items.append(entity)

    def _remove_book_relationship_items(self, book: Book, relationship_name: str, values: List[str]) -> None:
        """Remove items from a book's relationship.
        
        Args:
            book: The book to update
            relationship_name: Name of the relationship to update
            values: List of values to remove
            
        Raises:
            ValueError: If an invalid relationship is provided
        """
        relationship_mapping = {
            "authors": (Author, "name"),
            "tags": (Tag, "name"),
            "languages": (Language, "lang_code"),
            "publishers": (Publisher, "name"),
            "series": (Series, "name")
        }
        
        if relationship_name not in relationship_mapping:
            raise ValueError(f"Invalid relationship: {relationship_name}")
        
        if not values:
            return
            
        model_class, field_name = relationship_mapping[relationship_name]
        current_items = getattr(book, relationship_name)
        items_to_keep = []
        
        values_set = set(values)
        
        for item in current_items:
            if getattr(item, field_name) not in values_set:
                items_to_keep.append(item)
        
        setattr(book, relationship_name, items_to_keep)

    def _update_book_custom_columns(self, book: Book, custom_columns: Dict[str, Any]) -> None:
        """Update custom column values for a book.
        
        Args:
            book: The book to update
            custom_columns: Dictionary of custom column values to update
            
        Raises:
            ValueError: If a custom column doesn't exist
        """
        for column_label, value in custom_columns.items():
            custom_column = self._get_custom_column_by_label(column_label)
            if not custom_column:
                raise ValueError(f"Custom column with label '{column_label}' not found")
            
            # Create table objects for the custom column
            metadata = MetaData()
            value_table_name = f"custom_column_{custom_column.id}"
            value_table = Table(value_table_name, metadata, autoload_with=self._engine)
            
            # Handle multi-value columns
            if custom_column.is_multiple or custom_column.datatype in {"text", "rating"}:
                self._update_multi_value_custom_column(book, custom_column, value_table, value)
            else:
                self._update_single_value_custom_column(book, custom_column, value_table, value)

    def _update_multi_value_custom_column(self, book: Book, custom_column: CustomColumn, value_table: Table, value: Any) -> None:
        """Update a multi-value custom column for a book.
        
        Args:
            book: The book to update
            custom_column: The custom column to update
            value_table: The SQLAlchemy table for the custom column values
            value: The new value(s) for the column
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
        
        # Create link table
        metadata = MetaData()
        link_table_name = f"books_custom_column_{custom_column.id}_link"
        link_table = Table(link_table_name, metadata, autoload_with=self._engine)
        
        # Remove existing links
        self._session.execute(
            link_table.delete().where(link_table.c.book == book.id)
        )
        
        # Normalize the value to a list
        values_list = value if isinstance(value, list) else [value]
        
        # Add the new values
        for val in values_list:
            if val is None or val == "":
                continue
                
            # Check if the value already exists in the value table
            existing_value = self._session.execute(
                select(value_table.c.id).where(value_table.c.value == val)
            ).scalar()
            
            # If it doesn't exist, create it
            if existing_value is None:
                result = self._session.execute(
                    value_table.insert().values(value=val).returning(value_table.c.id)
                )
                value_id = result.scalar()
            else:
                value_id = existing_value
            
            # Create the link
            self._session.execute(
                link_table.insert().values(book=book.id, value=value_id)
            )

    def _update_single_value_custom_column(self, book: Book, custom_column: CustomColumn, value_table: Table, value: Any) -> None:
        """Update a single-value custom column for a book.
        
        Args:
            book: The book to update
            custom_column: The custom column to update
            value_table: The SQLAlchemy table for the custom column values
            value: The new value for the column
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
        
        # Special handling for datetime values
        if custom_column.datatype == "datetime" and isinstance(value, str):
            value = parse_calibre_datetime(value)
        
        # Check if a value already exists
        existing_value = self._session.execute(
            select(value_table.c.id).where(value_table.c.book == book.id)
        ).scalar()
        
        # If it exists, update it
        if existing_value is not None:
            self._session.execute(
                value_table.update()
                .where(value_table.c.book == book.id)
                .values(value=value)
            )
        else:
            # Insert a new value
            self._session.execute(
                value_table.insert().values(book=book.id, value=value)
            )

    def _add_multi_value_custom_column_items(self, book: Book, column_label: str, values: Union[List[Any], Any]) -> None:
        """Add values to a multi-value custom column.
        
        Args:
            book: The book to update
            column_label: The label of the custom column
            values: The values to add
            
        Raises:
            ValueError: If the custom column doesn't exist or isn't a multi-value column
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
            return
        
        # Convert to list if it's not already
        values_to_add = values if isinstance(values, list) else [values]
        if not values_to_add:
            return
            
        # Get the custom column
        custom_column = self._get_custom_column_by_label(column_label)
        if not custom_column:
            raise ValueError(f"Custom column '{column_label}' not found")
            
        # Check if it's a multi-value column
        if not custom_column.is_multiple and custom_column.datatype not in {"text", "rating"}:
            raise ValueError(f"Custom column '{column_label}' is not a multi-value column")
        
        # Create table objects for the custom column
        metadata = MetaData()
        value_table_name = f"custom_column_{custom_column.id}"
        value_table = Table(value_table_name, metadata, autoload_with=self._engine)
        
        # Create link table
        link_table_name = f"books_custom_column_{custom_column.id}_link"
        link_table = Table(link_table_name, metadata, autoload_with=self._engine)
        
        # Get current values
        current_values = self.get_custom_column_value(book, column_label)
        current_values_set = set(current_values)
        
        # Add new values
        for val in values_to_add:
            if val in current_values_set:
                # Skip if the value already exists
                continue
                
            # Check if the value exists in the value table
            existing_value = self._session.execute(
                select(value_table.c.id).where(value_table.c.value == val)
            ).scalar()
            
            # If it doesn't exist, create it
            if existing_value is None:
                result = self._session.execute(
                    value_table.insert().values(value=val).returning(value_table.c.id)
                )
                value_id = result.scalar()
            else:
                value_id = existing_value
            
            # Create the link
            self._session.execute(
                link_table.insert().values(book=book.id, value=value_id)
            )

    def _remove_multi_value_custom_column_items(self, book: Book, column_label: str, values: Union[List[Any], Any]) -> None:
        """Remove values from a multi-value custom column.
        
        Args:
            book: The book to update
            column_label: The label of the custom column
            values: The values to remove
            
        Raises:
            ValueError: If the custom column doesn't exist or isn't a multi-value column
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
            return

        # Convert to list if it's not already
        values_to_remove = values if isinstance(values, list) else [values]
        if not values_to_remove:
            return
            
        # Get the custom column
        custom_column = self._get_custom_column_by_label(column_label)
        if not custom_column:
            raise ValueError(f"Custom column '{column_label}' not found")
            
        # Check if it's a multi-value column
        if not custom_column.is_multiple and custom_column.datatype not in {"text", "rating"}:
            raise ValueError(f"Custom column '{column_label}' is not a multi-value column")
        
        # Create table objects for the custom column
        metadata = MetaData()
        value_table_name = f"custom_column_{custom_column.id}"
        value_table = Table(value_table_name, metadata, autoload_with=self._engine)
        
        # Create link table
        link_table_name = f"books_custom_column_{custom_column.id}_link"
        link_table = Table(link_table_name, metadata, autoload_with=self._engine)
        
        # Convert to list if it's not already
        values_to_remove = values if isinstance(values, list) else [values]
        values_set = set(values_to_remove)
        
        # For each value to remove, find the value_id and remove the link
        for val in values_to_remove:
            # Find the value ID
            value_id = self._session.execute(
                select(value_table.c.id).where(value_table.c.value == val)
            ).scalar()
            
            if value_id is not None:
                # Remove the link
                self._session.execute(
                    link_table.delete().where(
                        link_table.c.book == book.id,
                        link_table.c.value == value_id
                    )
                )

    def _add_book_identifiers(self, book: Book, identifiers: List[str]) -> None:
        """Add identifiers to a book.
        
        Args:
            book: The book to update
            identifiers: A list of strings in format "type:value" or just a value (which will be
                        treated as an ISBN)
        
        Raises:
            RuntimeError: If the library is not open
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
        
        # If no identifiers to add, return early
        if not identifiers:
            return
        
        # Process each identifier
        for id_str in identifiers:
            # If there's a colon, split it into type:value
            if ":" in id_str:
                id_type, id_value = id_str.split(":", 1)
            else:
                # If there's no colon, assume it's an ISBN
                id_type, id_value = "isbn", id_str
            
            # Check if this identifier already exists
            existing_identifier = next(
                (i for i in book.identifiers if 
                i.identifier_type == id_type and i.val == id_value),
                None
            )
            
            # If it doesn't exist, create it
            if not existing_identifier:
                # Check if the type exists but with a different value
                type_exists = next(
                    (i for i in book.identifiers if i.identifier_type == id_type),
                    None
                )
                
                # If the type exists, update the value
                if type_exists:
                    type_exists.val = id_value
                # Otherwise, create a new identifier
                else:
                    new_identifier = Identifier(identifier_type=id_type, val=id_value, book=book)
                    self._session.add(new_identifier)
                    book.identifiers.append(new_identifier)

    def _remove_book_identifiers(self, book: Book, identifiers: List[str]) -> None:
        """Remove identifiers from a book.
        
        Args:
            book: The book to update
            identifiers: A list of strings in format "type:value" or just "type" to remove
                        all identifiers of that type
        
        Raises:
            RuntimeError: If the library is not open
        """
        if self._session is None:
            raise RuntimeError("Library must be opened using a context manager before updating books")
        
        # If no identifiers to remove, return early
        if not identifiers:
            return
        
        identifiers_to_keep = []
        identifiers_to_remove = []
        
        for identifier in book.identifiers:
            should_keep = True
            
            for id_to_remove in identifiers:
                # Case 1: Format is "type" (remove all of that type)
                if ":" not in id_to_remove and identifier.identifier_type == id_to_remove:
                    should_keep = False
                    break
                # Case 2: Format is "type:value" (remove specific identifier)
                elif ":" in id_to_remove:
                    remove_type, remove_value = id_to_remove.split(":", 1)
                    if identifier.identifier_type == remove_type and identifier.val == remove_value:
                        should_keep = False
                        break
            
            if should_keep:
                identifiers_to_keep.append(identifier)
            else:
                identifiers_to_remove.append(identifier)
        
        for id_to_remove in identifiers_to_remove:
            self._session.delete(id_to_remove)
            
        book.identifiers = identifiers_to_keep

    def get_book_formats(self, book: 'Book') -> List[Format]:
        """Get a list of all formats for a book.
        
        Args:
            book: The book to get formats for
            
        Returns:
            List[Format]: A list of Format objects
            
        Raises:
            RuntimeError: If the library is not open
        """
        if not self._session:
            raise RuntimeError("Library must be opened using a context manager before getting formats")
        
        # Ensure the book has a library reference
        self._ensure_book_library_ref(book)
        
        # Get the formats
        formats = book.get_formats()
        
        # Ensure each format has a library reference
        for fmt in formats:
            fmt.set_library_reference(self)
        
        return formats

    def get_format(self, book: 'Book', format_type: str) -> Optional[Format]:
        """Get a specific format for a book.
        
        Args:
            book: The book to get the format for
            format_type: The format type (e.g., "EPUB", "PDF", etc.)
            
        Returns:
            Optional[Format]: The Format object, or None if it doesn't exist
            
        Raises:
            RuntimeError: If the library is not open
        """
        if not self._session:
            raise RuntimeError("Library must be opened using a context manager before getting formats")
        
        # Ensure the book has a library reference
        self._ensure_book_library_ref(book)
        
        # Get all formats and find the one we want
        formats = self.get_book_formats(book)
        format_type = format_type.upper()
        
        for fmt in formats:
            if fmt.format == format_type:
                return fmt
        
        return None

    def _ensure_book_library_ref(self, book: 'Book') -> None:
        """Ensure that a book has a reference to this library.
        
        This method sets the _library_ref attribute on a book if it doesn't already exist.
        
        Args:
            book: The book to set the library reference on
        """
        if not hasattr(book, '_library_ref') or book._library_ref is None or book._library_ref() is None:
            book.set_library_reference(self)

    def search(self, query: str, limit: Optional[int] = None, offset: Optional[int] = None) -> list[Book]:
        """
        Search for books that match the query across multiple attributes.
        
        Supports Calibre's query string format with boolean operators (AND, OR, NOT),
        field-specific searches, quoted strings, and relational operators.
        
        Searches through book title, author names, identifiers, series, publisher, tags, 
        and comments to find matching books.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return
            offset: Number of results to skip (for pagination)
            
        Returns:
            list[Book]: List of Book objects that match the search query
            
        Raises:
            RuntimeError: If the library is not open
        """
        if not self._session:
            raise RuntimeError("Library must be opened before searching")
            
        # Handle simple search case (for backward compatibility)
        if ":" not in query and all(op not in query.lower() for op in (" and ", " or ", " not ")):
            return self._simple_search(query, limit, offset)
        
        # Parse the query into a search expression tree and convert to SQLAlchemy conditions
        parsed_condition = self._parse_query(query)
        
        # Start a base query
        book_query = self._session.query(Book).distinct()
        
        # Apply the parsed condition
        if parsed_condition is not None:
            book_query = book_query.filter(parsed_condition)
        
        # Apply pagination
        if offset is not None:
            book_query = book_query.offset(offset)
        if limit is not None:
            book_query = book_query.limit(limit)
        
        # Execute the query and return the results
        return book_query.all()

    def _simple_search(self, query: str, limit: Optional[int] = None, offset: Optional[int] = None) -> list[Book]:
        """
        Perform a simple search across all searchable fields.
        
        Splits the query by whitespace and searches for the intersection of all terms
        across all searchable fields.
        
        Args:
            query: The search query string
            limit: Maximum number of results to return
            offset: Number of results to skip (for pagination)
            
        Returns:
            list[Book]: List of Book objects that match the search query
        """
        if self._session is None:
            raise RuntimeError("Library must be opened before searching")
        
        # Split the query into terms by whitespace
        search_terms = [term.strip() for term in query.split() if term.strip()]
        
        if not search_terms:
            # Return empty list if no valid search terms
            return []
        
        # Start a base query
        book_query = self._session.query(Book).distinct()
        
        # For each search term, add an AND condition that checks across all fields
        for term in search_terms:
            # Add % wildcards for SQL LIKE expressions
            like_pattern = f"%{term}%"
            
            # Build conditions for all searchable fields using OR for this term
            term_conditions = [
                # Direct book attributes
                Book.title.ilike(like_pattern),
                
                # Related entities with text fields
                Book.authors.any(Author.name.ilike(like_pattern)),
                Book.tags.any(Tag.name.ilike(like_pattern)),
                Book.series.any(Series.name.ilike(like_pattern)),
                Book.publishers.any(Publisher.name.ilike(like_pattern)),
                Book.comments.any(Comment.text.ilike(like_pattern)),
                
                # Identifiers (match in value)
                Book.identifiers.any(Identifier.val.ilike(like_pattern))
            ]
            
            # Apply the OR conditions for this term as an AND condition to the query
            # This ensures each term must match at least one field
            book_query = book_query.filter(or_(*term_conditions))
        
        # Apply pagination
        if offset is not None:
            book_query = book_query.offset(offset)
        if limit is not None:
            book_query = book_query.limit(limit)
        
        # Execute the query and return the results
        return book_query.all()

    def _parse_query(self, query_string: str) -> Optional[ColumnElement[bool]]:
        """
        Parse a Calibre query string into SQLAlchemy conditions.
        
        Args:
            query_string: The Calibre-format query string
            
        Returns:
            Optional[ColumnElement[bool]]: SQLAlchemy filter condition
            
        Raises:
            ValueError: If the query string cannot be parsed
        """
        from sqlalchemy import and_, or_, not_
        import re
        
        # Tokenize the query string
        def tokenize(s: str) -> list[str]:
            """Tokenize the query string, preserving quoted sections."""
            # Handle super-quotes first
            super_quotes_pattern = r'"""(.*?)"""'
            super_quoted_sections = re.findall(super_quotes_pattern, s)
            # Replace super-quoted sections with placeholders
            for i, section in enumerate(super_quoted_sections):
                s = s.replace(f'"""{section}"""', f"__SUPERQUOTE_{i}__")
            
            # Handle regular quotes
            quotes_pattern = r'"((?:\\"|[^"])*)"'
            quoted_sections = re.findall(quotes_pattern, s)
            # Replace quoted sections with placeholders
            for i, section in enumerate(quoted_sections):
                s = s.replace(f'"{section}"', f"__QUOTE_{i}__")
            
            # Replace parentheses with space-padded versions to tokenize them
            s = s.replace("(", " ( ").replace(")", " ) ")
            
            # Tokenize the string
            tokens = []
            for token in s.split():
                # Handle column:value format
                if ":" in token and not token.startswith("__QUOTE_") and not token.startswith("__SUPERQUOTE_"):
                    field, value = token.split(":", 1)
                    tokens.append(field)
                    tokens.append(":")
                    tokens.append(value)
                else:
                    tokens.append(token)
            
            # Restore quoted sections
            for i, section in enumerate(quoted_sections):
                # Unescape any escaped quotes
                section = section.replace('\\"', '"').replace('\\\\', '\\')
                for j, token in enumerate(tokens):
                    if token == f"__QUOTE_{i}__":
                        tokens[j] = section
            
            # Restore super-quoted sections
            for i, section in enumerate(super_quoted_sections):
                for j, token in enumerate(tokens):
                    if token == f"__SUPERQUOTE_{i}__":
                        tokens[j] = section
            
            return tokens
        
        tokens = tokenize(query_string)
        
        # Parse the tokens into an expression tree
        def parse_expression(tokens: list[str], pos: int = 0) -> tuple[Any, int]:
            """Parse the tokens into an expression tree."""
            if pos >= len(tokens):
                return None, pos
            
            # Parse a single term or subexpression
            def parse_term() -> tuple[Any, int]:
                nonlocal pos
                if pos >= len(tokens):
                    return None, pos
                
                token = tokens[pos]
                pos += 1
                
                # Handle NOT operator
                if token.lower() == "not":
                    expr, pos = parse_term()
                    return {"op": "NOT", "expr": expr}, pos
                
                # Handle parentheses
                if token == "(":
                    expr, pos = parse_expression(tokens, pos)
                    if pos < len(tokens) and tokens[pos] == ")":
                        pos += 1
                    else:
                        raise ValueError(f"Missing closing parenthesis in query: {query_string}")
                    return expr, pos
                
                # Handle field:value
                if pos < len(tokens) and tokens[pos] == ":":
                    field = token
                    pos += 1  # Skip the colon
                    if pos < len(tokens):
                        value = tokens[pos]
                        pos += 1
                        # Handle relational operators
                        if value.startswith(("=", ">", "<", "!", "~")):
                            op = value[0]
                            if op in ("=", ">", "<") and len(value) > 1 and value[1] == "=":
                                op = op + "="
                                value = value[2:]
                            elif op == "!" and len(value) > 1 and value[1] == "=":
                                op = "!="
                                value = value[2:]
                            elif op == "~":
                                op = "LIKE"
                                value = value[1:]
                            else:
                                value = value[1:]
                        else:
                            op = "CONTAINS"
                        
                        return {"field": field, "op": op, "value": value}, pos
                
                # Simple term (no field specified)
                return {"field": None, "op": "CONTAINS", "value": token}, pos
            
            left, pos = parse_term()
            
            while pos < len(tokens):
                # Check for operators
                if tokens[pos].lower() in ("and", "or"):
                    op = tokens[pos].upper()
                    pos += 1
                    right, pos = parse_term()
                    left = {"op": op, "left": left, "right": right}
                elif tokens[pos] == ")":
                    # End of a grouped expression
                    break
                else:
                    # Implicit AND
                    right, pos = parse_term()
                    left = {"op": "AND", "left": left, "right": right}
            
            return left, pos
        
        # Parse the expression
        try:
            expr, _ = parse_expression(tokens)
        except ValueError as e:
            raise ValueError(f"Error parsing query: {e}")
        
        # Convert the expression tree to SQLAlchemy conditions
        def build_condition(expr: dict) -> Optional[ColumnElement[bool]]:
            """Convert an expression node to a SQLAlchemy condition."""
            if expr is None:
                return None
            
            if expr["op"] == "AND":
                left_cond = build_condition(expr["left"])
                right_cond = build_condition(expr["right"])
                if left_cond is None:
                    return right_cond
                if right_cond is None:
                    return left_cond
                return and_(left_cond, right_cond)
            
            elif expr["op"] == "OR":
                left_cond = build_condition(expr["left"])
                right_cond = build_condition(expr["right"])
                if left_cond is None:
                    return right_cond
                if right_cond is None:
                    return left_cond
                return or_(left_cond, right_cond)
            
            elif expr["op"] == "NOT":
                cond = build_condition(expr["expr"])
                if cond is None:
                    return None
                return not_(cond)
            
            else:
                # Field-specific search
                field = expr["field"]
                op = expr["op"]
                value = expr["value"]
                
                # Remove leading = from value if present (used to indicate exact match)
                if value.startswith("="):
                    value = value[1:]
                    op = "EQUALS"
                
                # Handle field-specific searches
                if field is None:
                    # Search across all fields
                    like_pattern = f"%{value}%"
                    conditions = [
                        Book.title.ilike(like_pattern),
                        Book.authors.any(Author.name.ilike(like_pattern)),
                        Book.tags.any(Tag.name.ilike(like_pattern)),
                        Book.series.any(Series.name.ilike(like_pattern)),
                        Book.publishers.any(Publisher.name.ilike(like_pattern)),
                        Book.comments.any(Comment.text.ilike(like_pattern)),
                        Book.identifiers.any(Identifier.val.ilike(like_pattern))
                    ]
                    return or_(*conditions)
                
                # Map field names to appropriate SQLAlchemy models and columns
                field_mapping: dict[str, tuple[Any, Optional[Any]]] = {
                    "title": (Book.title, None),
                    "author": (Author.name, Book.authors),
                    "tag": (Tag.name, Book.tags),
                    "series": (Series.name, Book.series),
                    "publisher": (Publisher.name, Book.publishers),
                    "comments": (Comment.text, Book.comments),
                    "identifier": (Identifier.val, Book.identifiers),
                    "format": (Format.format, Book.formats),
                    "rating": (Rating.rating, Book.ratings),
                    # Add mappings for date fields
                    "date": (Book.timestamp, None),
                    "pubdate": (Book.pubdate, None),
                    "last_modified": (Book.last_modified, None),
                    # Add more mappings as needed
                }
                
                # Handle custom columns
                if field.startswith("#"):
                    # Look up the custom column by label
                    custom_column = self._get_custom_column_by_label(field[1:])
                    if custom_column:
                        return self._build_custom_column_condition(custom_column, op, value)
                
                if field in field_mapping:
                    column, relationship = field_mapping[field]
                    
                    # Handle relational operators
                    if field in {"date", "pubdate", "last_modified"}:
                        if op == "<" or op == "LESS_THAN" or op == ">=" or op == "GREATER_EQUAL":
                            converted_value = parse_calibre_datetime(value, complete_lower=True)

                        elif op == ">" or op == "GREATER_THAN" or op == "<=" or op == "LESS_EQUAL":
                            converted_value = parse_calibre_datetime(value, complete_lower=False)

                        else:
                            converted_value = parse_calibre_datetime(value)
                    else:
                        converted_value = value
                    sql_condition = self._build_field_condition(column, op, converted_value)
                    
                    # If it's a relationship, apply the condition through the relationship
                    if relationship is not None:
                        return relationship.any(sql_condition)
                    else:
                        return sql_condition
                
                # Fallback to basic search if field not recognized
                like_pattern = f"%{value}%"
                return Book.title.ilike(like_pattern)
        
        return build_condition(expr)

    def _build_field_condition(self, column: Column, op: str, value: str | int | float | datetime) -> ColumnElement[bool]:
        """
        Build a SQLAlchemy condition for a field based on the operator.
        
        Args:
            column: The SQLAlchemy column to query
            op: The operator to apply
            value: The value to compare against
            
        Returns:
            ColumnElement[bool]: SQLAlchemy filter condition
        """
        # Convert operator to SQLAlchemy filter expression
        if op == "=" or op == "EQUALS":
            return column == value
        elif op == "!=" or op == "NOT_EQUALS":
            return column != value
        elif op == ">" or op == "GREATER_THAN":
            return column > value
        elif op == ">=" or op == "GREATER_EQUAL":
            return column >= value
        elif op == "<" or op == "LESS_THAN":
            return column < value
        elif op == "<=" or op == "LESS_EQUAL":
            return column <= value
        elif op == "LIKE":
            return column.like(f"%{value}%")
        elif op == "CONTAINS":
            # For string fields, use ilike for case-insensitive containment
            if hasattr(column, 'ilike'):
                return column.ilike(f"%{value}%")
            # For other fields, try to convert value to the column's type
            return column == value
        else:
            # Default to exact match
            return column == value

    def _build_custom_column_condition(self, custom_column: CustomColumn, op: str, value: str) -> ColumnElement[bool]:
        """
        Build a condition for searching in a custom column.
        
        Args:
            custom_column: The custom column metadata
            op: The operator to apply
            value: The value to compare against
            
        Returns:
            ColumnElement[bool]: SQLAlchemy filter condition
        """
        # Create table objects for the custom column
        metadata = MetaData()
        value_table_name = f"custom_column_{custom_column.id}"
        value_table = Table(value_table_name, metadata, autoload_with=self._engine)

        converted_value : int | float | bool | str | datetime = value
        # Get the appropriate column from the value table
        if custom_column.datatype in {"text", "comments", "series", "enumeration"}:
            column = value_table.c.value
        elif custom_column.datatype in {"int", "float", "rating"}:
            column = value_table.c.value
            # Convert value to appropriate type
            if custom_column.datatype == "int":
                try:
                    converted_value = int(value)
                except ValueError:
                    return false()  # Return a false condition if conversion fails
            elif custom_column.datatype in {"float", "rating"}:
                try:
                    converted_value = float(value)
                except ValueError:
                    return false()  # Return a false condition if conversion fails
        elif custom_column.datatype == "bool":
            column = value_table.c.value
            # Convert string value to boolean
            if value.lower() in {"true", "yes", "1"}:
                converted_value = True
            elif value.lower() in {"false", "no", "0"}:
                converted_value = False
            else:
                return false()  # Return a false condition if conversion fails
        elif custom_column.datatype == "datetime":
            column = value_table.c.value
            # Handle date comparison
            try:
                # Parse date value - support various formats
                converted_value = parse_calibre_datetime(value)
            except ValueError:
                return false()  # Return a false condition if conversion fails
        else:
            # Default to value column
            column = value_table.c.value
        
        # Build the condition based on operator
        condition = self._build_field_condition(column, op, converted_value)
        
        # For multi-value columns, we need to join through the link table
        if custom_column.is_multiple or custom_column.datatype in {"text", "rating"}:
            link_table_name = f"books_custom_column_{custom_column.id}_link"
            link_table = Table(link_table_name, metadata, autoload_with=self._engine)
            
            # Define a subquery
            subq = select(link_table.c.book).where(
                and_(
                    link_table.c.value == value_table.c.id,
                    condition
                )
            ).correlate_except(link_table, value_table)
            
            # Return condition that checks if book.id is in the subquery results
            return Book.id.in_(subq)
        
        # For single-value columns
        return Book.id.in_(
            select(value_table.c.book).where(condition)
        )
