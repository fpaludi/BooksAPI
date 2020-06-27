from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date,
    ForeignKey, Text, Boolean
)
from sqlalchemy.orm import mapper, relationship
from ..models.books import Books
from ..models.users import Users
from ..models.reviews import Reviews

metadata = MetaData()


books = Table(
    'books', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("isbn", String, nullable=False),
    Column("title", String, nullable=False),
    Column("author", String, nullable=False),
    Column("year", Integer, nullable=False),
)


users = Table(
    'users', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String, nullable=False, unique=True),
    Column("password_hash", String, nullable=False),
    Column("confirmed", Boolean, default=False),
)


reviews = Table(
    'reviews', metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("review_value", Integer, nullable=False),
    Column("review_comment", Text),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("book_id", Integer, ForeignKey("books.id"), nullable=False),
)


def start_mappers():
    users_mapper = mapper(Users, users)
    reviews_mapper = mapper(Reviews, reviews)
    books_mapper = mapper(Books, books, properties={
        'reviews': relationship(
            reviews_mapper,
            backref="books",
            collection_class=list,
        )
    })



