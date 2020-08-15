from sqlalchemy import inspect
from sqlalchemy.orm import Session
from src.models.books import Books
from src.models.reviews import Reviews
from src.models.users import Users


class Repository:
    def __init__(self):
        self._session = None

    def _set_session(self, session: Session):
        self._session = session

    # --------------------------------
    # User Table
    # --------------------------------
    def get_username(self, username):
        return self._session.query(Users).filter_by(username=username).first()

    def add_user(self, user):
        new_user = Users(**user)
        self._session.add(new_user)

    def get_user_id(self, id_ref):
        return self._session.query(Users).get(id_ref)

    # --------------------------------
    # Books Table
    # --------------------------------
    def get_book_by_like(self, column_name, value):
        insp = inspect(Books)
        return (
            self._session.query(Books).filter(
                insp.all_orm_descriptors[column_name].like(f"%{value}%")
            )
            # .filter(Books.__table__.columns[column_name].like(f"%{value}%"))
            .all()
        )

    def get_book_id(self, id_ref):
        return self._session.query(Books).get(id_ref)

    # --------------------------------
    # Reviews Table
    # --------------------------------
    def add_review(self, review):
        new_review = Reviews(**review)
        self._session.add(new_review)
