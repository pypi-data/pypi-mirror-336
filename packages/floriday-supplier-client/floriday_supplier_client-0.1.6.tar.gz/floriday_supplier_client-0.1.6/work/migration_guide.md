# Migration Guide: Sync Module

This guide provides instructions on migrating from the sync functionality in vine-floriday-adapter to the new sync module in floriday-supplier-client.

## Background

The generic entity synchronization code has been moved from vine-floriday-adapter to floriday-supplier-client to make it available for other projects using the client library. The new implementation includes several improvements:

- More Pythonic with type hints
- Proper error handling
- Configurable rate limiting
- Optional in-memory tracking
- Logging instead of print statements
- Comprehensive docstrings and examples
- Class-based approach with EntitySynchronizer
- Context manager support

## Migration Steps

1. **Update Dependencies**

   Ensure you're using the latest version of floriday-supplier-client:

   ```bash
   pip install --upgrade floriday-supplier-client
   ```

2. **Import Changes**

   Old imports:
   ```python
   from vine_floriday_adapter.sync import sync_entities
   ```

   New imports:
   ```python
   from floriday_supplier_client.sync import sync_entities, EntitySynchronizer
   ```

3. **Function Signature Changes**

   The new sync_entities function has an improved signature with better parameter names and additional options:

   Old:
   ```python
   sync_entities(
       entity_type,
       get_entities_by_sequence_number,
       persist_entity,
       get_max_sequence_number=None,
       start_seq_number=None
   )
   ```

   New:
   ```python
   sync_entities(
       entity_type,
       fetch_entities_callback,
       persist_entity_callback=None,  # Now optional
       start_seq_number=None,
       get_max_sequence_number=None,
       batch_size=50,                 # New parameter
       rate_limit_delay=0.5           # New parameter
   )
   ```

4. **Return Value Changes**

   Old: Dictionary with sync statistics
   ```python
   {
       'entity_type': 'trade_items',
       'start_sequence_number': 0,
       'end_sequence_number': 100,
       'entities_processed': 50,
       'success': True
   }
   ```

   New: EntitySyncResult object with the same fields plus string representation
   ```python
   result = sync_entities(...)
   print(result)  # Prints a human-readable summary
   print(result.entities_processed)  # Access individual fields
   ```

5. **Advanced Usage with EntitySynchronizer**

   For more control, you can use the new class-based approach:

   ```python
   with EntitySynchronizer(
       entity_type='trade_items',
       fetch_entities_callback=api.get_trade_items_by_sequence_number,
       persist_entity_callback=persist_item,
       start_seq_number=0,
       batch_size=100,
       rate_limit_delay=0.2
   ) as synchronizer:
       result = synchronizer.sync()
   ```

6. **Error Handling**

   The new implementation provides more detailed error information:

   ```python
   result = sync_entities(...)
   if not result.success:
       print(f'Error: {result.error}')
       # Resume from where it failed
       new_result = sync_entities(
           ...,
           start_seq_number=result.end_sequence_number
       )
   ```

## Example Migration

Before:
```python
from vine_floriday_adapter.sync import sync_entities

def sync_trade_items():
    result = sync_entities(
        'trade_items',
        api.get_trade_items_by_sequence_number,
        db.save_trade_item,
        get_max_sequence_number=db.get_max_sequence_number
    )
    print(f'Processed {result["entities_processed"]} items')
```

After:
```python
from floriday_supplier_client.sync import sync_entities

def sync_trade_items():
    result = sync_entities(
        entity_type='trade_items',
        fetch_entities_callback=api.get_trade_items_by_sequence_number,
        persist_entity_callback=db.save_trade_item,
        get_max_sequence_number=db.get_max_sequence_number,
        batch_size=50,
        rate_limit_delay=0.5
    )
    print(result)  # Human-readable summary
```

## Additional Resources

- See the [example.py](https://github.com/serraict/vine-floriday-python-supplier-api-client/blob/main/example.py) file for more usage examples
- Check the docstrings in the [entity_sync.py](https://github.com/serraict/vine-floriday-python-supplier-api-client/blob/main/floriday_supplier_client/sync/entity_sync.py) module for detailed API documentation
