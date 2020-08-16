class Reviews:
    def __init__(self, review_value, review_comment, user_id, book_id, review_id=None):
        self.id = review_id
        self.review_value = review_value
        self.review_comment = review_comment
        self.user_id = user_id
        self.book_id = book_id

    # id = db.Column(db.Integer, primary_key=True)
    # review_value = db.Column(db.Integer, nullable=False)
    # review_comment = db.Column(db.Text)
    # user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
