"""Storage implementation using persist-queue."""

import os
from collections.abc import Iterator
from typing import Any, Generic, TypeVar

from persistqueue import Queue, SQLiteQueue
from persistqueue.serializers import json as pq_json

from ..core.logging import get_logger
from .base import QueueStorage, StateStorage

logger = get_logger()

T = TypeVar("T")


class PersistQueueStorage(QueueStorage[T], Generic[T]):
    """Queue storage implementation using persist-queue."""

    def __init__(self, path: str, name: str = "queue"):
        """Initialize the queue storage.

        Args:
            path: Path to the storage directory
            name: Name of the queue
        """
        os.makedirs(path, exist_ok=True)
        self._queue = Queue(
            path=os.path.join(path, name),
            chunksize=100,
            serializer=pq_json,
        )

    def put(self, item: T) -> None:
        """Put an item into the queue."""
        if hasattr(item, "model_dump"):
            # 如果是 Pydantic 模型，先转换为字典
            self._queue.put(item.model_dump())
        else:
            self._queue.put(item)

    def get(self, block: bool = True, timeout: float | None = None) -> T | None:
        """Get an item from the queue."""
        try:
            return self._queue.get(block=block, timeout=timeout)
        except Exception:  # Queue is empty or timeout
            return None

    def qsize(self) -> int:
        """Return the approximate size of the queue."""
        return self._queue.qsize()

    def empty(self) -> bool:
        """Return True if the queue is empty, False otherwise."""
        return self._queue.empty()

    def clear(self) -> None:
        """Clear all items from the queue."""
        try:
            if hasattr(self._queue, "clear"):
                self._queue.clear()
            else:
                while not self.empty():
                    _ = self.get(block=False)
        except Exception as e:
            logger.warning(f"Failed to clear queue: {str(e)}")

    def close(self) -> None:
        """Close the queue storage."""
        try:
            if hasattr(self._queue, "close"):
                self._queue.close()
        except Exception as e:
            logger.warning(f"Failed to close queue: {str(e)}")


class PersistStateStorage(StateStorage):
    """State storage implementation using persist-queue SQLiteQueue."""

    def __init__(self, path: str, name: str = "state"):
        """Initialize the state storage.

        Args:
            path: Path to the storage directory
            name: Name of the state storage
        """
        os.makedirs(path, exist_ok=True)
        self._queue = SQLiteQueue(
            path=os.path.join(path, name),
            multithreading=True,
            auto_commit=True,
        )
        self._cache: dict[str, dict[str, Any]] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load all items from queue into memory cache."""
        while not self._queue.empty():
            item = self._queue.get()
            if isinstance(item, dict) and "key" in item and "value" in item:
                self._cache[item["key"]] = item["value"]

    def put(self, key: str, value: dict[str, Any]) -> None:
        """Store a key-value pair."""
        self._cache[key] = value
        self._queue.put({"key": key, "value": value})

    def get(self, key: str) -> dict[str, Any] | None:
        """Retrieve a value by key."""
        return self._cache.get(key)

    def delete(self, key: str) -> None:
        """Delete a key-value pair."""
        if key in self._cache:
            del self._cache[key]
            # For SQLiteQueue, we need to rebuild the queue to remove the item
            self.clear()
            for k, v in self._cache.items():
                self._queue.put({"key": k, "value": v})

    def iterator(self, start_key: str | None = None) -> Iterator[tuple[str, dict[str, Any]]]:
        """Return an iterator over key-value pairs."""
        items = sorted(self._cache.items())
        if start_key is not None:
            for key, value in items:
                if key >= start_key:
                    yield key, value
        else:
            yield from items

    def batch_put(self, items: dict[str, dict[str, Any]]) -> None:
        """Store multiple key-value pairs in a batch."""
        for key, value in items.items():
            self.put(key, value)

    def batch_get(self, keys: list[str]) -> dict[str, dict[str, Any] | None]:
        """Retrieve multiple values by keys."""
        return {key: self.get(key) for key in keys}

    def batch_delete(self, keys: list[str]) -> None:
        """Delete multiple key-value pairs."""
        for key in keys:
            self.delete(key)

    def clear(self) -> None:
        """Clear all data from storage."""
        try:
            if hasattr(self._queue, "clear"):
                self._queue.clear()
            else:
                # 手动清理所有项
                while True:
                    try:
                        self._queue.get(block=False)
                    except Exception:
                        break
            self._cache.clear()
        except Exception as e:
            logger.warning(f"Failed to clear state storage: {str(e)}")

    def close(self) -> None:
        """Close the storage."""
        self._queue.close()
