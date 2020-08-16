import mock
from tests.unit.test_base_services import BaseTestService


class TestExternalApiService(BaseTestService):
    @mock.patch("requests.get", mock.MagicMock(return_value={"Test": "Value"}))
    def test_get_json_from_goodreads(self, external_api_service):
        # Load IO

        # Mock internal service

        # Method under test
        response = external_api_service.get_json_from_goodreads(1234)

        # Assertions
        assert response == {"Test": "Value"}
