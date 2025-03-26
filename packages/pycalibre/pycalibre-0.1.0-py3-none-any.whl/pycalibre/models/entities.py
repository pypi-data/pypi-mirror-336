"""Entity models for Calibre library objects like authors, tags, etc."""

from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import DisplayNameMixin, SerializableMixin

if TYPE_CHECKING:
    from .book import Book

class Author(Base, DisplayNameMixin, SerializableMixin):
    """An author in a Calibre library.
    
    Represents an author as stored in the authors table.
    """
    
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sort = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    
    # Back-populated from Book
    books = relationship('Book', secondary='books_authors_link', back_populates='authors')
    
    def __repr__(self) -> str:
        """Return a string representation of the author.
        
        Returns:
            str: String representation including ID and name.
        """
        return f"Author(id={self.id}, name={self.name})"


class Tag(Base, DisplayNameMixin, SerializableMixin):
    """A tag in a Calibre library.

    Represents a tag as stored in the tags table.
    """
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    
    # Back-populated from Book
    books = relationship('Book', secondary='books_tags_link', back_populates='tags')
    
    def __repr__(self) -> str:
        """Return a string representation of the tag.
        
        Returns:
            str: String representation including ID and name.
        """
        return f"Tag(id={self.id}, name={self.name})"


class Language(Base, DisplayNameMixin, SerializableMixin):
    """A language in a Calibre library.

    Represents a language as stored in the languages table.
    """
    __tablename__ = 'languages'
    
    id = Column(Integer, primary_key=True)
    lang_code = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    
    # Back-populated from Book
    books = relationship('Book', secondary='books_languages_link', back_populates='languages')
    
    def __repr__(self) -> str:
        """Return a string representation of the language.
        
        Returns:
            str: String representation including ID and language code.
        """
        return f"Language(id={self.id}, lang_code={self.lang_code})"

    def get_display_name(self) -> str:
        """Override to use lang_code for display instead of name.
        
        Returns:
            str: The language code for display
        """
        return str(self.lang_code)


class Publisher(Base, DisplayNameMixin, SerializableMixin):
    """A publisher in a Calibre library.

    Represents a publisher as stored in the publishers table.
    """
    __tablename__ = 'publishers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sort = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    
    # Back-populated from Book
    books = relationship('Book', secondary='books_publishers_link', back_populates='publishers')
    
    def __repr__(self) -> str:
        """Return a string representation of the publisher.
        
        Returns:
            str: String representation including ID and name.
        """
        return f"Publisher(id={self.id}, name={self.name})"


class Series(Base, DisplayNameMixin, SerializableMixin):
    """A series in a Calibre library.

    Represents a series as stored in the series table.
    """
    __tablename__ = 'series'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    sort = Column(String, nullable=False)
    link = Column(String, nullable=False, default='')
    
    # Back-populated from Book
    books = relationship('Book', secondary='books_series_link', back_populates='series')
    
    def __repr__(self) -> str:
        """Return a string representation of the series.
        
        Returns:
            str: String representation including ID and name.
        """
        return f"Series(id={self.id}, name={self.name})"


class Rating(Base, SerializableMixin):
    """A rating in a Calibre library.

    Represents a rating as stored in the ratings table.
    """
    __tablename__ = 'ratings'
    
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    
    # Back-populated from Book
    books = relationship('Book', secondary='books_ratings_link', back_populates='ratings')
    
    def __repr__(self) -> str:
        """Return a string representation of the rating.
        
        Returns:
            str: String representation including ID and rating value.
        """
        return f"Rating(id={self.id}, rating={self.rating})"
