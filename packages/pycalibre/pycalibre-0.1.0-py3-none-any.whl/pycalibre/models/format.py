"""Format model for ebook formats in the Calibre library."""

from __future__ import annotations
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import LibraryReferenceMixin, SerializableMixin, FilePathMixin

if TYPE_CHECKING:
    from .book import Book


class Format(Base, LibraryReferenceMixin, SerializableMixin, FilePathMixin):
    """Represents a book format in the Calibre library.
    
    This model maps to the 'data' table in the Calibre database.
    Each format corresponds to a file (EPUB, MOBI, PDF, etc.) for a book.
    """
    __tablename__ = 'data'
    
    id = Column(Integer, primary_key=True)
    book = Column(Integer, ForeignKey('books.id'), nullable=False)
    format = Column(String, nullable=False)
    name = Column(String, nullable=False)
    uncompressed_size = Column(Integer, nullable=False)
    
    # Define the relationship to Book
    book_ref = relationship("Book", back_populates="formats")
    
    def __repr__(self) -> str:
        """Return a string representation of the format.
        
        Returns:
            str: String representation including ID, format type, name, and size.
        """
        return f"Format(id={self.id}, format='{self.format}', name='{self.name}', uncompressed_size={self.uncompressed_size})"
    
    @property
    def file_path(self) -> Optional[Path]:
        """Get the path to the actual format file.
        
        Returns:
            Optional[Path]: The path to the format file, or None if 
                          library reference is not available.
        """
        # Get the book reference from the relationship
        if not hasattr(self, 'book_ref') or self.book_ref is None:
            return None
        
        # Return the path to the format file
        return self.book_ref.file_path / f"{self.name}.{self.format.lower()}"
