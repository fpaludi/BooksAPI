import dependency_injector.providers as providers
import dependency_injector.containers as containers
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from settings import Settings
from src.repositories.repository import Repository


class RepositoryContainer(containers.DeclarativeContainer):
    engine = providers.Singleton(create_engine, Settings.DATABASE_URL)
    session = providers.Singleton(Session, bind=engine)
    repository = providers.Singleton(Repository, session)
