from sqlalchemy import inspect
from src.models.books import Books
from src.models.users import Users
from src.models.reviews import Reviews

class Repository:
    def __init__(self, session):
        self._session = session

    # --------------------------------
    # User Table
    # --------------------------------
    def get_username(self, username):
        return self._session.query(Users).filter_by(username=username).first()

    def add_user(self, user):
        self._session.add(user)
    
    def get_user_id(self, id_ref):
        return self._session.query(Users).get(id_ref)        

    # --------------------------------
    # Books Table
    # --------------------------------
    def get_book_by_like(self, column_name, value):
        insp = inspect(Books)
        return (
            self._session.query(Books)
            .filter(insp.all_orm_descriptors[column_name].like(f"%{value}%"))
            #.filter(Books.__table__.columns[column_name].like(f"%{value}%"))
            .all()
        )

    def get_book_id(self, id_ref):
        return self._session.query(Books).get(id_ref)

    # --------------------------------
    # Reviews Table
    # --------------------------------
    def add_review(self, review):
        self._session.add(review)
        self._session.commit()
