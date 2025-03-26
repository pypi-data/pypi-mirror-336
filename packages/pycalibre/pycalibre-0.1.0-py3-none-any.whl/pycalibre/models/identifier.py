"""Identifier model for book identifiers in Calibre libraries."""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import SerializableMixin

if TYPE_CHECKING:
    from .book import Book


class Identifier(Base, SerializableMixin):
    """An identifier in a Calibre library.

    Represents an identifier as stored in the identifiers table.
    Examples include ISBN, ASIN, DOI, etc.
    """
    __tablename__ = 'identifiers'
    
    id = Column(Integer, primary_key=True)
    val = Column(String, nullable=False)
    identifier_type = Column(String, name='type', nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), name='book', nullable=False)
    
    # Relationship to Book
    book = relationship('Book', back_populates='identifiers')
    
    def __repr__(self) -> str:
        """Return a string representation of the identifier.
        
        Returns:
            str: String representation including ID, type, and val.
        """
        return f"Identifier(id={self.id}, identifier_type={self.identifier_type}, val={self.val})"
    
    @property
    def formatted(self) -> str:
        """Get the identifier in the format 'type:value'.
        
        Returns:
            str: The formatted identifier string
        """
        return f"{self.identifier_type}:{self.val}"
