from flask import Flask
import numpy as np
from .reviews import Reviews
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

    def insert_book_review(self, user_id, review_value, review_comment=""):
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
