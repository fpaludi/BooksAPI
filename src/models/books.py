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
            return np.array([r.review_value for r in self.reviews]).mean()

    def get_review_count(self):
        return len(self.reviews)

    def user_can_insert_review(self, user_id):
        result = user_id in [r.user_id for r in self.reviews]
        return not result
