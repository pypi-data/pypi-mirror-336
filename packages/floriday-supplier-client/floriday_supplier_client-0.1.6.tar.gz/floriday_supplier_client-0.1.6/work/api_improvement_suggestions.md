# API Improvement Suggestions

After analyzing the Floriday Supplier API Client from a developer's perspective, I've identified several areas where the API could be improved to make it more intuitive, efficient, and developer-friendly.

## Current API Usage (from example.py)

The current API usage pattern requires:
1. Creating an ApiFactory
2. Getting an ApiClient
3. Initializing a specific API instance
4. Making API calls

For synchronization, there are two approaches:
1. Function-based with `sync_entities`
2. Context manager-based with `EntitySynchronizer`

## Improvement Suggestions

### 1. Simplified Client Initialization

**Current approach:**
```python
factory = ApiFactory()
client = factory.get_api_client()
api_instance = TradeItemsApi(client)
```

**Suggested improvement:**
```python
# Option 1: Direct API class initialization, create a client implicitly (what to do about resource mngmt)
trade_items_api = floriday(TradeItemsApi)
organizations_api = floriday(OrganizationsApi)

# Option 2: Client with get_api method
client = Floriday()
trade_items_api = client.get_api(TradeItemsApi)
organizations_api = client.get_api(OrganizationsApi)
```

This would reduce boilerplate and make the API more intuitive to use. Option 1 is particularly elegant for single API use cases, while Option 2 is more efficient when working with multiple APIs.

### 2. Configuration Management

**Current approach:**
- Relies solely on environment variables
- No way to override configuration at runtime
- No configuration validation until runtime errors occur

**Suggested improvements:**
- Allow passing configuration directly to the client

```python
# Environment variables (current approach)
client = Floriday()

# Direct configuration
client = Floriday(
    client_id="my_client_id",
    client_secret="my_client_secret",
    api_key="my_api_key",
    base_url="https://api.floriday.io/api/v1/"
)
```

### 3. Unified Synchronization API

**Current approach:**
- Two different approaches (function and class-based)
- Requires callbacks for persistence
- Limited control over synchronization process

**Suggested improvements:**
- Provide a single, consistent synchronization API
- Support both callback and iterator patterns
- Add more control over the synchronization process
- Simplify common use cases

```python
# Simple synchronization (returns all entities)
items = client.trade_items.sync_all()

# Iterator pattern for memory efficiency
for item in client.trade_items.sync_iter(start_seq=last_seq):
    # Process each item
    db.save(item)

# Callback pattern (current approach, but simplified)
result = client.trade_items.sync(
    start_seq=last_seq,
    on_item=lambda item: db.save(item)
)

# Advanced control
sync = client.trade_items.create_sync(start_seq=last_seq)
sync.batch_size = 100
sync.rate_limit = 0.2  # seconds
sync.on_batch_complete = lambda batch: print(f"Processed {len(batch)} items")
result = sync.execute()
```

### 4. Resource Management

**Current approach:**
- No clear way to manage resources
- Authentication token management is hidden

**Suggested improvements:**
- Add explicit session management
- Provide token refresh handling
- Support connection pooling
- Add cleanup methods

```python
# Context manager for automatic resource cleanup
with Floriday() as client:
    items = client.trade_items.get_all()

# Explicit session management
client = Floriday()
client.start_session()
try:
    # Use client
finally:
    client.close_session()

# Token management
client.refresh_token()
```

## Future Improvements

The following improvements are marked for future implementation:

### 1. Advanced Configuration Management

- Support configuration files (e.g., YAML, JSON)
- Provide configuration validation
- Add a configuration builder pattern

### 2. Improved Error Handling

- Add specific exception types for different error categories
- Implement automatic retry for transient errors
- Provide more context in error messages
- Add request/response logging for debugging

```python
try:
    response = client.trade_items.get_by_id("item_id")
except AuthenticationError as e:
    # Handle authentication issues
except RateLimitError as e:
    # Handle rate limiting
    print(f"Rate limited, retry after: {e.retry_after}")
except ApiError as e:
    # Handle other API errors
    print(f"API Error: {e.status_code} - {e.message}")
    print(f"Request ID: {e.request_id}")  # For support reference
```

### 3. API Discoverability

- Add methods to discover available APIs
- Provide introspection capabilities
- Add helper methods for common operations

```python
# List available APIs
apis = client.available_apis()
print(apis)  # ['trade_items', 'sales_orders', ...]

# Get API documentation
help_text = client.trade_items.help()
print(help_text)

# Discover methods on an API
methods = client.trade_items.available_methods()
print(methods)  # ['get_by_id', 'get_all', ...]
```

### 4. Type Hints and Documentation

- Add comprehensive type hints for better IDE support
- Ensure all methods have proper docstrings
- Add examples in docstrings
- Support runtime type checking

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
    ...
```

### 5. Testing and Mocking

- Add a mock client for testing
- Provide request/response recording for tests
- Add fixtures for common test scenarios

```python
# Create a mock client for testing
mock_client = Floriday.mock()
mock_client.trade_items.get_by_id.return_value = TradeItem(id="test")

# Record and replay API interactions
with Floriday.record("test_session.json"):
    items = client.trade_items.get_all()

# Replay recorded session
with Floriday.replay("test_session.json") as client:
    items = client.trade_items.get_all()  # Uses recorded data
```

### 6. Pagination and Filtering

- Add consistent pagination across all APIs
- Support for filtering and sorting
- Provide helper methods for common queries

```python
# Pagination
page1 = client.trade_items.get_page(page=1, size=50)
page2 = client.trade_items.get_page(page=2, size=50)

# Automatic pagination
all_items = client.trade_items.get_all(batch_size=50)

# Filtering
filtered = client.trade_items.filter(
    status="active",
    created_after="2023-01-01"
)

# Sorting
sorted_items = client.trade_items.get_all(
    sort_by="created_at",
    sort_order="desc"
)
```

### 7. Async Support

- Add async versions of all APIs
- Support for concurrent operations
- Non-blocking I/O

```python
# Async client
async_client = Floriday.async_client()

# Async API calls
async def get_items():
    items = await async_client.trade_items.get_all()
    return items

# Concurrent operations
async def get_multiple_resources():
    items, orders = await asyncio.gather(
        async_client.trade_items.get_all(),
        async_client.sales_orders.get_all()
    )
    return items, orders
```

## Implementation Priority

Based on developer impact and implementation complexity:

1. **Simplified Client Initialization** - High impact, low complexity
2. **Configuration Management** - High impact, medium complexity
3. **Unified Synchronization API** - High impact, medium complexity
4. **Resource Management** - Medium impact, medium complexity
5. **Improved Error Handling** - High impact, medium complexity (future)
6. **Type Hints and Documentation** - Medium impact, low complexity (future)
7. **API Discoverability** - Medium impact, low complexity (future)
8. **Pagination and Filtering** - Medium impact, medium complexity (future)
9. **Testing and Mocking** - Medium impact, high complexity (future)
10. **Async Support** - High impact, high complexity (future)

## Conclusion

The current Floriday Supplier API Client provides a solid foundation, but implementing these improvements would significantly enhance developer experience, code quality, and maintainability. The suggested changes follow modern Python best practices and would make the API more intuitive and easier to use.
