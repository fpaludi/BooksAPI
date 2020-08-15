import pytest
from abc import ABC
from settings import create_app, update_settings
from create_tables import create_tables, delete_tables
from tests.integration.fake_mock_data import DBTestingData

CONF_NAME = "testing"


def pytest_configure():
    print("INITIAL Test configuration")
    print("Upload Setting object for testing pourposes")
    update_settings(CONF_NAME)


class BaseTestControllers(ABC):
    @pytest.fixture(scope="class")
    def client(self):
        # Create App Object
        app = create_app(CONF_NAME)

        # Create DB for testing
        self.create_testing_database()

        # "Running"
        test_client = app.test_client()
        try:
            yield test_client
        finally:
            # Clean testing DB to start clean every run tests
            self.delete_testing_database()

    @pytest.fixture(scope="function")
    def unit_of_work(self):
        from src.repositories import RepositoryContainer

        uow = RepositoryContainer.uow()
        return uow

    def create_testing_database(self):
        from src.repositories import RepositoryContainer

        engine = RepositoryContainer.engine()
        session = RepositoryContainer.DEFAULT_SESSIONFACTORY()
        if "_test" not in str(engine.url):
            print("Tests are running over production or development database")
            print(f"Database url: {engine.url}")
            raise (ValueError)

        print()
        print("*" * 80)
        print("TEST DB OPERATIONS")
        print("*" * 80)
        create_tables(engine, session)
        uow = RepositoryContainer.uow()

        # Add User
        with uow:
            new_user = dict(
                username=DBTestingData.TEST_USER, password=DBTestingData.TEST_PSW
            )
            uow.repository.add_user(new_user)
            uow.commit()

            # Add Review for User
            user = uow.repository.get_username(DBTestingData.TEST_USER)
            book = uow.repository.get_book_by_like(
                "title", DBTestingData.BOOK_TITLE_W_REVIEW
            )[0]
            new_review = dict(
                review_value="1",
                review_comment="test comment",
                user_id=user.id,
                book_id=book.id,
            )
            uow.repository.add_review(new_review)
            uow.commit()
        print("-" * 80)

    def delete_testing_database(self):
        from src.repositories import RepositoryContainer

        print()
        print("*" * 80)
        print("TEST DB OPERATIONS")
        print("*" * 80)
        engine = RepositoryContainer.engine()
        session = RepositoryContainer.DEFAULT_SESSIONFACTORY()
        delete_tables(engine, session)
        print("-" * 80)

    # @classmethod
    # def setup_class(cls):
    #    # Create Env Variables and App
    #    CONF_NAME = "testing"
    #    app = create_app(CONF_NAME)
    #    # Create DB for testing
    #    create_tables()

    # @classmethod
    # def teardown_method(cls):
    #    # Clean testing DB to start clean every run tests
    #    delete_tables()
