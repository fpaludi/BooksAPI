from flask import Flask
from flask_login import UserMixin, AnonymousUserMixin
import numpy as np
from .. import login_manager, db


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    # Relationships
    reviews = db.relationship("Reviews", backref="books", lazy=True)

    def get_review_average(self):
        if self.get_review_count() == 0:
            return None
        else:
            return np.array([x.review_value for x in self.reviews]).mean()

    def get_review_count(self):
        return len(self.reviews)

    def insert_review(self, user_id, review_value, review_comment=""):
        if self.user_can_insert_review(user_id):
            new_review = Reviews(
                review_value=review_value,
                review_comment=review_comment,
                user_id=user_id,
                book_id=self.id,
            )
            db.session.add(new_review)
            db.session.commit()
            return 1, "Review Inserted"
        return 0, "You have already inserted a review for this book"

    def user_can_insert_review(self, user_id):
        user_reviews = Reviews.query.filter_by(user_id=user_id, book_id=self.id).first()
        return user_reviews is None


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def validate_pass(self, password):
        return self.password == password

    def add_user(self):
        if not Users.query.filter_by(name=self.name).first():
            db.session.add(self)
            db.session.commit()
            return 1, "User signed up"
        return 0, "Username already exists, pick up another"


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    review_value = db.Column(db.Integer, nullable=False)
    review_comment = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)


# +++++++++++++++++++++++++++++++++++++++++++++++++
# Logged In Users
# +++++++++++++++++++++++++++++++++++++++++++++++++
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
