"""Base classes and utilities for SQLAlchemy models."""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base): # type: ignore
    """Base model with common functionality for all models."""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
