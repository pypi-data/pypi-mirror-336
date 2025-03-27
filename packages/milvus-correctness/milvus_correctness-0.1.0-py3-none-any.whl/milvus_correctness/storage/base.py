"""Base storage interfaces for the Milvus correctness framework."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class QueueStorage(ABC, Generic[T]):
    """Abstract base class for queue storage implementations."""

    @abstractmethod
    def put(self, item: T) -> None:
        """Put an item into the queue."""
        pass

    @abstractmethod
    def get(self, block: bool = True, timeout: float | None = None) -> T | None:
        """Get an item from the queue."""
        pass

    @abstractmethod
    def qsize(self) -> int:
        """Return the approximate size of the queue."""
        pass

    @abstractmethod
    def empty(self) -> bool:
        """Return True if the queue is empty, False otherwise."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all items from the queue."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the queue storage."""
        pass


class StateStorage(ABC):
    """Abstract base class for state storage implementations."""

    @abstractmethod
    def put(self, key: str, value: dict[str, Any]) -> None:
        """Store a key-value pair."""
        pass

    @abstractmethod
    def get(self, key: str) -> dict[str, Any] | None:
        """Retrieve a value by key."""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete a key-value pair."""
        pass

    @abstractmethod
    def iterator(self, start_key: str | None = None) -> Iterator[tuple[str, dict[str, Any]]]:
        """Return an iterator over key-value pairs."""
        pass

    @abstractmethod
    def batch_put(self, items: dict[str, dict[str, Any]]) -> None:
        """Store multiple key-value pairs in a batch."""
        pass

    @abstractmethod
    def batch_get(self, keys: list[str]) -> dict[str, dict[str, Any] | None]:
        """Retrieve multiple values by keys."""
        pass

    @abstractmethod
    def batch_delete(self, keys: list[str]) -> None:
        """Delete multiple key-value pairs."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all data from storage."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close the storage."""
        pass
