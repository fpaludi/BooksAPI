import numpy as np
from src.models.reviews import Reviews


class Books:
    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        # Relationships
        self.reviews: list[Reviews] = []
        # reviews = db.relationship("Reviews", backref="books", lazy=True)

    def get_review_average(self):
        if self.get_review_count() == 0:
            return None
        else:
            return np.array([r.review_value for r in self.reviews]).mean()

    def get_review_count(self):
        return len(self.reviews)

    def user_can_insert_review(self, user_id):
        result = user_id in (r.user_id for r in self.reviews)
        return not result
