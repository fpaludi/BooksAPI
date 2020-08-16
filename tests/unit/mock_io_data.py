from src.models.books import Books
from src.models.reviews import Reviews
from src.models.users import Users


user1 = Users(username="franco", password="1234")
user1.id = 1
user2 = Users(username="laura", password="pass")
user2.id = 2

book1 = Books(isbn="HP1", title="Harry Potter 1", author="J.K. Rowling", year=1999)
book1.id = 1
book2 = Books(isbn="HP2", title="Harry Potter 2", author="J.K. Rowling", year=2001)
book2.id = 2

review1 = Reviews(review_value=5, review_comment="Excelente", user_id=1, book_id=1)
review2 = Reviews(review_value=5, review_comment="Magico", user_id=2, book_id=1)

book1.reviews = [review1, review2]
