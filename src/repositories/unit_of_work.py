from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.repositories.repository import Repository


class UnitOfWork:
    def __init__(self, session_factory: sessionmaker, repository: Repository):
        self._session_factory = session_factory
        self.repository = repository

    def __enter__(self):
        self._session = self._session_factory()
        self.repository._set_session(self._session)
        return self

    def __exit__(self, *args):
        self._session.close()

    def rollback(self):
        self._session.rollback()

    def commit(self):
        try:
            self._session.commit()
        except SQLAlchemyError as e:
            self.rollback()
            raise (e)
