# coding: utf-8

"""
Tests for the entity_sync module.
"""

import pytest
from unittest.mock import Mock, patch

from floriday_supplier_client.sync.entity_sync import sync_entities


class MockEntity:
    """Mock entity for testing."""

    def __init__(self, id, sequence_number):
        self.id = id
        self.sequence_number = sequence_number


class MockApiSyncResult:
    """Mock ApiSyncResult for testing."""

    def __init__(self, maximum_sequence_number, results):
        self._maximum_sequence_number = maximum_sequence_number
        self._results = results

    @property
    def maximum_sequence_number(self):
        return self._maximum_sequence_number

    @property
    def results(self):
        return self._results


@patch("time.sleep")  # Mock sleep to speed up tests
def test_sync_entities_basic(mock_sleep):
    """Test basic functionality of sync_entities."""
    # Setup test data
    entity_type = "test_entity"

    # Create mock entities with sequence numbers
    entities_batch1 = [MockEntity(f"id_{i}", i) for i in range(1, 6)]
    entities_batch2 = [MockEntity(f"id_{i}", i) for i in range(6, 11)]

    # Create mock sync results
    result1 = MockApiSyncResult(5, entities_batch1)
    result2 = MockApiSyncResult(10, entities_batch2)
    # Final result with no new entities and same max sequence number to signal end of sync
    result3 = MockApiSyncResult(10, [])

    # Mock fetch_entities_callback function
    mock_fetch_entities = Mock()
    mock_fetch_entities.side_effect = [result1, result2, result3]

    # Mock persist_entity_callback function
    mock_persist_entity = Mock()
    mock_persist_entity.side_effect = lambda entity: entity.id

    # Call sync_entities
    result = sync_entities(
        entity_type=entity_type,
        fetch_entities_callback=mock_fetch_entities,
        persist_entity_callback=mock_persist_entity,
        start_seq_number=0,
    )

    # Verify results
    assert result.entity_type == entity_type
    assert result.start_sequence_number == 0
    assert result.end_sequence_number == 10
    assert result.entities_processed == 10
    assert result.success is True

    # Verify mock calls
    assert mock_fetch_entities.call_count == 3
    mock_fetch_entities.assert_any_call(sequence_number=0, limit_result=50)
    mock_fetch_entities.assert_any_call(sequence_number=5, limit_result=50)
    mock_fetch_entities.assert_any_call(sequence_number=10, limit_result=50)

    assert mock_persist_entity.call_count == 10
    for entity in entities_batch1 + entities_batch2:
        mock_persist_entity.assert_any_call(entity)

    # Verify sleep was called for rate limiting
    mock_sleep.assert_called_with(0.5)


@patch("time.sleep")  # Mock sleep to speed up tests
def test_sync_entities_with_custom_config(mock_sleep):
    """Test sync_entities with custom batch size and rate limit delay."""
    # Setup test data
    entity_type = "test_entity"
    custom_batch_size = 25
    custom_rate_limit_delay = 1.0

    # Create mock entities with sequence numbers
    entities = [MockEntity(f"id_{i}", i) for i in range(1, 6)]

    # Create mock sync results - need two results to complete the sync
    # First result with entities, second with same max sequence to signal end
    result1 = MockApiSyncResult(5, entities)
    result2 = MockApiSyncResult(
        5, []
    )  # Empty result with same max sequence to end sync

    # Mock fetch_entities_callback function
    mock_fetch_entities = Mock()
    mock_fetch_entities.side_effect = [result1, result2]

    # Call sync_entities with custom configuration
    sync_entities(
        entity_type=entity_type,
        fetch_entities_callback=mock_fetch_entities,
        start_seq_number=0,
        batch_size=custom_batch_size,
        rate_limit_delay=custom_rate_limit_delay,
    )

    # Verify custom batch size was used
    mock_fetch_entities.assert_any_call(
        sequence_number=0, limit_result=custom_batch_size
    )

    # Verify custom rate limit delay was used
    mock_sleep.assert_called_with(custom_rate_limit_delay)


def test_sync_entities_no_persistence():
    """Test sync_entities without persistence."""
    # Setup test data
    entity_type = "test_entity"

    # Create mock entities with sequence numbers
    entities = [MockEntity(f"id_{i}", i) for i in range(1, 6)]

    # Create mock sync result
    result = MockApiSyncResult(5, entities)

    # Mock fetch_entities_callback function
    mock_fetch_entities = Mock()
    mock_fetch_entities.return_value = result

    # Call sync_entities without persist_entity_callback
    with patch("time.sleep"):  # Mock sleep to speed up tests
        sync_result = sync_entities(
            entity_type=entity_type,
            fetch_entities_callback=mock_fetch_entities,
            start_seq_number=0,
        )

    # Verify results
    assert sync_result.entities_processed == 5
    assert sync_result.success is True


def test_sync_entities_with_get_max_sequence_number():
    """Test sync_entities with get_max_sequence_number."""
    # Setup test data
    entity_type = "test_entity"

    # Create mock entities with sequence numbers
    entities = [MockEntity(f"id_{i}", i) for i in range(101, 106)]

    # Create mock sync result
    result = MockApiSyncResult(105, entities)

    # Mock fetch_entities_callback function
    mock_fetch_entities = Mock()
    mock_fetch_entities.return_value = result

    # Mock get_max_sequence_number function
    mock_get_max_sequence_number = Mock()
    mock_get_max_sequence_number.return_value = 100

    # Call sync_entities with get_max_sequence_number
    with patch("time.sleep"):  # Mock sleep to speed up tests
        sync_result = sync_entities(
            entity_type=entity_type,
            fetch_entities_callback=mock_fetch_entities,
            get_max_sequence_number=mock_get_max_sequence_number,
        )

    # Verify results
    assert sync_result.start_sequence_number == 100
    assert sync_result.entities_processed == 5
    assert sync_result.success is True

    # Verify get_max_sequence_number was called
    mock_get_max_sequence_number.assert_called_once_with(entity_type)


def test_sync_entities_logging():
    """Test that sync_entities logs correctly."""
    # Setup test data
    entity_type = "test_entity"

    # Create mock entities with sequence numbers
    entities = [MockEntity(f"id_{i}", i) for i in range(1, 3)]

    # Create mock sync result
    result = MockApiSyncResult(2, entities)

    # Mock fetch_entities_callback function
    mock_fetch_entities = Mock()
    mock_fetch_entities.return_value = result

    # Call sync_entities with mocked logger
    with patch("time.sleep"), patch(
        "floriday_supplier_client.sync.entity_sync.logger"
    ) as mock_logger:
        sync_entities(
            entity_type=entity_type,
            fetch_entities_callback=mock_fetch_entities,
            start_seq_number=0,
        )

    # Verify logger was called at least once for each level
    assert mock_logger.info.call_count > 0
    assert mock_logger.debug.call_count > 0


def test_sync_entities_error_handling():
    """Test sync_entities error handling."""
    # Setup test data
    entity_type = "test_entity"

    # Mock fetch_entities_callback function that raises an exception
    mock_fetch_entities = Mock()
    mock_fetch_entities.side_effect = Exception("Test error")

    # Call sync_entities with mocked logger
    with patch("time.sleep"), patch(
        "floriday_supplier_client.sync.entity_sync.logger"
    ) as mock_logger:
        result = sync_entities(
            entity_type=entity_type,
            fetch_entities_callback=mock_fetch_entities,
            start_seq_number=0,
        )

    # Verify results
    assert result.entity_type == entity_type
    assert result.start_sequence_number == 0
    assert result.entities_processed == 0
    assert result.success is False
    assert result.error == "Test error"

    # Verify error was logged
    assert mock_logger.error.call_count > 0


def test_sync_entities_missing_parameters():
    """Test sync_entities with missing parameters."""
    # Setup test data
    entity_type = "test_entity"
    mock_fetch_entities = Mock()

    # Call sync_entities without start_seq_number or get_max_sequence_number
    with pytest.raises(ValueError) as excinfo:
        sync_entities(
            entity_type=entity_type, fetch_entities_callback=mock_fetch_entities
        )

    # Verify error message
    assert "Either start_seq_number or get_max_sequence_number must be provided" in str(
        excinfo.value
    )


def test_entity_sync_result_str_method():
    """Test the __str__ method of EntitySyncResult."""
    from floriday_supplier_client.sync.entity_sync import EntitySyncResult

    # Test successful result
    success_result = EntitySyncResult(
        entity_type="test_entity",
        start_sequence_number=100,
        end_sequence_number=200,
        entities_processed=50,
        success=True,
    )

    success_str = str(success_result)
    assert "SUCCESS" in success_str
    assert "test_entity" in success_str
    assert "50 entities" in success_str
    assert "100 → 200" in success_str

    # Test failed result
    error_result = EntitySyncResult(
        entity_type="test_entity",
        start_sequence_number=100,
        end_sequence_number=150,
        entities_processed=25,
        success=False,
        error="Connection error",
    )

    error_str = str(error_result)
    assert "FAILED" in error_str
    assert "test_entity" in error_str
    assert "25 entities" in error_str
    assert "100 → 150" in error_str
    assert "Connection error" in error_str
