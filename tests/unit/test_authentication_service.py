from tests.unit.test_base_services import BaseTestService
from tests.unit import mock_io_data


class TestAuthenticationService(BaseTestService):
    def test_login_ok(self, authentication_service):
        # Load IO

        # Mock internal service
        repository = authentication_service.uow.get_repository_mock()
        repository.get_username.return_value = mock_io_data.user1

        # Method under test
        response = authentication_service.login("franco", "1234")

        # Assertions
        assert response == ("Logged in successfully", True, mock_io_data.user1)

    def test_login_fail(self, authentication_service):
        # Load IO

        # Mock internal service
        repository = authentication_service.uow.get_repository_mock()
        repository.get_username.return_value = mock_io_data.user1

        # Method under test
        response = authentication_service.login("franco", "12345")

        # Assertions
        assert response == (
            "Username or password incorrect. Please try again",
            False,
            None,
        )

    def test_signin_ok(self, authentication_service):
        # Load IO

        # Mock internal service
        repository = authentication_service.uow.get_repository_mock()
        repository.get_username.return_value = None

        # Method under test
        response = authentication_service.signin("franco", "1234", "1234")

        # Assertions
        assert response == ("User signed up", True)

    def test_signin_fail(self, authentication_service):
        # Load IO

        # Mock internal service
        repository = authentication_service.uow.get_repository_mock()
        repository.get_username.return_value = mock_io_data.user1

        # Method under test
        response = authentication_service.signin("franco", "1234", "1234")

        # Assertions
        assert response == ("Username already exists, pick up another.", False)

    def test_signin_not_equal_passwords(self, authentication_service):
        # Load IO

        # Mock internal service
        repository = authentication_service.uow.get_repository_mock()
        repository.get_username.return_value = None

        # Method under test
        response = authentication_service.signin("franco", "1234", "12345")

        # Assertions
        assert response == ("Passwords are not equal. Try again", False)
