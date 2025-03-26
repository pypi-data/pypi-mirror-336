"""Custom column model and related functionality for Calibre libraries."""

from __future__ import annotations
import json
from typing import Any, Dict, Optional, List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship

from .base import Base
from .mixins import SerializableMixin, DisplayNameMixin

if TYPE_CHECKING:
    from .book import Book


class CustomColumn(Base, SerializableMixin, DisplayNameMixin):
    """A custom column in a Calibre library.
    
    Represents the metadata of a custom column as stored in the custom_columns table.
    """
    
    __tablename__ = 'custom_columns'
    
    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    name = Column(String, nullable=False)
    datatype = Column(String, nullable=False)
    mark_for_delete = Column(Boolean, nullable=False, default=False)
    is_multiple = Column(Boolean, nullable=False, default=False)
    normalized = Column(Boolean, nullable=False, default=False)
    display = Column(Text, nullable=False)
    
    def __repr__(self) -> str:
        """Return a string representation of the custom column.
        
        Returns:
            str: String representation including ID, label, name and datatype.
        """
        return f"CustomColumn(id={self.id}, label={self.label}, name={self.name}, datatype={self.datatype})"
    
    def get_display_name(self) -> str:
        """Return the name for display purposes.
        
        Returns:
            str: The display name of the custom column.
        """
        return str(self.name)
    
    @property
    def display_dict(self) -> Dict[str, Any]:
        """Return the display configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: The parsed display configuration dictionary.
        """
        result: Dict[str, Any] = {}
        if isinstance(self.display, str):
            try:
                result = json.loads(self.display)
            except json.JSONDecodeError:
                result = {}

        return result
    
    @property
    def description(self) -> Optional[str]:
        """Return the description of the column.
        
        Returns:
            Optional[str]: The column description if available.
        """
        return self.display_dict.get('description')
    
    @property
    def is_category(self) -> bool:
        """Check if this custom column is a category type.
        
        Category columns are displayed in the tag browser sidebar.
        
        Returns:
            bool: True if the column is a category, False otherwise.
        """
        if self.datatype == 'composite':
            return bool(self.display_dict.get('make_category', False))
            
        return self.datatype in {
            'text', 'enumeration', 'rating', 
            'series', 'datetime', 'bool'
        }
    
    @property
    def is_editable(self) -> bool:
        """Check if this custom column is editable.
        
        Some column types (like composite) are calculated and not user-editable.
        
        Returns:
            bool: True if the column is editable, False otherwise.
        """
        return bool(self.datatype != 'composite')
    
    @property
    def column_type(self) -> str:
        """Get the actual database column type based on datatype.
        
        Returns:
            str: The database column type name
        """
        if self.datatype in {'text', 'comments', 'series', 'enumeration'}:
            return 'text'
        elif self.datatype == 'datetime':
            return 'datetime'
        elif self.datatype == 'int':
            return 'int'
        elif self.datatype == 'float':
            return 'real'
        elif self.datatype == 'bool':
            return 'bool'
        elif self.datatype == 'rating':
            return 'int'
        elif self.datatype == 'composite':
            return 'text'
        else:
            return 'text'  # Default to text for unknown types
    
    def get_value_table_name(self) -> str:
        """Get the name of the database table that holds values for this column.
        
        Returns:
            str: The database table name
        """
        return f"custom_column_{self.id}"
    
    def get_link_table_name(self) -> str:
        """Get the name of the database table that links books to values for this column.
        
        Only applicable for multiple-value columns.
        
        Returns:
            str: The database link table name
        """
        return f"books_custom_column_{self.id}_link"
