from tests.unit.test_base_services import BaseTestService
from tests.unit import mock_io_data


class TestBookService(BaseTestService):
    def test_get_books_by_id(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = [{"title": "Harry Potter"}]
        repository = book_service.uow.get_repository_mock()
        repository.get_book_id.return_value = mock_result

        # Method under test
        response = book_service.get_books_by_id(1234)

        # Assertions
        assert response == mock_result

    def test_get_books_by_id_no_exists(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = []
        repository = book_service.uow.get_repository_mock()
        repository.get_book_id.return_value = mock_result

        # Method under test
        response = book_service.get_books_by_id(1234)

        # Assertions
        assert response == mock_result

    def test_get_books_by(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = [{"title": "Harry Potter"}]
        repository = book_service.uow.get_repository_mock()
        repository.get_book_by_like.return_value = mock_result

        # Method under test
        response = book_service.get_books_by("title", "Harry Potter")

        # Assertions
        assert response == mock_result

    def test_get_books_by_no_exists(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = []
        repository = book_service.uow.get_repository_mock()
        repository.get_book_by_like.return_value = mock_result

        # Method under test
        response = book_service.get_books_by("title", "Harry Potter")

        # Assertions
        assert response == mock_result

    def test_insert_book_review_ok(self, book_service):
        # Load IO
        user = mock_io_data.user1
        book = mock_io_data.book2

        # Method under test
        response = book_service.insert_book_review(book, user, 5, "Hola")

        # Assertions
        assert response == ("Review Inserted", True)

    def test_insert_book_review_fail(self, book_service):
        # Load IO
        user = mock_io_data.user1
        book = mock_io_data.book1

        # Method under test
        response = book_service.insert_book_review(book, user, 5, "Hola")

        # Assertions
        assert response == ("You have already inserted a review for this book", False)
