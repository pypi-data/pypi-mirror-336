# Doing

Issue reference on Github: https://github.com/serraict/vine-floriday-python-supplier-api-client/issues/3

## Goal

Move the generic entity synchronization code from vine-floriday-adapter to floriday-supplier-client to make it available for other projects using the client library.

The API should be intuitive to new developers and help to quickly write clean code.

## Analysis

The current situation:

- Generic sync code exists in vine-floriday-adapter's sync.py
- The code provides a reusable pattern for synchronizing Floriday entities using sequence numbers
- Key components:
  - `sync_entities` function that handles the synchronization workflow
  - Takes callbacks for entity-specific operations (get_by_sequence, persist_entity)
  - Manages pagination and sequence number tracking
  - Includes basic rate limiting (0.5s sleep between requests)
- The code is independent of vine-floriday-adapter specific concerns
- Current implementation relies on external persistence layer through get_max_sequence_number

## Design

Proposed solution:

1. Create a new module in floriday-supplier-client for synchronization:

   ```python
   floriday_supplier_client/
   └── sync/
       ├── __init__.py
       └── entity_sync.py  # Contains the sync functionality
   ```

2. Enhance the sync_entities function:
   - Make it more Pythonic with type hints
   - Add proper error handling
   - Make rate limiting configurable
   - Make persistence optional (allow in-memory tracking)
   - Add logging instead of print statements
   - Add docstrings and examples

3. Add tests:
   - Unit tests for sync logic
   - Integration tests with mock API responses
   - Example usage in documentation

4. Update documentation:
   - Add sync module documentation
   - Include example usage
   - Document configuration options

## Steps

1. Minimal sync implementation with fixed rate limiting and batch size
2. Add logging
3. Add configuration options for rate limiting and batch size
4. Update documentation:
   - Add docstring examples showing how to resume a failed sync
   - Document the error handling approach (why we don't need retry logic)
   - Add example usage in README.md or about/readme.md
   - Consider adding architecture documentation in about/architecture.md
5. Refactor API for better usability:
   - Use data classes for return values instead of dictionaries ✓
   - Improve parameter names to be more descriptive ✓
   - Add to string method to sync result ✓
   - Consider a class-based approach for complex use cases
   - Add context manager support for sync sessions
   - Add async support for modern Python applications
   - Provide simplified helper functions for common scenarios
   - Consider using a generator pattern for large datasets
6. Create issue in vine-floriday-adapter project:
   - Document how to migrate to the new sync function
   - Provide example code showing the migration path
   - Include any breaking changes and required updates
   - Include error handling recommendations

## Progress

- [x] Step 1: Minimal sync implementation
- [x] Step 2: Add logging
- [x] Step 3: Add configuration options
- [x] Step 4: Update documentation
- [x] Step 5: Refactor API (initial improvements)
- [x] Step 5: Refactor API (advanced features - partial)
  - [x] Add class-based approach with EntitySynchronizer
  - [x] Add context manager support for sync sessions
  - [ ] (not now) Add generator pattern for large datasets (planned in issue #5)
  - [ ] (not now) Add async support for modern Python applications (planned in issue #5)
- [x] Step 6: Implement API improvement suggestions (see work/api_improvement_suggestions.md and work/api_comparison.md)
  - [x] Simplified Client Initialization
  - [x] Configuration Management
  - [x] Unified Synchronization API
  - [x] Resource Management
- [x] Step 7: Create migration guide (see work/migration_guide.md)

Note: After analysis, we decided to skip implementing retry logic since the current implementation already handles failures gracefully by:

1. Returning the last successful sequence number in the result
2. Logging errors with details
3. Allowing syncs to resume from a specific sequence number using start_seq_number

We've also decided to implement the generator pattern and async support in a future update, as documented in GitHub issue #5.
