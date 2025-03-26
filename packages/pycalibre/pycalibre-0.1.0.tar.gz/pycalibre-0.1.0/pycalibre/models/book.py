"""Book model and related functionality."""

from __future__ import annotations
from datetime import datetime
import dateparser
from pathlib import Path
import weakref
from typing import Any, Dict, List, Optional, Tuple, Union, TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from .base import Base
from .mixins import LibraryReferenceMixin, SerializableMixin
from .associations import (
    book_author_association, 
    book_tag_association, 
    book_language_association,
    book_publisher_association, 
    book_series_association,
    book_rating_association
)

if TYPE_CHECKING:
    from .entities import Author, Tag, Language, Publisher, Series
    from .custom import CustomColumn
    from .format import Format
    from .comment import Comment


def parse_calibre_datetime(date_string: str, complete_lower: bool = True) -> datetime:
    """Parse a Calibre datetime string into a Python datetime object.
    
    Args:
        date_string: String representation of a datetime from Calibre
        
    Returns:
        datetime: Parsed datetime object
        
    Raises:
        ValueError: If the date string cannot be parsed
    """
    # Calibre typically uses ISO format strings
    if isinstance(date_string, datetime):
        return date_string  # Already a datetime object, return as is
    try:
        if complete_lower:
            parsed_date = dateparser.parse(date_string, settings={
                'PREFER_DAY_OF_MONTH': 'first',
                'PREFER_MONTH_OF_YEAR': 'first',
            }) # type: ignore
        else:
            parsed_date = dateparser.parse(date_string, settings={
                'PREFER_DAY_OF_MONTH': 'last',
                'PREFER_MONTH_OF_YEAR': 'last',
            }) # type: ignore
        
        if parsed_date is None:
            raise ValueError(f"Could not parse date string: {date_string}")

        return parsed_date

    except ValueError:
        # Try some fallback parsing methods
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d'):
            try:
                return datetime.strptime(date_string, fmt)
            except ValueError:
                continue
        # If all parsing fails, raise an error
        raise ValueError(f"Could not parse date string: {date_string}")


class Book(Base, LibraryReferenceMixin, SerializableMixin):
    """Model representing a book in the Calibre library."""
    
    __tablename__ = 'books'
    
    # Basic attributes
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    sort = Column(String, nullable=False)
    timestamp = Column(DateTime, name='timestamp', nullable=False)
    pubdate = Column(DateTime, name='pubdate', nullable=False)
    series_index = Column(Integer, nullable=False)
    author_sort = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    lccn = Column(String, nullable=False)
    path = Column(String, nullable=False)
    flags = Column(Integer, nullable=False)
    uuid = Column(String, nullable=False)
    has_cover = Column(Boolean, nullable=False)
    last_modified = Column(DateTime, name='last_modified', nullable=False)
    
    # Relationships
    identifiers = relationship('Identifier', back_populates='book')
    authors = relationship('Author', secondary=book_author_association, back_populates='books')
    tags = relationship('Tag', secondary=book_tag_association, back_populates='books')
    languages = relationship('Language', secondary=book_language_association, back_populates='books')
    publishers = relationship('Publisher', secondary=book_publisher_association, back_populates='books')
    series = relationship('Series', secondary=book_series_association, back_populates='books')
    comments = relationship('Comment', back_populates='book_ref', order_by='Comment.id')
    ratings = relationship('Rating', secondary=book_rating_association, back_populates='books')
    formats = relationship('Format', back_populates='book_ref')
    
    def __repr__(self) -> str:
        """Return string representation of the book.
        
        Returns:
            str: String representation including ID and title.
        """
        return f"Book(id={self.id}, title={self.title})"
    
    def __getattr__(self, name: str) -> Any:
        """Allow access to custom columns as if they were properties.
        
        Args:
            name: The name of the attribute to get
            
        Returns:
            Any: The value of the custom column if it exists
            
        Raises:
            AttributeError: If the attribute doesn't exist as a custom column
        """
        if hasattr(self, '_library_ref') and self._library_ref is not None:
            try:
                library = self._library_ref()
                if library is not None:
                    return library.get_custom_column_value(self, name)
            except ValueError:
                pass
        
        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
    
    @property
    def cover_path(self) -> Optional[Path]:
        """Get the path to the book's cover image file.
        
        Returns:
            Optional[Path]: The path to the cover image file, or None if 
                           no cover exists or library reference is not available.
        """
        # If the book doesn't have a cover, return None
        if not self.has_cover:
            return None
        
        # Get the book's directory path
        book_dir = self.file_path
        if book_dir is None:
            return None
        
        # Define the priority order for cover file extensions
        cover_extensions = ['.jpeg', '.jpg', '.png', '.webp', '.tga', '.gif']
        
        # Check for each possible cover file in priority order
        for ext in cover_extensions:
            cover_path = book_dir / f"cover{ext}"
            if cover_path.exists():
                return cover_path
        
        # If no cover file was found with any of the extensions
        return None

    @property
    def file_path(self) -> Optional[Path]:
        """Get the path of the book's directory

        Returns:
            Optional[Path]: The path to the book's directory, or None if the library reference is not available.
        """
        # If the library reference is missing, return None
        if not hasattr(self, '_library_ref') or self._library_ref is None:
            return None
        
        # Retrieve the library instance from the weak reference
        library = self._library_ref() if self._library_ref() else None
        if not library:
            return None
        
        # Get the book's directory path
        return library.path / self.path
    
    def update(self, **kwargs) -> "Book":
        """Update book properties with a simple interface.
        
        Updates can include basic properties, relationship additions/removals, 
        and custom column values.
        
        Args:
            **kwargs: Arbitrary keyword arguments:
                - Basic properties: title, isbn, etc.
                - Adding to relationships: add_authors=["Author Name"], add_tags=["Tag Name"]
                - Removing from relationships: remove_authors=["Author Name"], remove_tags=["Tag Name"]
                - Custom columns: Any parameter name that matches a custom column label
                
        Returns:
            Book: The updated book
            
        Raises:
            RuntimeError: If the library reference is not available
            ValueError: If an invalid property is provided
        """
        self._check_library_reference("update")
        library = self.get_library()
        
        if library is None:
            # If the library isn't available, return the book unchanged
            return self

        return library.update_book_properties(self, **kwargs)
    
    def get_formats(self) -> List['Format']:
        """Get all formats for this book with proper library references.
        
        This method ensures that all Format objects have access to the 
        book and library references they need.
        
        Returns:
            List[Format]: A list of Format objects
            
        Raises:
            RuntimeError: If the book's library reference is not set
        """
        self._check_library_reference("get_formats")
        
        # Load formats if not already loaded
        if 'formats' not in self.__dict__ or self.__dict__['formats'] is None:
            # Use the SQLAlchemy relationship to load formats
            _ = self.formats
        
        return self.formats
