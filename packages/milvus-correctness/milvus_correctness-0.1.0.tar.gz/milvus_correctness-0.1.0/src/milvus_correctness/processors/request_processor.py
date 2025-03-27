"""Request processor for handling write operations."""

import threading
import time
from typing import Any

from tqdm import tqdm

from ..core.logging import get_logger
from ..core.models import OperationType, SuccessfulOperation, WriteRequest
from ..storage.base import QueueStorage

logger = get_logger()


class RequestProcessor:
    """
    Processes write requests from a queue and logs successful operations.

    Features:
    1. Batch processing for improved throughput
    2. Automatic retries for failed operations
    3. Progress tracking and statistics
    4. Graceful shutdown handling
    """

    def __init__(
        self,
        request_queue: QueueStorage[WriteRequest],
        success_log_queue: QueueStorage[SuccessfulOperation],
        milvus_client: Any,  # Type hint as Any to avoid circular import
        batch_size: int = 100,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        progress_interval: int = 1000,
    ):
        """Initialize the processor."""
        self.request_queue = request_queue
        self.success_log_queue = success_log_queue
        self.milvus_client = milvus_client
        self.batch_size = batch_size
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.progress_interval = progress_interval

        # Statistics
        self._processed_count = 0
        self._success_count = 0
        self._retry_count = 0
        self._error_count = 0
        self._start_time = None
        self._last_progress_time = None

        # Control
        self._stop_event = threading.Event()
        self._is_running = False

    def _process_batch(self, batch: list[dict | WriteRequest]) -> None:
        """Process a batch of requests."""
        # Group requests by operation type for batch processing
        op_groups = {}
        for request in batch:
            # Convert dict to WriteRequest if needed
            if isinstance(request, dict):
                request = WriteRequest(**request)
            op_groups.setdefault(request.op_type, []).append(request)

        # Process each operation type group
        for op_type, requests in op_groups.items():
            if op_type == OperationType.INSERT:
                self._process_insert_batch(requests)
            elif op_type == OperationType.UPSERT:
                self._process_upsert_batch(requests)
            elif op_type == OperationType.DELETE:
                self._process_delete_batch(requests)

    def _process_insert_batch(self, requests: list[dict | WriteRequest]) -> None:
        """Process a batch of INSERT requests."""
        # Convert all requests to WriteRequest objects
        requests = [req if isinstance(req, WriteRequest) else WriteRequest(**req) for req in requests]
        data_list = [req.data for req in requests if req.data]
        if not data_list:
            return

        try:
            self.milvus_client.collection.insert(data_list)
            # Log successful operations
            for req in requests:
                self.success_log_queue.put(
                    SuccessfulOperation(request_id=req.request_id, pk=req.pk, op_type=req.op_type, data=req.data)
                )
            self._success_count += len(requests)
        except Exception as e:
            logger.error(f"Batch INSERT failed: {str(e)}")
            # Fall back to individual processing
            for req in requests:
                self._process_single_request(req)

    def _process_upsert_batch(self, requests: list[dict | WriteRequest]) -> None:
        """Process a batch of UPSERT requests."""
        # Convert all requests to WriteRequest objects
        requests = [req if isinstance(req, WriteRequest) else WriteRequest(**req) for req in requests]
        data_list = [req.data for req in requests if req.data]
        if not data_list:
            return

        try:
            self.milvus_client.collection.upsert(data_list)
            # Log successful operations
            for req in requests:
                self.success_log_queue.put(
                    SuccessfulOperation(request_id=req.request_id, pk=req.pk, op_type=req.op_type, data=req.data)
                )
            self._success_count += len(requests)
        except Exception as e:
            logger.error(f"Batch UPSERT failed: {str(e)}")
            # Fall back to individual processing
            for req in requests:
                self._process_single_request(req)

    def _process_delete_batch(self, requests: list[dict | WriteRequest]) -> None:
        """Process a batch of DELETE requests."""
        # Convert all requests to WriteRequest objects
        requests = [req if isinstance(req, WriteRequest) else WriteRequest(**req) for req in requests]

        # Group by PK field type for correct expression formatting
        str_pks = []
        int_pks = []
        for req in requests:
            if isinstance(req.pk, str):
                str_pks.append(req.pk)
            else:
                int_pks.append(req.pk)

        try:
            # Process string PKs
            if str_pks:
                expr = f"{self.milvus_client._pk_field} in {str_pks}"
                self.milvus_client.collection.delete(expr)

            # Process integer PKs
            if int_pks:
                expr = f"{self.milvus_client._pk_field} in {int_pks}"
                self.milvus_client.collection.delete(expr)

            # Log successful operations
            for req in requests:
                self.success_log_queue.put(
                    SuccessfulOperation(request_id=req.request_id, pk=req.pk, op_type=req.op_type)
                )
            self._success_count += len(requests)
        except Exception as e:
            logger.error(f"Batch DELETE failed: {str(e)}")
            # Fall back to individual processing
            for req in requests:
                self._process_single_request(req)

    def _process_single_request(self, request: dict | WriteRequest) -> None:
        """Process a single request with retries."""
        # Convert request to WriteRequest if needed
        if isinstance(request, dict):
            request = WriteRequest(**request)

        retries = 0
        while retries < self.max_retries:
            try:
                if request.op_type == OperationType.INSERT:
                    if request.data:
                        self.milvus_client.collection.insert([request.data])
                elif request.op_type == OperationType.UPSERT:
                    if request.data:
                        self.milvus_client.collection.upsert([request.data])
                elif request.op_type == OperationType.DELETE:
                    expr = f"{self.milvus_client._pk_field} in [{request.pk}]"
                    self.milvus_client.collection.delete(expr)

                # Log successful operation
                self.success_log_queue.put(
                    SuccessfulOperation(
                        request_id=request.request_id, pk=request.pk, op_type=request.op_type, data=request.data
                    )
                )
                self._success_count += 1
                return
            except Exception as e:
                logger.error(f"Request failed (request_id={request.request_id}, retry={retries + 1}): {str(e)}")
                retries += 1
                self._retry_count += 1
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)

        self._error_count += 1
        logger.error(
            "Request failed permanently", request_id=request.request_id, pk=request.pk, op_type=request.op_type
        )

    def _update_progress(self) -> None:
        """Update and log progress statistics."""
        current_time = time.time()
        if self._last_progress_time is None:
            self._last_progress_time = current_time
            return

        if current_time - self._last_progress_time >= 5.0 or self._processed_count % self.progress_interval == 0:
            elapsed = current_time - self._start_time
            rate = self._processed_count / elapsed if elapsed > 0 else 0
            logger.info(
                "Processing progress",
                processed=self._processed_count,
                successful=self._success_count,
                retries=self._retry_count,
                errors=self._error_count,
                rate=f"{rate:.2f} req/s",
                elapsed=f"{elapsed:.2f}s",
            )
            self._last_progress_time = current_time

    def run(self, max_requests: int | None = None, show_progress: bool = True) -> None:
        """Run the processor."""
        if self._is_running:
            logger.warning("Processor is already running")
            return

        self._is_running = True
        self._stop_event.clear()
        self._start_time = time.time()
        self._last_progress_time = None

        logger.info(f"Starting request processor (batch_size={self.batch_size}, max_retries={self.max_retries})")

        try:
            with tqdm(
                total=max_requests,
                desc="处理请求",
                unit="个",
                disable=not show_progress,
                mininterval=1.0,  # 最小更新间隔1秒
                maxinterval=5.0,  # 最大更新间隔5秒
            ) as pbar:
                current_batch: list[WriteRequest] = []

                while not self._stop_event.is_set():
                    if max_requests and self._processed_count >= max_requests:
                        break

                    # Try to fill the batch
                    empty_queue = False
                    try:
                        while len(current_batch) < self.batch_size:
                            request = self.request_queue.get(block=True, timeout=1.0)
                            if request is None:
                                empty_queue = True
                                break
                            current_batch.append(request)
                    except Exception:
                        # 超时或队列为空
                        empty_queue = True

                    # Process the batch if we have requests
                    if current_batch:
                        self._process_batch(current_batch)
                        self._processed_count += len(current_batch)
                        pbar.update(len(current_batch))
                        self._update_progress()
                        current_batch = []

                    # 如果队列为空且没有待处理的请求，退出循环
                    if empty_queue and not current_batch:
                        break

        except KeyboardInterrupt:
            logger.info("Processor interrupted by user")
        except Exception as e:
            logger.error(f"Processor error: {str(e)}")
        finally:
            self._is_running = False
            elapsed = time.time() - self._start_time
            logger.info(
                "Processor finished",
                processed=self._processed_count,
                successful=self._success_count,
                retries=self._retry_count,
                errors=self._error_count,
                elapsed=f"{elapsed:.2f}s",
                rate=f"{self._processed_count / elapsed:.2f} req/s" if elapsed > 0 else "0 req/s",
            )

    def stop(self) -> None:
        """Stop the processor."""
        self._stop_event.set()
        logger.info("Stopping processor...")
