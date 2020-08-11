import pytest
import mock
from abc import ABC
from src.services.book_service import BookServices
from src.services.external_api_service import ExternalApiService
from src.repositories.repository import Repository


class BaseTestService(ABC):
    def teardown_method(self):
        pass

    @pytest.fixture(scope="function")
    def repository_mock(self):
        return mock.create_autospec(Repository)

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
    def book_service(self, repository_mock):
        # Service
        book_service = BookServices(repository=repository_mock)

        # Lambdas
        book_service.get_repository_mock = lambda: repository_mock

        return book_service

    @pytest.fixture(scope="function")
    def external_api_service(self, repository_mock):
        # Service
        external_api_service = ExternalApiService("URL", "KEY")

        return external_api_service
