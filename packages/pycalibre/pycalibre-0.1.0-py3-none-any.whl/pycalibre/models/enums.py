"""Enumeration types used throughout the pycalibre library."""

from enum import Enum


class FilterOperator(Enum):
    """Enumeration of available filter operators for book queries.
    
    These operators define how values are compared when filtering books.
    They're used in the Library.query_books method to specify comparison types.
    
    Attributes:
        EQUALS: Exact equality matching (==)
        NOT_EQUALS: Negated equality matching (!=)
        CONTAINS: String/list contains matching (like SQL LIKE or array inclusion)
        NOT_CONTAINS: Negated contains matching
        GREATER_THAN: Greater than comparison (>)
        LESS_THAN: Less than comparison (<)
        GREATER_EQUAL: Greater than or equal comparison (>=)
        LESS_EQUAL: Less than or equal comparison (<=)
        IN: Check if value is in a set of values
        NOT_IN: Check if value is not in a set of values
    """
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_EQUAL = "greater_equal"
    LESS_EQUAL = "less_equal"
    IN = "in"
    NOT_IN = "not_in"
