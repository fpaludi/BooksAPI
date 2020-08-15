import pytest
import mock
from abc import ABC
from sqlalchemy.orm import sessionmaker, Session
from src.services.book_service import BookServices
from src.services.external_api_service import ExternalApiService
from src.repositories.repository import Repository
from src.repositories.unit_of_work import UnitOfWork


class BaseTestService(ABC):
    def teardown_method(self):
        pass

    @pytest.fixture(scope="function")
    def repository_mock(self):
        return mock.create_autospec(Repository)

    @pytest.fixture(scope="function")
    def session_mock(self):
        return mock.create_autospec(Session)

    @pytest.fixture(scope="function")
    def sessionmaker_mock(self, session_mock):
        session_factory_mock = mock.create_autospec(sessionmaker)
        session_factory_mock.return_value = session_mock
        return session_factory_mock

    @pytest.fixture(scope="function")
    def book_service_mock(self):
        return mock.create_autospec(BookServices)

    # @pytest.fixture(scope='function')
    # def authentication_service_mock(self):
    #     return mock.create_autospec(AuthenticationService)

    @pytest.fixture(scope="function")
    def external_api_service_mock(self):
        return mock.create_autospec(ExternalApiService)

    @pytest.fixture(scope="function")
    def unit_of_work(self, sessionmaker_mock, repository_mock):
        uow = UnitOfWork(sessionmaker_mock, repository_mock)
        # Lambdas
        uow.get_sessionmaker_mock = lambda: sessionmaker_mock
        uow.get_repository_mock = lambda: repository_mock

        return uow

    @pytest.fixture(scope="function")
    def book_service(self, unit_of_work):
        # Service
        book_service = BookServices(uow=unit_of_work)

        return book_service

    @pytest.fixture(scope="function")
    def external_api_service(self, repository_mock):
        # Service
        external_api_service = ExternalApiService("URL", "KEY")

        return external_api_service
