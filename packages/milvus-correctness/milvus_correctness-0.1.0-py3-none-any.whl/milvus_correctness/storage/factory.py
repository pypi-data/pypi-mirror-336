"""Storage factory for creating storage instances."""

from typing import Any, TypeVar

from .base import QueueStorage, StateStorage
from .persist_queue_storage import PersistQueueStorage, PersistStateStorage

T = TypeVar("T")


class StorageFactory:
    """Factory class for creating storage instances."""

    QUEUE_BACKENDS: dict[str, type[QueueStorage]] = {
        "persist-queue": PersistQueueStorage,
    }

    STATE_BACKENDS: dict[str, type[StateStorage]] = {
        "persist-queue": PersistStateStorage,
    }

    @classmethod
    def create_queue(cls, backend: str, path: str, name: str = "default", **kwargs: Any) -> QueueStorage[T]:
        """Create a queue storage instance."""
        if backend not in cls.QUEUE_BACKENDS:
            raise ValueError(f"Unsupported queue backend: {backend}")
        return cls.QUEUE_BACKENDS[backend](path=path, name=name, **kwargs)

    @classmethod
    def create_state(cls, backend: str, path: str, name: str = "default", **kwargs: Any) -> StateStorage:
        """Create a state storage instance."""
        if backend not in cls.STATE_BACKENDS:
            raise ValueError(f"Unsupported state backend: {backend}")
        return cls.STATE_BACKENDS[backend](path=path, name=name, **kwargs)
