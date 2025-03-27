"""State calculator for determining expected final state."""

from typing import Any

from tqdm import tqdm

from ..core.logging import get_logger
from ..core.models import OperationType, SuccessfulOperation
from ..storage.base import QueueStorage, StateStorage

logger = get_logger()


class ExpectedStateCalculator:
    """
    Calculates the expected final state by processing successful operations.

    Features:
    1. Disk-based state tracking for large-scale data
    2. Streaming processing of success log
    3. Batch processing for improved performance
    4. Progress tracking and statistics
    """

    def __init__(
        self,
        success_log_queue: QueueStorage[SuccessfulOperation],
        state_storage: StateStorage,
        batch_size: int = 1000,
        progress_interval: int = 10000,
    ):
        """Initialize the calculator."""
        self.success_log_queue = success_log_queue
        self.state_storage = state_storage
        self.batch_size = batch_size
        self.progress_interval = progress_interval

        # Statistics
        self._processed_count = 0
        self._insert_count = 0
        self._upsert_count = 0
        self._delete_count = 0
        self._unique_pks = set()  # Only tracks PKs during current batch

    def _process_operation(self, operation: dict | SuccessfulOperation, batch: dict[str, dict[str, Any]]) -> None:
        """Process a single operation and update the batch."""
        # Convert operation to SuccessfulOperation if needed
        if isinstance(operation, dict):
            operation = SuccessfulOperation(**operation)

        pk_str = str(operation.pk)
        self._unique_pks.add(pk_str)

        if operation.op_type == OperationType.DELETE:
            batch[pk_str] = None  # Mark for deletion
            self._delete_count += 1
        else:
            batch[pk_str] = {"pk": operation.pk, "data": operation.data, "op_type": operation.op_type}
            if operation.op_type == OperationType.INSERT:
                self._insert_count += 1
            else:  # UPSERT
                self._upsert_count += 1

    def _flush_batch(self, batch: dict[str, dict[str, Any]], pbar: tqdm | None = None) -> None:
        """Flush a batch of operations to storage."""
        # Collect keys to delete
        delete_keys = [k for k, v in batch.items() if v is None]

        # Collect items to put
        put_items = {k: v for k, v in batch.items() if v is not None}

        # Execute batch operations
        if delete_keys:
            self.state_storage.batch_delete(delete_keys)
        if put_items:
            self.state_storage.batch_put(put_items)

        # Update progress
        batch_size = len(batch)
        self._processed_count += batch_size
        if pbar:
            pbar.update(batch_size)

        # Log progress periodically
        if self._processed_count % self.progress_interval == 0:
            logger.info(
                "Processing progress",
                processed=self._processed_count,
                inserts=self._insert_count,
                upserts=self._upsert_count,
                deletes=self._delete_count,
                unique_pks=len(self._unique_pks),
            )

    def calculate_final_state(self, show_progress: bool = True) -> None:
        """
        Calculate the expected final state by consuming the success log queue.
        The state is stored in the state storage backend.
        """
        logger.info(f"Starting state calculation (batch_size={self.batch_size})")

        # Clear any existing state
        self.state_storage.clear()

        try:
            current_batch: dict[str, dict[str, Any]] = {}
            # 获取队列大小
            queue_size = self.success_log_queue.qsize()
            with tqdm(
                desc="计算状态",
                unit="个",
                total=queue_size,
                disable=not show_progress,
                mininterval=1.0,  # 最小更新间隔1秒
                maxinterval=5.0,  # 最大更新间隔5秒
            ) as pbar:
                while True:
                    # Get next operation
                    operation = self.success_log_queue.get(block=False)
                    if operation is None:
                        break

                    # Process operation
                    self._process_operation(operation, current_batch)

                    # Flush batch if full
                    if len(current_batch) >= self.batch_size:
                        self._flush_batch(current_batch, pbar)
                        current_batch = {}
                        self._unique_pks.clear()

                # Flush final batch
                if current_batch:
                    self._flush_batch(current_batch, pbar)

        except KeyboardInterrupt:
            logger.warning("State calculation interrupted by user")
        finally:
            logger.info(
                "State calculation finished",
                processed=self._processed_count,
                inserts=self._insert_count,
                upserts=self._upsert_count,
                deletes=self._delete_count,
            )

    def verify_against_milvus(
        self,
        milvus_client: Any,  # Type hint as Any to avoid circular import
        batch_size: int = 1000,
        sample_size: int | None = None,
        show_progress: bool = True,
    ) -> tuple[bool, dict[str, int]]:
        """
        Verify the calculated state against Milvus.

        Args:
            milvus_client: MilvusClientWrapper instance
            batch_size: Number of PKs to verify in each batch
            sample_size: If set, verify only a random sample of PKs

        Returns:
            tuple[bool, Dict[str, int]]: (is_consistent, statistics)
        """
        logger.info(f"Starting verification (batch_size={batch_size}, sample_size={sample_size})")

        stats = {"total_checked": 0, "matching": 0, "missing_in_milvus": 0, "extra_in_milvus": 0, "data_mismatch": 0}

        try:
            # Get iterator over state storage
            it = self.state_storage.iterator()
            current_batch: dict[str, dict[str, Any]] = {}

            with tqdm(
                desc="验证状态",
                unit="个",
                total=sample_size if sample_size else None,
                disable=not show_progress,
                mininterval=1.0,  # 最小更新间隔1秒
                maxinterval=5.0,  # 最大更新间隔5秒
            ) as pbar:
                for pk_str, expected_data in it:
                    if sample_size and stats["total_checked"] >= sample_size:
                        break

                    current_batch[pk_str] = expected_data
                    if len(current_batch) >= batch_size:
                        self._verify_batch(current_batch, milvus_client, stats)
                        current_batch = {}
                        pbar.update(batch_size)

                # Verify final batch
                if current_batch:
                    self._verify_batch(current_batch, milvus_client, stats)
                    pbar.update(len(current_batch))

        except Exception as e:
            logger.error(f"Verification error: {str(e)}")
            return False, stats

        is_consistent = (
            stats["missing_in_milvus"] == 0 and stats["extra_in_milvus"] == 0 and stats["data_mismatch"] == 0
        )

        logger.info(f"Verification finished: consistent={is_consistent}, matching={stats['matching']}, " \
                  f"missing_in_milvus={stats['missing_in_milvus']}, extra_in_milvus={stats['extra_in_milvus']}, " \
                  f"data_mismatch={stats['data_mismatch']}, total_checked={stats['total_checked']}")

        return is_consistent, stats

    def _verify_batch(self, batch: dict[str, dict[str, Any]], milvus_client: Any, stats: dict[str, int]) -> None:
        """Verify a batch of PKs against Milvus."""
        # Convert PKs to appropriate type
        pks = []
        for pk_str, _ in batch.items():
            pk = int(pk_str) if pk_str.isdigit() else pk_str
            pks.append(pk)

        # Query Milvus
        expr = f"{milvus_client._pk_field} in {pks}"
        results = milvus_client.collection.query(
            expr=expr,
            output_fields=["*"],  # Include all fields
        )

        # Build map of actual results
        actual_results = {str(item[milvus_client._pk_field]): item for item in results}

        # Compare results
        for pk_str, expected_data in batch.items():
            stats["total_checked"] += 1
            actual_data = actual_results.get(pk_str)

            if actual_data is None:
                stats["missing_in_milvus"] += 1
                logger.warning(f"PK missing in Milvus: {pk_str}")
            else:
                # Compare data
                if self._compare_data(expected_data, actual_data):
                    stats["matching"] += 1
                else:
                    stats["data_mismatch"] += 1
                    logger.warning(f"Data mismatch for PK {pk_str}: expected={expected_data}, actual={actual_data}")

        # Check for extra PKs in Milvus
        extra_pks = set(actual_results.keys()) - set(batch.keys())
        stats["extra_in_milvus"] += len(extra_pks)
        if extra_pks:
            logger.warning(f"Extra PKs found in Milvus: {extra_pks}")

    def _compare_data(self, expected: dict[str, Any], actual: dict[str, Any]) -> bool:
        """Compare expected and actual data."""
        if expected is None:
            return actual is None

        if "data" not in expected:
            return True  # Skip comparison for deleted items

        expected_data = expected["data"]

        # 检查所有必需字段是否存在
        required_fields = {"id", "vector", "text", "score", "timestamp"}
        if not all(field in actual for field in required_fields):
            return False

        # 比较标量字段
        scalar_fields = {"id", "text", "timestamp"}
        for field in scalar_fields:
            if expected_data[field] != actual[field]:
                return False

        # 比较 vector，考虑浮点数精度
        expected_vector = [float(x) for x in expected_data["vector"]]
        actual_vector = [float(x) for x in actual["vector"]]
        if len(expected_vector) != len(actual_vector):
            return False
        for e, a in zip(expected_vector, actual_vector, strict=True):
            if abs(e - a) > 1e-4:  # 允许小的浮点数误差
                return False

        # 比较 score，考虑浮点数精度
        if abs(float(expected_data["score"]) - float(actual["score"])) > 1e-1:  # score 可以允许更大的误差
            return False

        return True
