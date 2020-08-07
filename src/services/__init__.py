import dependency_injector.containers as containers
import dependency_injector.providers as providers
from settings import Settings
from src.repositories import RepositoryContainer
from src.services.book_service import BookServices
from src.services.authentication_service import AuthenticationService
from src.services.external_api_service import ExternalApiService

class ServicesContainer(containers.DeclarativeContainer):
    book_service = providers.Factory(BookServices, RepositoryContainer.repository)
    auth_service = providers.Factory(AuthenticationService, RepositoryContainer.repository)

    api_service  = providers.Factory(ExternalApiService, Settings.GOODREAD_API_URL, Settings.GOODREAD_API_KEY)



