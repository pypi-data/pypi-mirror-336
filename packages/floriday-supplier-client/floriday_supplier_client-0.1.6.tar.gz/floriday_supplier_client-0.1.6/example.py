import logging
from pprint import pprint

from floriday_supplier_client import (
    TradeItemsApi,
    OrganizationsApi,
)
from floriday_supplier_client.client import Floriday
from floriday_supplier_client.sync import sync_entities, EntitySynchronizer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def ex1_print_a_trade_item():
    """Example 1: Print a known trade item using the old API style."""
    print("\n=== Example 1: Print a known trade item (old API style) ===\n")

    # Old API style using ApiFactory directly
    from floriday_supplier_client.api_factory import ApiFactory

    factory = ApiFactory()
    client = factory.get_api_client()
    api_instance = TradeItemsApi(client)

    api_response = api_instance.get_trade_items_summary(
        trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
    )
    pprint(api_response)


def ex2_print_a_trade_item_new_api():
    """Example 2: Print a known trade item using the new API style."""
    print("\n=== Example 2: Print a known trade item (new API style) ===\n")

    # New API style using the Floriday client
    with Floriday() as client:
        trade_items_api = client.get_api(TradeItemsApi)
        api_response = trade_items_api.get_trade_items_summary(
            trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
        )
        pprint(api_response)


# Example persistence functions for different entity types
def persist_trade_item(item):
    """Example persistence function for trade items."""
    print(
        f"Processing trade item: {item.trade_item_id} - {getattr(item, 'trade_item_name', 'N/A')}"
    )
    return item.trade_item_id


def persist_organization(org):
    """Example persistence function for organizations."""
    print(
        f"Processing organization: {org.organization_id} - {getattr(org, 'name', 'N/A')}"
    )
    return org.organization_id


def persist_supply_line(supply_line):
    """Example persistence function for supply lines."""
    print(
        f"Processing supply line: {supply_line.supply_line_id} - {getattr(supply_line, 'status', 'N/A')}"
    )
    return supply_line.supply_line_id


def ex3_sync_trade_items():
    """Example 3: Synchronize trade items using the unified API."""
    print("\n=== Example 3: Synchronize Trade Items ===\n")

    with Floriday() as client:
        # Get the trade items API
        trade_items_api = client.get_api(TradeItemsApi)

        # Synchronize trade items
        result = sync_entities(
            entity_type="trade_items",
            fetch_entities_callback=trade_items_api.get_trade_items_by_sequence_number,
            persist_entity_callback=persist_trade_item,
            start_seq_number=0,  # Start from the beginning
            batch_size=10,  # Process 10 items at a time
            rate_limit_delay=0.5,  # Wait 0.5 seconds between API calls
        )

        print(f"Trade Items Sync Result: {result}")


def ex4_sync_organizations_with_max_sequence():
    """Example 4: Synchronize organizations using max sequence number."""
    print("\n=== Example 4: Synchronize Organizations with Max Sequence ===\n")

    with Floriday() as client:
        # Get the organizations API
        organizations_api = client.get_api(OrganizationsApi)

        # Get the maximum sequence number
        max_seq = organizations_api.get_organizations_max_sequence()
        print(f"Maximum sequence number for organizations: {max_seq}")

        # This allows us to sync only the most recent organizations
        start_seq = max_seq - 100
        print(f"Starting synchronization from sequence number: {start_seq}")

        # Synchronize organizations from the calculated starting point
        result = sync_entities(
            entity_type="organizations",
            fetch_entities_callback=organizations_api.get_organizations_by_sequence_number,
            persist_entity_callback=persist_organization,
            start_seq_number=start_seq,
            batch_size=10,  # Process 10 items at a time
            rate_limit_delay=0.5,  # Wait 0.5 seconds between API calls
        )

        print(f"Organizations Sync Result: {result}")


def ex5_sync_supply_lines():
    """Example 5: Synchronize supply lines using the unified API."""
    print("\n=== Example 5: Synchronize Supply Lines ===\n")

    pass


def ex6_advanced_sync_with_context_manager():
    """Example 6: Advanced synchronization using EntitySynchronizer with context manager."""
    print("\n=== Example 6: Advanced Synchronization with Context Manager ===\n")

    with Floriday() as client:
        # Get the trade items API
        trade_items_api = client.get_api(TradeItemsApi)

        # Create a synchronizer with advanced options
        with EntitySynchronizer(
            entity_type="trade_items",
            fetch_entities_callback=trade_items_api.get_trade_items_by_sequence_number,
            persist_entity_callback=persist_trade_item,
            start_seq_number=0,  # Start from the beginning
            batch_size=20,  # Process 20 items at a time
            rate_limit_delay=0.2,  # Wait 0.2 seconds between API calls
        ) as synchronizer:
            # Configure event handlers
            synchronizer.on_batch_start = lambda seq: print(
                f"Starting batch at sequence {seq}"
            )
            synchronizer.on_batch_complete = lambda batch: print(
                f"Completed batch with {len(batch)} items"
            )

            # Execute the sync
            result = synchronizer.sync()
            print(f"Advanced Sync Result: {result}")


def ex7_sync_multiple_entity_types():
    """Example 7: Synchronize multiple entity types in sequence."""
    print("\n=== Example 7: Synchronize Multiple Entity Types ===\n")

    with Floriday() as client:
        # Synchronize trade items
        trade_items_api = client.get_api(TradeItemsApi)
        trade_items_result = sync_entities(
            entity_type="trade_items",
            fetch_entities_callback=trade_items_api.get_trade_items_by_sequence_number,
            persist_entity_callback=persist_trade_item,
            start_seq_number=0,
            batch_size=10,
        )
        print(f"Trade Items Sync Result: {trade_items_result}")

        # Synchronize organizations using max sequence number
        organizations_api = client.get_api(OrganizationsApi)

        # Get the maximum sequence number
        max_seq = organizations_api.get_organizations_max_sequence()
        print(f"Maximum sequence number for organizations: {max_seq}")

        # Calculate a starting point
        start_seq = int(max_seq - 100)
        print(
            f"Starting organizations synchronization from sequence number: {start_seq}"
        )

        organizations_result = sync_entities(
            entity_type="organizations",
            fetch_entities_callback=organizations_api.get_organizations_by_sequence_number,
            persist_entity_callback=persist_organization,
            start_seq_number=start_seq,
            batch_size=10,
        )
        print(f"Organizations Sync Result: {organizations_result}")


if __name__ == "__main__":
    # Choose which examples to run
    ex1_print_a_trade_item()
    ex2_print_a_trade_item_new_api()
    ex3_sync_trade_items()
    ex4_sync_organizations_with_max_sequence()
    ex5_sync_supply_lines()
    ex6_advanced_sync_with_context_manager()
    ex7_sync_multiple_entity_types()
