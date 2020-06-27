import abc
from sqlalchemy import inspect
from ..models.books import Books
from ..models.users import Users
from ..models.reviews import Reviews


class AbstractRepository(abc.ABC):
    # --------------------------------
    # User Table
    # --------------------------------
    @abc.abstractmethod
    def get_username(self, username):
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user):
        raise NotImplementedError

    # --------------------------------
    # Books Table
    # --------------------------------
    @abc.abstractmethod
    def get_book_by_like(self, column_name, value):
        raise NotImplementedError

    @abc.abstractmethod
    def get_book_id(self, id):
        raise NotImplementedError

    # --------------------------------
    # Reviews Table
    # --------------------------------
    @abc.abstractmethod
    def add_review(self, review):
        raise NotImplementedError


class Repository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    # --------------------------------
    # User Table
    # --------------------------------
    def get_username(self, username):
        return self.session.query(Users).filter_by(username=username).first()

    def add_user(self, user):
        self.session.add(user)
    
    def get_user_id(self, id_ref):
        return self.session.query(Users).get(id_ref)        

    # --------------------------------
    # Books Table
    # --------------------------------
    def get_book_by_like(self, column_name, value):
        insp = inspect(Books)
        return (
            self.session.query(Books)
            .filter(insp.all_orm_descriptors[column_name].like(f"%{value}%"))
            #.filter(Books.__table__.columns[column_name].like(f"%{value}%"))
            .all()
        )

    def get_book_id(self, id_ref):
        return self.session.query(Books).get(id_ref)

    # --------------------------------
    # Reviews Table
    # --------------------------------
    def add_review(self, review):
        self.session.add(review)
