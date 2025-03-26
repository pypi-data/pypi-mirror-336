"""
SQLAlchemy association tables for the pycalibre database.
This module defines the many-to-many relationship tables between books and other entities
in the Calibre database schema. These tables are used to associate books with authors,
tags, languages, publishers, series, and ratings.
Tables:
    book_author_association: Links books to authors
    book_tag_association: Links books to tags
    book_language_association: Links books to languages with an order indicator
    book_publisher_association: Links books to publishers
    book_series_association: Links books to series
    book_rating_association: Links books to ratings
"""


from sqlalchemy import Column, ForeignKey, Integer, Table, text

from pycalibre.models.base import Base


book_author_association = Table(
    'books_authors_link',
    Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author', Integer, ForeignKey('authors.id'), primary_key=True)
)

book_tag_association = Table(
    'books_tags_link',
    Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('tag', Integer, ForeignKey('tags.id'), primary_key=True)
)

book_language_association = Table(
    'books_languages_link',
    Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('lang_code', Integer, ForeignKey('languages.id'), primary_key=True),
    Column('item_order', Integer, nullable=False, server_default=text('0'))
)

book_publisher_association = Table(
    'books_publishers_link',
    Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    
    Column('publisher', Integer, ForeignKey('publishers.id'), primary_key=True)
)

book_series_association = Table(
    'books_series_link',
    Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('series', Integer, ForeignKey('series.id'), primary_key=True)
)

book_rating_association = Table(
    'books_ratings_link',
    Base.metadata,
    Column('book', Integer, ForeignKey('books.id'), primary_key=True),
    Column('rating', Integer, ForeignKey('ratings.id'), primary_key=True)
)
