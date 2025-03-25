# Current API vs. Proposed Improvements

This document provides a side-by-side comparison of the current Floriday Supplier API Client with the proposed improvements.

## Client Initialization

### Current API
```python
factory = ApiFactory()
client = factory.get_api_client()
api_instance = TradeItemsApi(client)
```

### Proposed API
```python
# Option 1: Direct API class initialization
trade_items_api = Floriday(TradeItemsApi)
organizations_api = Floriday(OrganizationsApi)

# Option 2: Client with get_api method
client = Floriday()
trade_items_api = client.get_api(TradeItemsApi)
organizations_api = client.get_api(OrganizationsApi)
```

## Making API Calls

### Current API
```python
api_response = api_instance.get_trade_items_summary(
    trade_item_ids=["1987a15c-2c28-4ba6-89a1-3780e585b42c"]
)
```

### Proposed API
```python
# More intuitive method naming
trade_item = client.trade_items.get_by_id(
    "1987a15c-2c28-4ba6-89a1-3780e585b42c"
)
```

## Synchronization

### Current API
```python
# Function-based approach
result = sync_entities(
    entity_type="trade_items",
    fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
    persist_entity_callback=persist_item,
    start_seq_number=0,
)

# Context manager approach
with EntitySynchronizer(
    entity_type="trade_items",
    fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
    persist_entity_callback=persist_item,
    start_seq_number=0,
) as synchronizer:
    result = synchronizer.sync()
```

### Proposed API
```python
# Simple synchronization with callback
result = client.trade_items.sync(
    start_seq=0,
    on_item=persist_item,
    batch_size=50,
    rate_limit=0.5,
)

# Iterator pattern for memory efficiency
for item in client.trade_items.sync_iter(start_seq=last_seq):
    # Process each item individually
    db.save_trade_item(item)

# Advanced control
sync = client.trade_items.create_sync(start_seq=0)
sync.batch_size = 100
sync.rate_limit = 0.2
sync.on_batch_start = lambda seq: print(f"Starting batch at sequence {seq}")
sync.on_batch_complete = lambda batch: print(f"Completed batch with {len(batch)} items")
sync.on_item = persist_item
result = sync.execute()
```

## Error Handling

### Current API
```python
try:
    response = api_instance.get_trade_items()
except ApiException as e:
    print(f"API Exception: {e}")
```

### Proposed API
```python
try:
    items = client.trade_items.get_all(limit=10)
except AuthenticationError as e:
    print(f"Authentication error: {e}")
    client.refresh_token()  # Automatic token refresh
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after} seconds")
except ApiError as e:
    print(f"API Error: {e.status_code} - {e.message}")
    print(f"Request ID: {e.request_id}")  # For support reference
    
    if e.is_retryable:
        print("This error is retryable, implementing backoff...")
```

## Resource Management

### Current API
No explicit resource management. Resources are managed internally by the ApiClient.

### Proposed API
```python
# Context manager for automatic cleanup
with FloriDay() as client:
    items = client.trade_items.get_all(limit=10)

# Manual resource management
client = FloriDay()
try:
    items = client.trade_items.get_all(limit=10)
finally:
    client.close()  # Explicitly close resources
```

## Configuration Management

### Current API
Configuration is handled through environment variables only:
```python
# Environment variables required
# FLORIDAY_CLIENT_ID
# FLORIDAY_CLIENT_SECRET
# FLORIDAY_API_KEY
# FLORIDAY_AUTH_URL
# FLORIDAY_BASE_URL
```

### Proposed API
Multiple configuration options:
```python
# Environment variables (current approach)
client = FloriDay()

# Direct configuration
client = FloriDay(
    client_id="my_client_id",
    client_secret="my_client_secret",
    api_key="my_api_key",
    base_url="https://api.floriday.io/api/v1/"
)

# Configuration file
client = FloriDay.from_config("config.yaml")
```

## API Discoverability

### Current API
No built-in discovery mechanism. Developers need to refer to documentation.

### Proposed API
```python
# List available APIs
apis = client.available_apis()

# Get API documentation
help_text = client.trade_items.help()

# Discover methods on an API
methods = client.trade_items.available_methods()
```

## Type Hints and Documentation

### Current API
Limited type hints and documentation separate from code.

### Proposed API
Comprehensive type hints and inline documentation:
```python
def get_trade_items(
    self, 
    trade_item_ids: List[str] = None,
    limit: int = 50
) -> List[TradeItem]:
    """
    Get trade items by their IDs.
    
    Args:
        trade_item_ids: List of trade item IDs to retrieve
        limit: Maximum number of items to return
        
    Returns:
        List of TradeItem objects
        
    Example:
        ```python
        items = client.trade_items.get_trade_items(
            trade_item_ids=["id1", "id2"]
        )
        ```
    """
```

## Summary of Benefits

The proposed improvements offer several key benefits:

1. **Reduced Boilerplate**: Simplified client initialization and API access
2. **Improved Developer Experience**: More intuitive API design and method naming
3. **Flexible Configuration**: Multiple ways to configure the client
4. **Better Error Handling**: Specific exception types and more context in errors
5. **Resource Management**: Explicit control over resources with context managers
6. **API Discoverability**: Built-in mechanisms to discover available APIs and methods
7. **Comprehensive Type Hints**: Better IDE support and code completion
8. **Unified Synchronization API**: Consistent API for synchronization with multiple patterns
9. **Documentation**: Inline documentation with examples

These improvements would make the Floriday Supplier API Client more intuitive, efficient, and developer-friendly while maintaining compatibility with the existing codebase.
