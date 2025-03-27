"""Milvus client wrapper for the correctness framework."""

import threading
from typing import Any

from pymilvus import Collection, DataType, MilvusException, connections, utility

from ..core.logging import get_logger
from .models import MilvusConfig

logger = get_logger()


class MilvusClientWrapper:
    """
    Wrapper for Milvus client with enhanced functionality.

    Features:
    1. Connection management and auto-reconnection
    2. Collection schema introspection
    3. Batch operation support
    4. Error handling and logging
    """

    def __init__(self, config: MilvusConfig):
        """Initialize the client."""
        self.config = config
        self.collection: Collection | None = None
        self._pk_field: str | None = None
        self._vector_field: str | None = None
        self._lock = threading.Lock()
        self._is_connected = False

    def connect(self) -> None:
        """Connect to Milvus and load the collection."""
        with self._lock:
            try:
                if self._is_connected:
                    logger.warning("Already connected to Milvus")
                    return

                connections.connect(alias=self.config.alias, host=self.config.host, port=str(self.config.port))

                logger.info(
                    f"Connected to Milvus (host={self.config.host}, port={self.config.port}, alias={self.config.alias})"
                )

                if not utility.has_collection(self.config.collection_name, using=self.config.alias):
                    raise ValueError(f"Collection '{self.config.collection_name}' does not exist")

                self.collection = Collection(name=self.config.collection_name, using=self.config.alias)
                self._introspect_schema()
                self._ensure_collection_loaded()
                self._is_connected = True

            except Exception as e:
                logger.error(f"Failed to connect to Milvus (collection={self.config.collection_name}): {str(e)}")
                self.disconnect()
                raise

    def disconnect(self) -> None:
        """Disconnect from Milvus."""
        with self._lock:
            if not self._is_connected:
                return

            try:
                connections.disconnect(self.config.alias)
                logger.info(f"Disconnected from Milvus (alias={self.config.alias})")
            except Exception as e:
                logger.error(f"Error disconnecting from Milvus (alias={self.config.alias}): {str(e)}")
            finally:
                self.collection = None
                self._pk_field = None
                self._vector_field = None
                self._is_connected = False

    def _introspect_schema(self) -> None:
        """Introspect collection schema to identify field types."""
        if not self.collection:
            raise RuntimeError("Collection not initialized")

        schema = self.collection.schema
        for field in schema.fields:
            if field.is_primary:
                self._pk_field = field.name
            if field.dtype in (DataType.FLOAT_VECTOR, DataType.BINARY_VECTOR):
                self._vector_field = field.name

        if not self._pk_field:
            raise ValueError(f"Could not find primary key field in collection '{self.config.collection_name}'")

        logger.info(f"Collection schema introspected: pk_field={self._pk_field}, vector_field={self._vector_field}")

    def _ensure_collection_loaded(self) -> None:
        """Ensure the collection is loaded into memory."""
        if not self.collection:
            raise RuntimeError("Collection not initialized")

        load_state = utility.load_state(self.config.collection_name, using=self.config.alias)

        if load_state != "Loaded":
            logger.info(f"Loading collection {self.config.collection_name} (current_state={load_state})")
            self.collection.load()
            self.collection.flush()
            logger.info(f"Collection loaded: {self.config.collection_name}")
        else:
            logger.info(f"Collection already loaded: {self.config.collection_name}")

    def _ensure_connected(self) -> None:
        """Ensure connection is active, reconnect if necessary."""
        if not self._is_connected:
            logger.warning("Not connected to Milvus, attempting to reconnect")
            self.connect()

    def execute_batch_insert(self, data_list: list[dict[str, Any]], timeout: float | None = None) -> bool:
        """Execute batch insert operation."""
        self._ensure_connected()
        try:
            self.collection.insert(data_list, timeout=timeout)
            return True
        except MilvusException as e:
            logger.error(f"Batch INSERT failed (code={e.code}, count={len(data_list)}): {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in batch INSERT: {str(e)}")
            return False

    def execute_batch_upsert(self, data_list: list[dict[str, Any]], timeout: float | None = None) -> bool:
        """Execute batch upsert operation."""
        self._ensure_connected()
        try:
            self.collection.upsert(data_list, timeout=timeout)
            return True
        except MilvusException as e:
            logger.error(f"Batch UPSERT failed (code={e.code}, count={len(data_list)}): {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in batch UPSERT: {str(e)}")
            return False

    def execute_batch_delete(self, pks: list[Any], timeout: float | None = None) -> bool:
        """Execute batch delete operation."""
        self._ensure_connected()
        try:
            expr = f"{self._pk_field} in {pks}"
            self.collection.delete(expr, timeout=timeout)
            return True
        except MilvusException as e:
            logger.error(f"Batch DELETE failed (code={e.code}, count={len(pks)}): {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error in batch DELETE: {str(e)}")
            return False

    def get_collection_stats(self) -> dict[str, Any]:
        """Get collection statistics."""
        self._ensure_connected()
        try:
            stats = {
                "name": self.config.collection_name,
                "row_count": self.collection.num_entities,
            }
            return stats
        except Exception as e:
            logger.error(f"Failed to get collection stats for {self.config.collection_name}: {str(e)}")
            return {}
