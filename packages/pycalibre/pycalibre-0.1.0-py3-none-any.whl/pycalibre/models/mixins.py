"""Mixins providing shared functionality for models."""

from __future__ import annotations
from pathlib import Path
import weakref
from typing import Any, Optional, TypeVar, Generic, runtime_checkable, Protocol

from pycalibre.models.base import Base

T = TypeVar('T')


class LibraryReferenceMixin:
    """Mixin providing library reference functionality."""
    
    _library_ref: Optional[weakref.ReferenceType]

    def set_library_reference(self, library: Any) -> None:
        """Set the library reference for this object."""
        self._library_ref = weakref.ref(library)
    
    def get_library(self) -> Optional['Library']: # type: ignore
        """Get the library object if the reference is valid."""
        return self._library_ref() if self._library_ref is not None else None
    
    def _check_library_reference(self, method_name: str) -> None:
        """Verify library reference is valid or raise an appropriate error."""
        if not self._library_ref:
            raise RuntimeError(f"Cannot execute {method_name}: missing library reference")
        
        if not self._library_ref():
            raise RuntimeError(f"Cannot execute {method_name}: library reference is no longer valid")

class SerializableMixin:
    """Provides serialization capabilities to models."""
    
    def to_dict(self) -> Optional[dict[str, Any]]:
        """Convert object to dictionary."""
        if not isinstance(self, Base):
            return None
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class DisplayNameMixin:
    """Provides consistent name display functions."""
    
    def get_display_name(self) -> str:
        """Return formatted display name."""
        return getattr(self, 'name', str(self))

class FilePathMixin:
    """Provides file path resolution functionality."""
    
    def resolve_path(self, filename: str) -> Optional[Path]:
        """Resolve a file path relative to this object."""
        if not hasattr(self, 'get_library') or not callable(self.get_library):
            return None
            
        library = self.get_library()
        if not library:
            return None

        return library.path / filename
