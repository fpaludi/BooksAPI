from tests.unit.test_base_services import BaseTestService


class TestBookService(BaseTestService):
    def test_get_books_by_id(self, book_service):
        # Load IO

        # Mock internal service
        mock_result = [{"Book": "1234"}]
        repository = book_service.get_repository_mock()
        repository.get_book_id.return_value = mock_result

        # Method under test
        response = book_service.get_books_by_id(1234)

        # Assertions
        assert response == mock_result
