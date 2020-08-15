import dependency_injector.providers as providers
import dependency_injector.containers as containers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import Settings
from src.repositories.unit_of_work import UnitOfWork
from src.repositories.repository import Repository


class RepositoryContainer(containers.DeclarativeContainer):
    engine = providers.Singleton(create_engine, Settings.DATABASE_URL)
    DEFAULT_SESSIONFACTORY = sessionmaker(bind=engine())
    repository_factory = providers.Factory(Repository)
    uow = providers.Factory(UnitOfWork, DEFAULT_SESSIONFACTORY, repository_factory)
