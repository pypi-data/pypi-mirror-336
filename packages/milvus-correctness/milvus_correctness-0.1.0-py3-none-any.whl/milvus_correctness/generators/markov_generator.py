"""Markov chain-based request generator with probabilistic PK tracking."""

import random
import uuid

import numpy as np

from ..core.logging import get_logger
from ..core.models import GeneratorConfig, OperationType, WriteRequest
from ..storage.base import StateStorage

logger = get_logger()


class MarkovRequestGenerator:
    """
    Generates WriteRequest objects based on a Markov chain for operation types
    and probabilistic PK tracking for large-scale simulation.

    This implementation uses a combination of:
    1. Probabilistic PK tracking (Bloom filter) for memory efficiency
    2. Disk-based state storage for accurate PK existence checks when needed
    3. Sampling-based approach for selecting existing PKs
    """

    def __init__(
        self,
        config: GeneratorConfig,
        state_storage: StateStorage | None = None,
        initial_active_pks: set[int | str] | None = None,
    ):
        """Initialize the generator."""
        self.config = config
        self.state_storage = state_storage
        self._validate_probabilities()

        # Internal state
        self.current_op_type: OperationType | None = None
        self.next_new_pk_candidate: int = 0

        # Initialize probabilistic PK tracking
        self._init_pk_tracking(initial_active_pks)

        logger.info(
            f"MarkovRequestGenerator initialized (pk_tracking_method="
            f"{('probabilistic' if state_storage else 'memory')}, "
            f"max_pk_value={config.max_pk_value})"
        )

    def _validate_probabilities(self) -> None:
        """Validate transition and initial probabilities."""
        if not abs(sum(self.config.initial_state_probs.values()) - 1.0) < 1e-9:
            raise ValueError("Initial state probabilities must sum to 1.0")

        for state, transitions in self.config.transition_matrix.items():
            if not abs(sum(transitions.values()) - 1.0) < 1e-9:
                raise ValueError(f"Transition probabilities for state '{state}' must sum to 1.0")

    def _init_pk_tracking(self, initial_active_pks: set[int | str] | None = None) -> None:
        """Initialize PK tracking mechanism."""
        if initial_active_pks:
            if self.state_storage:
                # Store initial PKs in state storage
                batch = {str(pk): {"exists": True, "last_op": "INSERT"} for pk in initial_active_pks}
                self.state_storage.batch_put(batch)
            else:
                # Use in-memory set for small-scale testing
                self._active_pks = initial_active_pks
        elif self.state_storage:
            # Start with empty state storage
            pass
        else:
            # Start with empty in-memory set
            self._active_pks = set()

    def _get_next_op_type(self) -> OperationType:
        """Determine the next operation type based on Markov chain."""
        if self.current_op_type is None:
            # Initial state
            states = list(self.config.initial_state_probs.keys())
            probs = list(self.config.initial_state_probs.values())
            state_idx = np.random.choice(len(states), p=probs)
            self.current_op_type = states[state_idx]
        else:
            # Transition to next state
            transitions = self.config.transition_matrix[self.current_op_type]
            states = list(transitions.keys())
            probs = list(transitions.values())
            state_idx = np.random.choice(len(states), p=probs)
            self.current_op_type = states[state_idx]

        return self.current_op_type

    def _generate_vector(self) -> list[float]:
        """Generate a random vector of specified dimension."""
        return list(np.random.randn(self.config.vector_dim))

    def _generate_field_value(self, field_type: str) -> int | float | str | list:
        """Generate a random value for a field based on its type."""
        if field_type == "int":
            return random.randint(0, 1000000)
        elif field_type == "float":
            return random.uniform(0, 1000000)
        elif field_type == "str":
            return str(uuid.uuid4())
        elif field_type.startswith("vector"):
            dim = int(field_type.split("[")[1].rstrip("]"))
            return list(np.random.randn(dim))
        else:
            raise ValueError(f"Unsupported field type: {field_type}")

    def _check_pk_exists(self, pk: int | str) -> bool:
        """Check if a PK exists using the appropriate tracking mechanism."""
        if self.state_storage:
            return self.state_storage.get(str(pk)) is not None
        return pk in self._active_pks

    def _add_pk(self, pk: int | str, op_type: OperationType) -> None:
        """Track a new PK using the appropriate mechanism."""
        if self.state_storage:
            self.state_storage.put(str(pk), {"exists": True, "last_op": op_type})
        else:
            self._active_pks.add(pk)

    def _remove_pk(self, pk: int | str) -> None:
        """Remove a PK using the appropriate mechanism."""
        if self.state_storage:
            self.state_storage.delete(str(pk))
        else:
            self._active_pks.discard(pk)

    def _select_existing_pk(self) -> int | str | None:
        """Select an existing PK using sampling or state storage."""
        if self.state_storage:
            # Sample from state storage using iterator
            it = self.state_storage.iterator()
            try:
                # Reservoir sampling
                selected = None
                count = 0
                for pk, _ in it:
                    count += 1
                    if random.random() < 1 / count:
                        selected = pk
                return int(selected) if isinstance(selected, str) and selected.isdigit() else selected
            except StopIteration:
                return None
        else:
            # Sample from in-memory set
            return random.choice(list(self._active_pks)) if self._active_pks else None

    def _select_pk(self, op_type: OperationType) -> int | str:
        """Select a PK based on operation type and probabilities."""
        if op_type == OperationType.INSERT:
            if random.random() < self.config.prob_new_pk_for_insert or (
                self.state_storage is None and not self._active_pks
            ):
                # Generate new PK
                while True:
                    pk = self.next_new_pk_candidate
                    self.next_new_pk_candidate += 1
                    if not self._check_pk_exists(pk):
                        return pk
            else:
                # Use existing PK
                existing_pk = self._select_existing_pk()
                return existing_pk if existing_pk is not None else self.next_new_pk_candidate

        else:  # UPSERT or DELETE
            if random.random() < self.config.prob_existing_pk_for_update_delete and (
                self.state_storage is not None or self._active_pks
            ):
                # Use existing PK
                existing_pk = self._select_existing_pk()
                if existing_pk is not None:
                    return existing_pk

            # Generate new PK if no existing PK available or probability check failed
            return self.next_new_pk_candidate

    def generate_request(self) -> WriteRequest:
        """Generate a single write request."""
        op_type = self._get_next_op_type()
        pk = self._select_pk(op_type)

        # Prepare data for INSERT/UPSERT
        data = None
        if op_type in (OperationType.INSERT, OperationType.UPSERT):
            data = {
                self.config.pk_field_name: pk,
                self.config.vector_field_name: self._generate_vector(),
            }
            # Add other fields according to schema
            for field_name, field_type in self.config.data_schema.items():
                data[field_name] = self._generate_field_value(field_type)

        # Update PK tracking
        if op_type == OperationType.INSERT:
            self._add_pk(pk, op_type)
        elif op_type == OperationType.DELETE:
            self._remove_pk(pk)
        # For UPSERT, we don't need to update tracking as it doesn't affect existence

        return WriteRequest(request_id=str(uuid.uuid4()), pk=pk, op_type=op_type, data=data)
