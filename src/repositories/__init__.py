import os
import dependency_injector.providers as providers
import dependency_injector.containers as containers
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from src.repositories.repository import Repository

class RepositoryContainer(containers.DeclarativeContainer):

    URI = os.getenv("DATABASE_URL")
    engine  = providers.Singleton(create_engine, URI)
    session = providers.Singleton(Session, bind=engine)
    repository = providers.Singleton(Repository, session)

