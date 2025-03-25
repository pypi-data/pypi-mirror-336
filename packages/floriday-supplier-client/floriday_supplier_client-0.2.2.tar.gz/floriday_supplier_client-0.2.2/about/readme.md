# Floriday Supplier API Client

A Python client for interacting with the Floriday Supplier API. This client provides a clean, type-safe interface to Floriday's supplier endpoints.

## Overview

This client library is automatically generated from the Floriday Supplier API OpenAPI/Swagger specification using Swagger Codegen. It provides Python developers with a convenient way to interact with Floriday's supplier services.

## Features

- Auto-generated API client from Swagger/OpenAPI specs
- Type-safe API interactions
- Comprehensive API coverage for supplier operations
- Environment-based configuration
- OAuth2 authentication handling
- Support for all Floriday Supplier API endpoints
- Entity synchronization utilities for efficient data retrieval

## Installation

### Requirements

- Python 3.4+ (developed and tested with Python 3.12)
- Required Python packages (automatically installed as dependencies):
  - requests
  - urllib3
  - certifi
  - six

### Installation Methods

#### From GitHub

```sh
pip install git+https://github.com/serraict/vine-floriday-python-supplier-api-client
```

#### Using Setuptools

```sh
python setup.py install --user
```

Or for all users:

```sh
sudo python setup.py install
```

## Configuration

The client requires several environment variables to be set for authentication and API access:

| Variable | Description |
|----------|-------------|
| FLORIDAY_CLIENT_ID | OAuth client ID |
| FLORIDAY_CLIENT_SECRET | OAuth client secret |
| FLORIDAY_API_KEY | API key for Floriday API |
| FLORIDAY_AUTH_URL | Authentication server URL |
| FLORIDAY_BASE_URL | Base URL for API requests |

See `.env.example` in the repository root for a template.

## Basic Usage

### Direct API Access

```python
from floriday_supplier_client import TradeItemsApi
from floriday_supplier_client.api_factory import ApiFactory
from floriday_supplier_client.rest import ApiException

# Create API factory and client
factory = ApiFactory()
client = factory.get_api_client()

# Initialize specific API instance
api_instance = TradeItemsApi(client)

try:
    # Call API methods
    response = api_instance.get_trade_items_summary(
        trade_item_ids=["your-trade-item-id"]
    )
    print(response)
    
except ApiException as e:
    print(f"API Exception: {e}")
```

### Entity Synchronization

The client includes utilities for efficiently synchronizing entities from the Floriday API:

```python
from floriday_supplier_client import TradeItemsApi
from floriday_supplier_client.api_factory import ApiFactory
from floriday_supplier_client.sync import sync_entities

# Create API factory and client
factory = ApiFactory()
client = factory.get_api_client()
api_instance = TradeItemsApi(client)

# Define a persistence function
def persist_trade_item(item):
    # In a real application, save to database
    print(f"Processing trade item: {item.trade_item_id}")
    return item.trade_item_id

# Synchronize trade items
result = sync_entities(
    entity_type="trade_items",
    fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
    persist_entity_callback=persist_trade_item,
    start_seq_number=0
)

# Handle the result
print(f"Processed {result.entities_processed} trade items")
if not result.success:
    print(f"Error: {result.error}")
```

## Documentation

- API endpoint documentation is available in the `docs/` directory
- Example usage can be found in `example.py`
- For architecture details, see [architecture.md](architecture.md)

## Development

All code in `floriday_supplier_client` and `test` directories is generated. Files that should not be overwritten on generation should be included in `.swagger-codegen-ignore`.

To regenerate the client:

```bash
make local_specs  # get a local copy of the swagger specification
make client       # generate the client
```

For development and testing:

```bash
make bootstrap
./venv/bin/activate
make update
python example.py
