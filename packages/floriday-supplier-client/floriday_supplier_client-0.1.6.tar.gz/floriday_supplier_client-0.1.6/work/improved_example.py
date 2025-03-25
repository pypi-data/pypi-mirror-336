"""
Improved example of using the Floriday Supplier API Client.

This example demonstrates how the API could be improved for better developer experience.
"""

import logging

# Hypothetical improved imports
# Note: These imports don't exist in the current implementation
# They represent how the API could be improved
from floriday_supplier_client import TradeItem
from floriday_supplier_client.api import TradeItemsApi, OrganizationsApi

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def ex1_print_a_trade_item():
    """Example 1: Print a known trade item with improved API."""
    print("\n=== Example 1: Print a known trade item (Improved API) ===\n")

    # Option 1: Direct API class initialization
    trade_items_api = Floriday(TradeItemsApi)

    # Get a trade item by ID
    trade_item = trade_items_api.get_by_id("1987a15c-2c28-4ba6-89a1-3780e585b42c")
    print(f"Trade Item: {trade_item.trade_item_id} - {trade_item.trade_item_name}")

    # Rich object representation
    print(trade_item)


def ex2_multiple_apis():
    """Example 2: Working with multiple APIs."""
    print("\n=== Example 2: Working with Multiple APIs (Improved API) ===\n")

    # Option 2: Client with get_api method
    client = Floriday()

    # Get different API instances
    trade_items_api = client.get_api(TradeItemsApi)
    organizations_api = client.get_api(OrganizationsApi)

    # Use trade items API
    trade_item = trade_items_api.get_by_id("1987a15c-2c28-4ba6-89a1-3780e585b42c")
    print(f"Trade Item: {trade_item.trade_item_id}")

    # Use organizations API
    organization = organizations_api.get_current_organization()
    print(f"Organization: {organization.name}")


def persist_item(item: TradeItem) -> str:
    """Example persistence function for trade items."""
    print(
        f"Processing: {item.trade_item_id} - {getattr(item, 'trade_item_name', 'N/A')}"
    )
    return item.trade_item_id


def ex3_basic_trade_items_sync():
    """Example 3: Basic Trade Items Sync with improved API."""
    print("\n=== Example 3: Basic Trade Items Sync (Improved API) ===\n")

    # Create client
    client = Floriday()
    trade_items_api = client.get_api(TradeItemsApi)

    # Simple synchronization with callback
    result = trade_items_api.sync(
        # Starting sequence number
        start_seq=0,
        # Callback for each item
        on_item=persist_item,
        # Configuration options
        batch_size=50,
        rate_limit=0.5,  # seconds between requests
    )

    print(f"Sync completed: {result.success}")
    print(f"Processed {result.entities_processed} items")
    print(
        f"Sequence range: {result.start_sequence_number} → {result.end_sequence_number}"
    )


def ex4_iterator_sync():
    """Example 4: Using iterator pattern for synchronization."""
    print("\n=== Example 4: Using Iterator Pattern for Sync (Improved API) ===\n")

    # Create client
    client = Floriday()
    trade_items_api = client.get_api(TradeItemsApi)

    # Get a database connection (hypothetical)
    db = get_database_connection()

    # Get last processed sequence number from database
    last_seq = db.get_last_sequence_number("trade_items") or 0

    # Use iterator pattern for memory efficiency
    processed = 0
    for item in trade_items_api.sync_iter(start_seq=last_seq):
        # Process each item individually
        db.save_trade_item(item)
        processed += 1

        # Update sequence number periodically
        if processed % 100 == 0:
            db.update_sequence_number("trade_items", item.sequence_number)

    # Final update
    if processed > 0:
        db.update_sequence_number("trade_items", item.sequence_number)

    print(f"Processed {processed} items")


def ex5_advanced_sync_control():
    """Example 5: Advanced synchronization control."""
    print("\n=== Example 5: Advanced Sync Control (Improved API) ===\n")

    # Create client
    client = Floriday()
    trade_items_api = client.get_api(TradeItemsApi)

    # Create a synchronizer with advanced options
    sync = trade_items_api.create_sync(start_seq=0)

    # Configure the synchronizer
    sync.batch_size = 100
    sync.rate_limit = 0.2  # seconds

    # Add event handlers
    sync.on_batch_start = lambda seq: print(f"Starting batch at sequence {seq}")
    sync.on_batch_complete = lambda batch: print(
        f"Completed batch with {len(batch)} items"
    )
    sync.on_item = persist_item

    # Execute the sync
    result = sync.execute()
    print(result)


def ex6_configuration():
    """Example 6: Configuration options."""
    print("\n=== Example 6: Configuration Options ===\n")

    # Default configuration from environment variables
    client1 = Floriday()
    print("Client 1: Using environment variables")

    # Direct configuration
    client2 = Floriday(
        client_id="my_client_id",
        client_secret="my_client_secret",
        api_key="my_api_key",
        base_url="https://api.floriday.io/api/v1/",
    )
    print("Client 2: Using direct configuration")


def ex7_resource_management():
    """Example 7: Resource management."""
    print("\n=== Example 7: Resource Management ===\n")

    # Using context manager for automatic cleanup
    with Floriday() as client:
        trade_items_api = client.get_api(TradeItemsApi)
        items = trade_items_api.get_all(limit=10)
        print(f"Retrieved {len(items)} items")
    # Client is automatically closed when exiting the context

    # Manual resource management
    client = Floriday()
    try:
        trade_items_api = client.get_api(TradeItemsApi)
        items = trade_items_api.get_all(limit=10)
        print(f"Retrieved {len(items)} items")
    finally:
        client.close()  # Explicitly close resources


def get_database_connection():
    """Mock function to simulate getting a database connection."""

    class MockDB:
        def get_last_sequence_number(self, entity_type):
            return 0

        def save_trade_item(self, item):
            print(f"Saving item {item.trade_item_id}")

        def update_sequence_number(self, entity_type, seq_number):
            print(f"Updating sequence number for {entity_type}: {seq_number}")

    return MockDB()


# Hypothetical Floriday class implementation
class Floriday:
    """
    Hypothetical improved Floriday client class.

    This class doesn't exist in the current implementation but represents
    how the API could be improved for better developer experience.
    """

    def __init__(self, api_class=None, **kwargs):
        """
        Initialize a Floriday client.

        Args:
            api_class: Optional API class to directly initialize a specific API.
            **kwargs: Configuration options (client_id, client_secret, etc.)
        """
        # If an API class is provided, return an instance of that API
        if api_class:
            # This would be the implementation for Option 1
            return api_class(self)

    def get_api(self, api_class):
        """
        Get an API instance by class.

        Args:
            api_class: API class

        Returns:
            API instance
        """
        # This would be the implementation for Option 2
        return api_class(self)

    def close(self):
        """Close the client and release resources."""
        print("Client closed")

    def __enter__(self):
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        self.close()


if __name__ == "__main__":
    print(
        "Note: This is a hypothetical improved API example and won't run with the current implementation."
    )
    print(
        "It demonstrates how the API could be improved for better developer experience.\n"
    )

    # Uncomment to run examples when implemented
    # ex1_print_a_trade_item()
    # ex2_multiple_apis()
    # ex3_basic_trade_items_sync()
    # ex4_iterator_sync()
    # ex5_advanced_sync_control()
    # ex6_configuration()
    # ex7_resource_management()
