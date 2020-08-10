from tests.integration.conftest import BaseTestControllers
from tests.integration.fake_mock_data import DBTestingData


class TestControllers(BaseTestControllers):
    def test_index_get(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_index_post_unregistered_user(self, client):
        response = client.post(
            "/",
            data={"username": "franco", "password": 1234},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        assert b"<title> Log In </title>" in response.data

    def test_index_post_registered_user(self, client):
        response = client.post(
            "/",
            data={
                "username": DBTestingData.TEST_USER,
                "password": DBTestingData.TEST_PSW,
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"<title> Filter Books </title>" in response.data

    def test_sign_in_new_user_post(self, client, repository):
        # Unregistered user
        response = client.post(
            "/sign_in",
            data={
                "username": "new_user",
                "password": 1234,
                "password2": 1234,
                "submit": True,
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        user = repository.get_username("new_user")
        assert response.status_code == 200  # redirect code
        assert b"<title> Log In </title>" in response.data
        assert user is not None
        assert user.username == "new_user"

    def test_sign_in_registered_user_post(self, client, repository):
        # Recent registered user
        response = client.post(
            "/sign_in",
            data={
                "username": DBTestingData.TEST_USER,
                "password": 1234,
                "password2": 1234,
                "submit": True,
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        user = repository.get_username("test_user")
        assert response.status_code == 200  # redirect code
        assert b"<title> Sign In </title>" in response.data
        assert user is not None
        assert user.username == "test_user"
