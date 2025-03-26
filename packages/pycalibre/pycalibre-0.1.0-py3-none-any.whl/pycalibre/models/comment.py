"""Comment model for book comments in Calibre libraries."""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import SerializableMixin

if TYPE_CHECKING:
    from .book import Book


class Comment(Base, SerializableMixin):
    """A comment associated with a book in a Calibre library.

    Represents a comment as stored in the comments table.
    """
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    book = Column(Integer, ForeignKey('books.id'), nullable=False)
    text = Column(Text, nullable=False)
    
    # Relationship to Book
    book_ref = relationship('Book', back_populates='comments')
    
    def __repr__(self) -> str:
        """Return a string representation of the comment.
        
        Returns:
            str: String representation including ID and truncated text.
        """
        preview = self.text[:27] + "..." if len(self.text) > 30 else self.text
        return f"Comment(id={self.id}, text={preview})"
