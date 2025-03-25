import os
import pytest
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
    test_base_url = f"https://test.floriday.io/suppliers-api-{ApiFactory.EXPECTED_API_VERSION}"
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


@patch("floriday_supplier_client.api_factory.requests.request")
def test_api_version_validation_success(mock_request):
    """Test API version validation succeeds with correct version.

    Verifies the ApiFactory initializes correctly when the API version in the base URL
    matches the expected version.
    """
    # Mock the response from the token endpoint
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_request.return_value = mock_response

    # Set up environment variables with correct API version
    with patch.dict(
        os.environ,
        {
            "FLORIDAY_CLIENT_ID": "test_client_id",
            "FLORIDAY_CLIENT_SECRET": "test_client_secret",
            "FLORIDAY_API_KEY": "test_api_key",
            "FLORIDAY_AUTH_URL": "https://test.auth.url",
            "FLORIDAY_BASE_URL": f"https://test.floriday.io/suppliers-api-{ApiFactory.EXPECTED_API_VERSION}",
        },
    ):
        # This should not raise an exception
        factory = ApiFactory()
        assert factory is not None


@patch("floriday_supplier_client.api_factory.requests.request")
def test_api_version_validation_failure(mock_request):
    """Test API version validation fails with incorrect version.

    Verifies the ApiFactory raises a ValueError when the API version in the base URL
    doesn't match the expected version.
    """
    # Mock the response from the token endpoint
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_request.return_value = mock_response

    # Set up environment variables with incorrect API version
    with patch.dict(
        os.environ,
        {
            "FLORIDAY_CLIENT_ID": "test_client_id",
            "FLORIDAY_CLIENT_SECRET": "test_client_secret",
            "FLORIDAY_API_KEY": "test_api_key",
            "FLORIDAY_AUTH_URL": "https://test.auth.url",
            "FLORIDAY_BASE_URL": "https://test.floriday.io/suppliers-api-2023v2",  # Wrong version
        },
    ):
        # This should raise a ValueError
        with pytest.raises(ValueError) as excinfo:
            ApiFactory()
        
        # Check that the error message contains the expected and actual versions
        assert "API version mismatch" in str(excinfo.value)
        assert "2023v2" in str(excinfo.value)
        assert ApiFactory.EXPECTED_API_VERSION in str(excinfo.value)


@patch("floriday_supplier_client.api_factory.requests.request")
def test_api_version_validation_invalid_url(mock_request):
    """Test API version validation fails with invalid URL format.

    Verifies the ApiFactory raises a ValueError when the base URL doesn't contain
    the expected 'suppliers-api-XXX' pattern.
    """
    # Mock the response from the token endpoint
    mock_response = MagicMock()
    mock_response.json.return_value = {"access_token": "test_token"}
    mock_request.return_value = mock_response

    # Set up environment variables with invalid URL format
    with patch.dict(
        os.environ,
        {
            "FLORIDAY_CLIENT_ID": "test_client_id",
            "FLORIDAY_CLIENT_SECRET": "test_client_secret",
            "FLORIDAY_API_KEY": "test_api_key",
            "FLORIDAY_AUTH_URL": "https://test.auth.url",
            "FLORIDAY_BASE_URL": "https://test.floriday.io/invalid-url-format",  # Invalid format
        },
    ):
        # This should raise a ValueError
        with pytest.raises(ValueError) as excinfo:
            ApiFactory()
        
        # Check that the error message indicates invalid format
        assert "Invalid base URL format" in str(excinfo.value)
