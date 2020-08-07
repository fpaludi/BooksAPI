import os
import dependency_injector.containers as containers
import dependency_injector.providers as providers
from src.repositories import RepositoryContainer

from src.services.book_service import BookServices
from src.services.authentication_service import AuthenticationService
from src.services.external_api_service import ExternalApiService

class ServicesContainer(containers.DeclarativeContainer):
    book_service = providers.Factory(BookServices, RepositoryContainer.repository)
    auth_service = providers.Factory(AuthenticationService, RepositoryContainer.repository)

    GOODREAD_API_URL = os.getenv("GOODREAD_API_URL")
    GOODREAD_API_KEY = os.getenv("GOODREAD_API_KEY")
    print(GOODREAD_API_URL, GOODREAD_API_KEY)
    api_service  = providers.Factory(ExternalApiService, GOODREAD_API_URL, GOODREAD_API_KEY)



