# coding: utf-8

"""
Entity synchronization utilities for Floriday Supplier API Client.

This module provides tools for synchronizing entities from the Floriday API
using sequence numbers.
"""

import logging
import time
from dataclasses import dataclass
from typing import (
    TypeVar,
    Generic,
    Callable,
    List,
    Optional,
    Any,
    Protocol,
    Dict,
)

# Configure logger
logger = logging.getLogger(__name__)

# Type variables for generic typing
T = TypeVar("T")

# Rate limiting constants
# Floriday API rate limits (as per documentation)
FLORIDAY_RATE_LIMIT_CALLS_PER_SECOND = 3.4  # 204 per minute
FLORIDAY_RATE_LIMIT_BURST_LIMIT = 1000

# Default conservative rate limit used by this module
DEFAULT_RATE_LIMIT_DELAY = 0.5  # seconds between calls (2 calls/second)
DEFAULT_BATCH_SIZE = 50


class ApiSyncResult(Protocol, Generic[T]):
    """Protocol defining the structure of a SyncResult object returned by Floriday API."""

    @property
    def maximum_sequence_number(self) -> int:
        """Gets the maximum sequence number in this result set."""
        ...

    @property
    def results(self) -> List[T]:
        """Gets the list of entities in this result set."""
        ...


@dataclass
class EntitySyncResult:
    """Result of a sync_entities operation."""

    entity_type: str
    """The type of entity that was synchronized."""

    start_sequence_number: int
    """The sequence number the sync started from."""

    end_sequence_number: int
    """The highest sequence number processed."""

    entities_processed: int
    """The number of entities processed during the sync."""

    success: bool
    """Whether the sync completed successfully."""

    error: Optional[str] = None
    """Error message if success is False, None otherwise."""

    def __str__(self) -> str:
        """Return a human-readable string representation of the sync result."""
        if self.success:
            return (
                f"Sync of {self.entity_type}: SUCCESS\n"
                f"Processed {self.entities_processed} entities\n"
                f"Sequence range: {self.start_sequence_number} → {self.end_sequence_number}"
            )
        else:
            return (
                f"Sync of {self.entity_type}: FAILED\n"
                f"Processed {self.entities_processed} entities before failure\n"
                f"Sequence range: {self.start_sequence_number} → {self.end_sequence_number}\n"
                f"Error: {self.error}"
            )


def sync_entities(
    entity_type: str,
    fetch_entities_callback: Callable[[int, int], ApiSyncResult[T]],
    persist_entity_callback: Optional[Callable[[T], Any]] = None,
    start_seq_number: Optional[int] = None,
    get_max_sequence_number: Optional[Callable[[str], int]] = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
) -> EntitySyncResult:
    """Synchronize entities from Floriday API using sequence numbers.

    Args:
        entity_type: A string identifier for the type of entity being synchronized.
        fetch_entities_callback: A function that retrieves entities by sequence number.
            It should accept a sequence number and limit, and return an ApiSyncResult.
        persist_entity_callback: Optional function to persist each entity. If None, entities
            will not be persisted.
        start_seq_number: Optional starting sequence number. If None and get_max_sequence_number
            is provided, it will be used to retrieve the starting sequence number.
        get_max_sequence_number: Optional function to retrieve the maximum sequence number
            for the given entity type from persistence. Required if start_seq_number is None.
        batch_size: Number of entities to retrieve in each API call. Default is DEFAULT_BATCH_SIZE (50).
        rate_limit_delay: Delay in seconds between API calls to avoid rate limiting.
            Default is DEFAULT_RATE_LIMIT_DELAY (0.5s), which is more conservative than
            Floriday's limit of FLORIDAY_RATE_LIMIT_CALLS_PER_SECOND (3.4 calls/second).
            A warning will be logged if the specified delay could exceed Floriday's rate limits.

    Returns:
        An EntitySyncResult containing sync statistics.

    Raises:
        ValueError: If both start_seq_number and get_max_sequence_number are None.

    Example:
        ```python
        # Basic usage
        result = sync_entities(
            entity_type="trade_items",
            fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
            persist_entity_callback=persist_item,
            start_seq_number=0
        )
        print(result)
        ```
    """
    # Use the EntitySynchronizer class internally to avoid code duplication
    synchronizer = EntitySynchronizer(
        entity_type=entity_type,
        fetch_entities_callback=fetch_entities_callback,
        persist_entity_callback=persist_entity_callback,
        start_seq_number=start_seq_number,
        get_max_sequence_number=get_max_sequence_number,
        batch_size=batch_size,
        rate_limit_delay=rate_limit_delay,
    )

    return synchronizer.sync()


class EntitySynchronizer(Generic[T]):
    """
    A class-based approach for synchronizing entities from Floriday API.

    This class provides a more flexible and feature-rich way to synchronize entities,
    including context manager support for easier resource management.

    Example:
        ```python
        # Basic usage with context manager
        with EntitySynchronizer(
            entity_type="trade_items",
            fetch_entities_callback=api_instance.get_trade_items_by_sequence_number,
            persist_entity_callback=persist_item,
            start_seq_number=0
        ) as synchronizer:
            result = synchronizer.sync()
            print(result)
        ```
    """

    def __init__(
        self,
        entity_type: str,
        fetch_entities_callback: Callable[[int, int], ApiSyncResult[T]],
        persist_entity_callback: Optional[Callable[[T], Any]] = None,
        start_seq_number: Optional[int] = None,
        get_max_sequence_number: Optional[Callable[[str], int]] = None,
        batch_size: int = DEFAULT_BATCH_SIZE,
        rate_limit_delay: float = DEFAULT_RATE_LIMIT_DELAY,
        config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a new EntitySynchronizer.

        Args:
            entity_type: A string identifier for the type of entity being synchronized.
            fetch_entities_callback: A function that retrieves entities by sequence number.
                It should accept a sequence number and limit, and return an ApiSyncResult.
            persist_entity_callback: Optional function to persist each entity. If None, entities
                will not be persisted.
            start_seq_number: Optional starting sequence number. If None and get_max_sequence_number
                is provided, it will be used to retrieve the starting sequence number.
            get_max_sequence_number: Optional function to retrieve the maximum sequence number
                for the given entity type from persistence. Required if start_seq_number is None.
            batch_size: Number of entities to retrieve in each API call. Default is DEFAULT_BATCH_SIZE (50).
            rate_limit_delay: Delay in seconds between API calls to avoid rate limiting.
                Default is DEFAULT_RATE_LIMIT_DELAY (0.5s).
            config: Optional dictionary with additional configuration options.
        """
        self.entity_type = entity_type
        self.fetch_entities_callback = fetch_entities_callback
        self.persist_entity_callback = persist_entity_callback
        self.start_seq_number = start_seq_number
        self.get_max_sequence_number = get_max_sequence_number
        self.batch_size = batch_size
        self.rate_limit_delay = rate_limit_delay
        self.config = config or {}

        # Internal state
        self._next_sequence_start_number = None
        self._entities_processed = 0
        self._is_initialized = False

    def __enter__(self):
        """Enter the context manager."""
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context manager."""
        # Nothing to clean up for now
        pass

    def execute(self) -> EntitySyncResult:
        """
        Execute the synchronization.

        This method is an alias for sync() that provides a more intuitive API
        when using the create_sync pattern.

        Returns:
            An EntitySyncResult containing sync statistics.

        Example:
            ```python
            # Create a synchronizer with advanced options
            sync = client.trade_items.create_sync(start_seq=0)

            # Configure the synchronizer
            sync.batch_size = 100
            sync.rate_limit_delay = 0.2

            # Execute the sync
            result = sync.execute()
            ```
        """
        return self.sync()

    def initialize(self) -> None:
        """
        Initialize the synchronizer.

        This method determines the starting sequence number and validates configuration.
        It is called automatically when using the context manager, but must be called
        manually if not using the context manager.

        Raises:
            ValueError: If both start_seq_number and get_max_sequence_number are None.
        """
        if self._is_initialized:
            return

        # Determine starting sequence number
        if self.start_seq_number is None:
            if self.get_max_sequence_number is None:
                raise ValueError(
                    "Either start_seq_number or get_max_sequence_number must be provided"
                )
            self.start_seq_number = self.get_max_sequence_number(self.entity_type)

        self._next_sequence_start_number = self.start_seq_number
        self._entities_processed = 0

        logger.info(
            f"Initializing sync for {self.entity_type} from sequence number {self._next_sequence_start_number}"
        )

        # Validate rate limit delay to ensure we don't exceed Floriday's limits
        min_safe_delay = 1.0 / FLORIDAY_RATE_LIMIT_CALLS_PER_SECOND
        if self.rate_limit_delay < min_safe_delay:
            logger.warning(
                f"Specified rate_limit_delay ({self.rate_limit_delay}s) is faster than Floriday's "
                f"limit of {FLORIDAY_RATE_LIMIT_CALLS_PER_SECOND} calls/second "
                f"(minimum safe delay: {min_safe_delay:.2f}s). "
                f"This may result in API rate limiting."
            )

        # Log configuration settings
        logger.debug(
            f"Sync configuration: batch_size={self.batch_size}, rate_limit_delay={self.rate_limit_delay}s "
            f"({1.0 / self.rate_limit_delay:.1f} calls/second)"
        )

        self._is_initialized = True

    def sync(self) -> EntitySyncResult:
        """
        Synchronize entities from Floriday API using sequence numbers.

        This method is similar to the original sync_entities function but uses the
        class instance's configuration.

        Returns:
            An EntitySyncResult containing sync statistics.
        """
        if not self._is_initialized:
            self.initialize()

        try:
            while True:
                sync_result = self.fetch_entities_callback(
                    sequence_number=self._next_sequence_start_number,
                    limit_result=self.batch_size,
                )

                # Check if we've reached the end of the data
                if (
                    self._next_sequence_start_number
                    >= sync_result.maximum_sequence_number
                ):
                    logger.info(
                        f"Reached maximum sequence number for {self.entity_type}"
                    )
                    break

                # Log sequence information for debugging
                logger.debug(
                    f"Current sequence: {self._next_sequence_start_number}, Max sequence: {sync_result.maximum_sequence_number}"
                )

                # Process entities
                for entity in sync_result.results:
                    self._entities_processed += 1

                    if self.persist_entity_callback:
                        result_id = self.persist_entity_callback(entity)
                        logger.debug(
                            f"Seq nr {getattr(entity, 'sequence_number', 'N/A')}: "
                            f"Persisted {self.entity_type} {result_id}"
                        )

                # Update sequence number for next batch
                self._next_sequence_start_number = sync_result.maximum_sequence_number

                # Apply rate limiting
                time.sleep(self.rate_limit_delay)

        except Exception as e:
            logger.error(
                f"Error during {self.entity_type} sync: {str(e)}", exc_info=True
            )
            return EntitySyncResult(
                entity_type=self.entity_type,
                start_sequence_number=self.start_seq_number,
                end_sequence_number=self._next_sequence_start_number,
                entities_processed=self._entities_processed,
                success=False,
                error=str(e),
            )

        logger.info(
            f"Done syncing {self.entity_type}. "
            f"Processed {self._entities_processed} entities from {self.start_seq_number} to {self._next_sequence_start_number}"
        )

        return EntitySyncResult(
            entity_type=self.entity_type,
            start_sequence_number=self.start_seq_number,
            end_sequence_number=self._next_sequence_start_number,
            entities_processed=self._entities_processed,
            success=True,
        )
