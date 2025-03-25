"""
Tests for the client module.
"""

import pytest
from unittest.mock import Mock, patch

from floriday_supplier_client.client import Floriday, floriday, ApiWrapper


class MockApiClass:
    """Mock API class for testing."""

    def __init__(self, api_client):
        self.api_client = api_client

    def get_items_by_sequence_number(self, sequence_number, limit_result):
        """Mock method for testing."""
        return Mock(maximum_sequence_number=10, results=[])


class MockApiFactory:
    """Mock ApiFactory for testing."""

    def get_api_instance(self, api_class):
        """Mock method for testing."""
        return api_class(Mock())

    def get_api_client(self):
        """Mock method for testing."""
        return Mock()


@pytest.mark.integration
def test_floriday_function():
    """Test the floriday function."""
    from floriday_supplier_client import TradeItemsApi

    # Test creating a client and use it as a context manager
    with floriday() as client:
        assert isinstance(client, Floriday)

    # Test creating an API instance directly and use it via the client context manager
    with floriday() as client:
        api = client.get_api(TradeItemsApi)
        assert isinstance(api, ApiWrapper)
        assert hasattr(
            api, "get_trade_items_summary"
        )  # Verify it has the expected API methods


@patch("floriday_supplier_client.client.ApiFactory")
def test_floriday_client_init(mock_api_factory):
    """Test Floriday client initialization."""
    # Setup
    mock_factory_instance = Mock()
    mock_api_factory.return_value = mock_factory_instance

    # Test with default options
    with Floriday():
        pass
    mock_api_factory.assert_called_once()

    # Test with custom options
    with Floriday(
        client_id="test_id",
        client_secret="test_secret",
        api_key="test_key",
        auth_url="https://test.auth.url",
        base_url="https://test.base.url",
    ):
        pass
    assert mock_api_factory.call_count == 2


@pytest.mark.integration
def test_get_api():
    """Test get_api method."""
    from floriday_supplier_client import TradeItemsApi, OrganizationsApi

    # Use the client as a context manager
    with Floriday() as client:
        # Get an API instance
        trade_items_api = client.get_api(TradeItemsApi)
        assert isinstance(trade_items_api, ApiWrapper)
        assert hasattr(trade_items_api, "get_trade_items_summary")

        # Get the same API instance again (should be cached)
        trade_items_api2 = client.get_api(TradeItemsApi)
        assert trade_items_api is trade_items_api2

        # Get a different API instance
        organizations_api = client.get_api(OrganizationsApi)
        assert isinstance(organizations_api, ApiWrapper)
        assert hasattr(organizations_api, "get_organization_by_id")

        # Verify they are different instances
        assert trade_items_api is not organizations_api


@patch("floriday_supplier_client.client.ApiFactory")
def test_refresh_token(mock_api_factory):
    """Test refresh_token method."""
    # Setup
    mock_factory_instance = Mock()
    mock_api_factory.return_value = mock_factory_instance

    # Use the client as a context manager
    with Floriday() as client:
        # Get an API instance to populate the cache
        client._api_cache["MockApiClass"] = Mock()

        # Refresh the token
        client.refresh_token()

        # Verify the token was refreshed
        assert mock_factory_instance._get_access_token.called
        assert mock_factory_instance._configure_client.called

        # Verify the API cache was cleared
        assert not client._api_cache


@patch("floriday_supplier_client.client.ApiFactory")
def test_context_manager(mock_api_factory):
    """Test context manager support."""
    # Setup
    mock_factory_instance = Mock()
    mock_api_factory.return_value = mock_factory_instance

    # Use the client as a context manager
    with Floriday() as client:
        # Get an API instance to populate the cache
        client._api_cache["MockApiClass"] = Mock()

    # Verify the API cache was cleared
    assert not client._api_cache


@patch("floriday_supplier_client.client.sync_entities")
@pytest.mark.integration
def test_api_wrapper_sync(mock_sync_entities):
    """Test ApiWrapper sync method."""
    from floriday_supplier_client import TradeItemsApi

    # Use the client as a context manager
    with Floriday() as client:
        # Get an API wrapper
        wrapper = client.get_api(TradeItemsApi)

        # Call sync
        wrapper.sync(start_seq=0, on_item=lambda x: x)

        # Verify sync_entities was called
        mock_sync_entities.assert_called_once()


@patch("floriday_supplier_client.client.EntitySynchronizer")
@pytest.mark.integration
def test_api_wrapper_create_sync(mock_entity_synchronizer):
    """Test ApiWrapper create_sync method."""
    from floriday_supplier_client import TradeItemsApi

    # Setup
    mock_synchronizer = Mock()
    mock_entity_synchronizer.return_value = mock_synchronizer

    # Use the client as a context manager
    with Floriday() as client:
        # Get an API wrapper
        wrapper = client.get_api(TradeItemsApi)

        # Call create_sync
        result = wrapper.create_sync(start_seq=0)

        # Verify EntitySynchronizer was created
        mock_entity_synchronizer.assert_called_once()
        assert result is mock_synchronizer


# Test for sync_iter will be added in a future increment
