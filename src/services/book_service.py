# from src.models.books import Books
# from src.models.users import Users
# from src.models.reviews import Reviews


class BookServices:
    def __init__(self, repository):
        self._repository = repository

    def get_books_by(self, column_name, value):
        # books = Books.query.filter(
        #    Books.__table__.columns[column_name].like(f"%{value}%")
        # ).all()
        books = self._repository.get_book_by_like(column_name, value)
        books = [] if books is None else books
        return books

    def get_books_by_id(self, id_value):
        # book = Books.query.get(id_value)
        book = self._repository.get_book_id(id_value)
        book = [] if book is None else book
        return book

    def insert_book_review(self, book, user, review_value, review_comment):
        if book.user_can_insert_review(user.id):
            new_review = dict(
                review_value=review_value,
                review_comment=review_comment,
                user_id=user.id,
                book_id=book.id,
            )

            # new_review = Reviews(
            #     review_value=review_value,
            #     review_comment=review_comment,
            #     user_id=user.id,
            #     book_id=book.id,
            # )
            # db.session.add(new_review)
            self._repository.add_review(new_review)
            return "Review Inserted", True
        return "You have already inserted a review for this book", False
