"""Core data models for the Milvus correctness framework."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class OperationType(str, Enum):
    """Supported operation types."""

    INSERT = "INSERT"
    UPSERT = "UPSERT"
    DELETE = "DELETE"


class WriteRequest(BaseModel):
    """Represents a single write operation request."""

    request_id: str = Field(..., description="Unique identifier for the request")
    pk: int | str = Field(..., description="Primary key value")
    op_type: OperationType = Field(..., description="Operation type")
    data: dict[str, Any] | None = Field(
        None, description="Data for INSERT/UPSERT operations, should contain PK field and vector field"
    )

    model_config = {"json_encoders": {OperationType: lambda x: x.value}}


class SuccessfulOperation(BaseModel):
    """Represents a successfully executed operation, logged for state calculation."""

    request_id: str = Field(..., description="Unique identifier for the request")
    pk: int | str = Field(..., description="Primary key value")
    op_type: OperationType = Field(..., description="Operation type")
    data: dict[str, Any] | None = Field(None, description="Data for INSERT/UPSERT operations, can be None for DELETE")


class MilvusConfig(BaseModel):
    """Configuration for Milvus connection."""

    host: str = Field(..., description="Milvus server host")
    port: int | str = Field(..., description="Milvus server port")
    collection_name: str = Field(..., description="Target collection name")
    alias: str = Field("default", description="Connection alias")


class GeneratorConfig(BaseModel):
    """Configuration for the request generator."""

    op_states: list[OperationType] = Field(..., description="List of possible operation states")
    transition_matrix: dict[OperationType, dict[OperationType, float]] = Field(
        ..., description="State transition probabilities"
    )
    initial_state_probs: dict[OperationType, float] = Field(..., description="Initial state probabilities")
    pk_field_name: str = Field(..., description="Name of the primary key field")
    vector_field_name: str = Field(..., description="Name of the vector field")
    max_pk_value: int = Field(1_000_000, description="Maximum value for integer primary keys")
    prob_new_pk_for_insert: float = Field(0.9, description="Probability of using a new PK for INSERT")
    prob_existing_pk_for_update_delete: float = Field(
        0.8, description="Probability of using an existing PK for UPSERT/DELETE"
    )
    data_schema: dict[str, Any] = Field(..., description="Schema for non-PK and non-vector fields")
    vector_dim: int = Field(..., description="Dimension of the vector field")


class StorageConfig(BaseModel):
    """Configuration for persistent storage."""

    request_queue_path: str = Field(..., description="Path to the request queue storage")
    success_log_path: str = Field(..., description="Path to the success log storage")
    failure_log_path: str | None = Field(None, description="Path to the failure log file")
    clear_on_start: bool = Field(False, description="Whether to clear storage on start")
    storage_type: str = Field("persist-queue", description="Storage backend type (sqlite, persist-queue)")
