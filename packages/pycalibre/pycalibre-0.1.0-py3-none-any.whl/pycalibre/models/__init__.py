"""
Models module for pycalibre.

This package contains ORM models for interacting with a Calibre database.

Classes:
    Book: Represents a book in the Calibre library.
    Author: Represents an author of books.
    Publisher: Represents a publisher of books.
    Series: Represents a book series.
    Tag: Represents a tag that can be applied to books.
    Rating: Represents book ratings.
    Language: Represents the language of a book.
    CustomColumn: Represents a custom column in the Calibre database.
    Format: Represents a file format for a book.
    Comment: Represents book comments/descriptions.
    Identifier: Represents book identifiers (ISBN, ASIN, etc.).

Mixins:
    LibraryReferenceMixin: Mixin for models that reference a library.
    DisplayNameMixin: Mixin for models with a display name.
    SerializableMixin: Mixin for serializable models.
    FilePathMixin: Mixin for models with file paths.

Enums:
    FilterOperator: Operators for filtering books in queries.
"""

from .base import Base, BaseModel
from .book import Book, parse_calibre_datetime 
from .entities import Author, Publisher, Series, Tag, Rating, Language
from .custom import CustomColumn
from .format import Format
from .comment import Comment
from .identifier import Identifier
from .mixins import LibraryReferenceMixin, DisplayNameMixin, SerializableMixin, FilePathMixin
from .enums import FilterOperator
from .associations import (
    book_author_association,
    book_tag_association,
    book_language_association,
    book_publisher_association,
    book_series_association,
    book_rating_association
)

__all__ = [
    'Base', 'BaseModel',
    'Book', 'Author', 'Publisher', 'Series', 'Tag', 'Rating', 'Language', 
    'CustomColumn', 'Format', 'Comment', 'Identifier',
    'LibraryReferenceMixin', 'DisplayNameMixin', 'SerializableMixin', 'FilePathMixin',
    'FilterOperator', 'parse_calibre_datetime', 
]
