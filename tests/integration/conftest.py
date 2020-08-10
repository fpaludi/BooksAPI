import pytest
from abc import ABC
from settings import create_app
from create_tables import create_tables, delete_tables
from tests.integration.fake_mock_data import DBTestingData


def pytest_configure():
    pass


class BaseTestControllers(ABC):
    @pytest.fixture(scope="class")
    def client(self):
        # Create Env Variables
        conf_name = "testing"
        app = create_app(conf_name)

        # Create DB for testing
        self.create_testing_database()

        # "Running"
        test_client = app.test_client()
        yield test_client

        # Clean testing DB to start clean every run tests
        self.delete_testing_database()

    @pytest.fixture(scope="function")
    def repository(self):
        from src.repositories import RepositoryContainer

        repository = RepositoryContainer.repository()
        return repository

    def create_testing_database(self):
        from src.repositories import RepositoryContainer

        engine = RepositoryContainer.engine()
        session = RepositoryContainer.session()
        create_tables(engine, session)

        repository = RepositoryContainer.repository()

        # Add User
        new_user = dict(username=DBTestingData.TEST_USER, password=DBTestingData.TEST_PSW)
        repository.add_user(new_user)

        # Add Review for User
        user = repository.get_username(DBTestingData.TEST_USER)
        book = repository.get_book_by_like("title", DBTestingData.BOOK_TITLE_W_REVIEW)[0]
        new_review = dict(
            review_value="1",
            review_comment="test comment",
            user_id=user.id,
            book_id=book.id,
        )
        repository.add_review(new_review)

    def delete_testing_database(self):
        from src.repositories import RepositoryContainer

        engine = RepositoryContainer.engine()
        session = RepositoryContainer.session()
        delete_tables(engine, session)

    # @classmethod
    # def setup_class(cls):
    #    # Create Env Variables and App
    #    conf_name = "testing"
    #    app = create_app(conf_name)
    #    # Create DB for testing
    #    create_tables()

    # @classmethod
    # def teardown_method(cls):
    #    # Clean testing DB to start clean every run tests
    #    delete_tables()
