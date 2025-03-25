# Architecture

## Overview

The Floriday Supplier API Client is a Python library that provides a structured interface to the Floriday Supplier API. It is built using Swagger Codegen to generate type-safe API clients from the OpenAPI specification.

## System Components

```text
┌─────────────────────────────────────────────────────────────┐
│                  Floriday Supplier API Client                │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ ApiFactory  │───▶│ ApiClient   │───▶│ API Endpoints   │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│        │                                        │           │
│        ▼                                        ▼           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │ Auth Flow   │    │ Sync Module │    │ API Models      │  │
│  └─────────────┘    └─────────────┘    └─────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            │                               │
            ▼                               ▼
┌─────────────────────┐         ┌─────────────────────────┐
│ OAuth2 Auth Server  │         │ Floriday Supplier API   │
└─────────────────────┘         └─────────────────────────┘
```

### 1. ApiFactory

The `ApiFactory` class is the entry point for client configuration and instantiation. It handles:

- Environment variable loading
- OAuth2 authentication
- Client configuration
- API client instantiation

```python
class ApiFactory:
    def __init__(self):
        # Load configuration from environment variables
        self.client_id = os.getenv("FLORIDAY_CLIENT_ID")
        self.client_secret = os.getenv("FLORIDAY_CLIENT_SECRET")
        self.api_key = os.getenv("FLORIDAY_API_KEY")
        self.auth_url = os.getenv("FLORIDAY_AUTH_URL")
        self.base_url = os.getenv("FLORIDAY_BASE_URL")
        
        # Get access token and configure client
        self.access_token = self._get_access_token()
        self.configuration = self._configure_client()
    
    # Methods for authentication and client creation
    def get_api_client(self):
        return floriday_supplier_client.ApiClient(self.configuration)
    
    def get_api_instance(self, api_class):
        return api_class(self.get_api_client())
```

### 2. API Clients

The library provides specialized API clients for each endpoint group in the Floriday Supplier API:

- TradeItemsApi
- SalesOrdersApi
- BatchesApi
- ContractsApi
- And many others...

Each API client provides methods corresponding to the API endpoints, with proper parameter typing and error handling.

### 3. Sync Module

The `sync` module provides utilities for synchronizing entities from the Floriday API using sequence numbers. It handles pagination, rate limiting, and error handling to provide a robust synchronization mechanism.

#### Key Components

- `EntitySyncResult`: A data class that represents the result of a synchronization operation
- `sync_entities`: A function that synchronizes entities from the Floriday API

```python
from floriday_supplier_client import TradeItemsApi
from floriday_supplier_client.api_factory import ApiFactory
from floriday_supplier_client.sync import sync_entities

# Initialize API
factory = ApiFactory()
client = factory.get_api_client()
api_instance = TradeItemsApi(client)

# Define a persistence function
def persist_item(item):
    # Save the item to your database
    print(f"Persisting item: {item.trade_item_id}")
    return item.trade_item_id

# Synchronize trade items
result = sync_entities(
    entity_type="trade_items",
    fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
    persist_entity_callback=persist_item,
    start_seq_number=0
)

# Handle the result
print(f"Processed {result.entities_processed} entities")
print(f"Success: {result.success}")
```

#### Features

- **Sequence-based synchronization**: Efficiently retrieve only new or updated entities
- **Configurable rate limiting**: Avoid API throttling with customizable delay between requests
- **Optional persistence**: Integrate with any storage system through callback functions
- **Resumable synchronization**: Continue from where a previous sync left off
- **Comprehensive error handling**: Detailed error information and logging

### 4. Authentication Flow

The client uses OAuth2 client credentials flow for authentication:

1. `ApiFactory` requests an access token from the authentication server
2. The token is added to the API client configuration
3. All subsequent API requests include the token in the Authorization header
4. The API key is included in the X-Api-Key header for all requests

## Configuration

The client is configured through environment variables:

| Variable | Purpose |
|----------|---------|
| FLORIDAY_CLIENT_ID | OAuth client ID for authentication |
| FLORIDAY_CLIENT_SECRET | OAuth client secret for authentication |
| FLORIDAY_API_KEY | API key for request authorization |
| FLORIDAY_AUTH_URL | Authentication server URL |
| FLORIDAY_BASE_URL | Base URL for API requests |

## Integration Patterns

### Entity Synchronization Pattern

For synchronizing entities from the Floriday API:

```python
# 1. Create factory and client
factory = ApiFactory()
client = factory.get_api_client()

# 2. Initialize specific API
api_instance = TradeItemsApi(client)

# 3. Define persistence function
def persist_entity(entity):
    # Save entity to database
    return entity.id

# 4. Get last processed sequence number (optional)
def get_max_sequence_number(entity_type):
    # Retrieve from database
    return last_sequence_number

# 5. Synchronize entities
result = sync_entities(
    entity_type="trade_items",
    fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
    persist_entity_callback=persist_entity,
    get_max_sequence_number=get_max_sequence_number
)

# 6. Handle result
if result.success:
    print(f"Successfully processed {result.entities_processed} entities")
else:
    print(f"Sync failed: {result.error}")
```

### Basic Usage Pattern

```python
# 1. Create factory and client
factory = ApiFactory()
client = factory.get_api_client()

# 2. Initialize specific API
api_instance = TradeItemsApi(client)

# 3. Make API calls
try:
    response = api_instance.get_trade_items()
    # Process response
except ApiException as e:
    # Handle error
```

### Factory Helper Method

For convenience, the ApiFactory provides a helper method to create API instances:

```python
factory = ApiFactory()
api_instance = factory.get_api_instance(TradeItemsApi)
```

## Error Handling

The client uses the `ApiException` class for error handling:

```python
try:
    # API call
    response = api_instance.get_trade_items()
except ApiException as e:
    # Access error details
    status_code = e.status
    reason = e.reason
    body = e.body
```

## Development and Maintenance

The client is generated using Swagger Codegen. To update the client:

1. Update the local copy of the Swagger specification:

   ```bash
   make local_specs
   ```

2. Regenerate the client:

   ```bash
   make client
   ```

Custom code that should not be overwritten during regeneration should be added to the `.swagger-codegen-ignore` file.
