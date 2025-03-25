"""
Example of using the improved Floriday Supplier API Client.

This example demonstrates the new API design with simplified client initialization,
unified synchronization API, and improved resource management.
"""

import logging
from pprint import pprint

from floriday_supplier_client import TradeItemsApi
from floriday_supplier_client.client import Floriday, floriday

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def ex1_print_a_trade_item():
    """Example 1: Print a known trade item with direct API initialization."""
    print("\n=== Example 1: Print a known trade item (Direct API) ===\n")

    # Option 1: Direct API class initialization
    trade_items_api = floriday(TradeItemsApi)

    # Get trade items
    api_response = trade_items_api.get_trade_items_summary(
        trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
    )
    pprint(api_response)


def ex2_multiple_apis():
    """Example 2: Working with multiple APIs using a client instance."""
    print("\n=== Example 2: Working with Multiple APIs ===\n")

    # Option 2: Client with get_api method
    client = Floriday()

    # Get different API instances
    trade_items_api = client.get_api(TradeItemsApi)

    # Use trade items API
    api_response = trade_items_api.get_trade_items_summary(
        trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
    )
    pprint(api_response)

    # Use organizations API (would need appropriate permissions)
    try:
        # Import only when needed to avoid unused import error
        from floriday_supplier_client import OrganizationsApi

        organizations_api = client.get_api(OrganizationsApi)
        organization = organizations_api.get_current_organization()
        print(f"Organization: {organization}")
    except Exception as e:
        print(f"Could not get organization: {e}")


def persist_item(item):
    """Example persistence function for trade items."""
    print(
        f"Processing: {item.trade_item_id} - {getattr(item, 'trade_item_name', 'N/A')}"
    )
    return item.trade_item_id


def ex3_basic_trade_items_sync():
    """Example 3: Basic Trade Items Sync with simplified API."""
    print("\n=== Example 3: Basic Trade Items Sync (Simplified API) ===\n")

    # Create client and get API
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

    print(result)


def ex4_iterator_sync():
    """Example 4: Using iterator pattern for synchronization."""
    print("\n=== Example 4: Using Iterator Pattern for Sync ===\n")

    # Create client and get API
    client = Floriday()
    trade_items_api = client.get_api(TradeItemsApi)

    # Use iterator pattern for memory efficiency
    processed = 0
    for item in trade_items_api.sync_iter(start_seq=0, batch_size=10):
        # Process each item individually
        persist_item(item)
        processed += 1

        # Limit to 20 items for this example
        if processed >= 20:
            break

    print(f"Processed {processed} items")


def ex5_advanced_sync_control():
    """Example 5: Advanced synchronization control."""
    print("\n=== Example 5: Advanced Sync Control ===\n")

    # Create client and get API
    client = Floriday()
    trade_items_api = client.get_api(TradeItemsApi)

    # Create a synchronizer with advanced options
    sync = trade_items_api.create_sync(start_seq=0)

    # Configure the synchronizer
    sync.batch_size = 10
    sync.rate_limit_delay = 0.2  # seconds

    # Add event handlers
    sync.persist_entity_callback = persist_item

    # Execute the sync
    result = sync.execute()
    print(result)


def ex6_resource_management():
    """Example 6: Resource management with context manager."""
    print("\n=== Example 6: Resource Management with Context Manager ===\n")

    # Using context manager for automatic cleanup
    with Floriday() as client:
        trade_items_api = client.get_api(TradeItemsApi)
        api_response = trade_items_api.get_trade_items_summary(
            trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
        )
        print("Retrieved trade item with context manager")
    # Client is automatically closed when exiting the context

    # Manual resource management
    client = Floriday()
    try:
        trade_items_api = client.get_api(TradeItemsApi)
        api_response = trade_items_api.get_trade_items_summary(
            trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
        )
        print(f"Retrieved trade item with manual resource management")
    finally:
        client.close()  # Explicitly close resources


def ex7_configuration_options():
    """Example 7: Configuration options."""
    print("\n=== Example 7: Configuration Options ===\n")

    # Default configuration from environment variables
    Floriday()
    print("Client 1: Using environment variables")

    # Direct configuration (would need valid credentials)
    # Commented out to avoid unused variable warning
    # Floriday(
    #     client_id="my_client_id",
    #     client_secret="my_client_secret",
    #     api_key="my_api_key",
    #     base_url="https://api.floriday.io/api/v1/",
    # )
    # print("Client 2: Using direct configuration")


if __name__ == "__main__":
    print(
        "Note: This example demonstrates the improved API but requires proper credentials to run."
    )
    print(
        "Uncomment the function calls below to run the examples when you have valid credentials.\n"
    )

    # Uncomment to run examples
    # ex1_print_a_trade_item()
    # ex2_multiple_apis()
    # ex3_basic_trade_items_sync()
    # ex4_iterator_sync()
    # ex5_advanced_sync_control()
    # ex6_resource_management()
    # ex7_configuration_options()
