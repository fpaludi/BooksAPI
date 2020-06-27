import os
import requests
from flask import current_app as app
from flask_login import login_user
from .models.books import Books
from .models.users import Users
from .models.reviews import Reviews
# from . import db


def get_json_from_goodreads(isbn):
    GOODREAD_API_URL = app.config["GOODREAD_API_URL"]
    GOODREAD_API_KEY = app.config["GOODREAD_API_KEY"]
    res = requests.get(
        GOODREAD_API_URL, params={"key": GOODREAD_API_KEY, "isbns": isbn}
    )
    return res.json()


def login(username, password, repo):
    user = repo.get_username(username)
    #Users.query.filter_by(username=username).first()
    if user is not None and user.validate_pass(password):
        login_user(user, True)
        return "Logged in successfully", True
    return "Username or password incorrect. Please try again", False


def signin(username, password, password2, repo, session):
    if password == password2:
        user = repo.get_username(username)
        if not user:
            user = Users(username=username, password=password)
            #db.session.add(user)
            repo.add_user(user)
            session.commit()
            return "User signed up", True
        return "Username already exists, pick up another.", False
    return "Passwords are not equal. Try again", False


def get_books_by(column_name, value, repo):
    #books = Books.query.filter(
    #    Books.__table__.columns[column_name].like(f"%{value}%")
    #).all()
    books = repo.get_book_by_like(column_name, value)
    books = [] if books is None else books
    return books


def get_books_by_id(id_value, repo):
    #book = Books.query.get(id_value)
    book = repo.get_book_id(id_value)
    book = [] if book is None else book
    return book


def insert_book_review(book, user, review_value, review_comment, repo, session):
    if book.user_can_insert_review(user.id):
        new_review = Reviews(
            review_value=review_value,
            review_comment=review_comment,
            user_id=user.id,
            book_id=book.id,
        )
        #db.session.add(new_review)
        repo.add_review(new_review)
        session.commit()
        return "Review Inserted", True
    return "You have already inserted a review for this book", False
