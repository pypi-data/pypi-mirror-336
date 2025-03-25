import os
from unittest.mock import patch, MagicMock

from floriday_supplier_client.api_factory import ApiFactory


@patch("floriday_supplier_client.api_factory.requests.request")
def test_host_set_from_environment_variable(mock_request):
    """Test host setting from environment variable.

    Verifies the API client uses the URL from FLORIDAY_BASE_URL.
    """
    # Mock the response from the token endpoint
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_request.return_value = mock_response

    # Set up environment variables for the test
    test_base_url = "https://test.floriday.io/suppliers-api-2024v1"
    with patch.dict(
        os.environ,
        {
            "FLORIDAY_CLIENT_ID": "test_client_id",
            "FLORIDAY_CLIENT_SECRET": "test_client_secret",
            "FLORIDAY_API_KEY": "test_api_key",
            "FLORIDAY_AUTH_URL": "https://test.auth.url",
            "FLORIDAY_BASE_URL": test_base_url,
        },
    ):
        # Create an instance of ApiFactory
        factory = ApiFactory()

        # Verify host is set from environment variable
        assert factory.configuration.host == test_base_url

        # Get API client and verify its configuration has correct host
        client = factory.get_api_client()
        assert client.configuration.host == test_base_url
