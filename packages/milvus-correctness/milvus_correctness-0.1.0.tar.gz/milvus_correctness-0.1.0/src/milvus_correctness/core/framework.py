"""Core framework for Milvus correctness testing."""

import os
import shutil
from typing import Any

from tqdm import tqdm

from ..calculators.state_calculator import ExpectedStateCalculator
from ..core.logging import get_logger
from ..generators.markov_generator import MarkovRequestGenerator
from ..processors.request_processor import RequestProcessor
from ..storage.base import QueueStorage, StateStorage
from ..storage.factory import StorageFactory
from .milvus_client import MilvusClientWrapper
from .models import GeneratorConfig, MilvusConfig, StorageConfig, WriteRequest

logger = get_logger()


class CorrectnessFramework:
    """
    主框架类，用于协调请求生成、处理和状态计算。

    特性：
    1. 支持大规模数据处理（1B+）
    2. 可配置的存储后端 (RocksDB, LMDB)
    3. 批处理优化
    4. 进度跟踪和统计
    5. 优雅的错误处理
    """

    def __init__(
        self,
        milvus_config: MilvusConfig,
        generator_config: GeneratorConfig,
        storage_config: StorageConfig,
        batch_size: int = 1000,
        max_retries: int = 3,
    ):
        """初始化框架。"""
        self.milvus_config = milvus_config
        self.generator_config = generator_config
        self.storage_config = storage_config
        self.batch_size = batch_size
        self.max_retries = max_retries

        # 清理持久化存储（如果配置要求）
        if storage_config.clear_on_start:
            self._clear_persistent_storage()

        # 初始化存储
        self._init_storage()

        # 初始化 Milvus 客户端
        self.milvus_client = MilvusClientWrapper(milvus_config)

        # 初始化处理器
        self.processor = RequestProcessor(
            request_queue=self.request_queue,
            success_log_queue=self.success_log_queue,
            milvus_client=self.milvus_client,
            batch_size=batch_size,
            max_retries=max_retries,
        )

        # 初始化状态计算器
        self.calculator = ExpectedStateCalculator(
            success_log_queue=self.success_log_queue, state_storage=self.state_storage, batch_size=batch_size
        )

        logger.info(
            f"CorrectnessFramework initialized (collection={milvus_config.collection_name}, "
            f"storage_type={storage_config.storage_type}, batch_size={batch_size})"
        )

    def _clear_persistent_storage(self) -> None:
        """清理所有持久化存储。"""
        paths = [self.storage_config.request_queue_path, self.storage_config.success_log_path]
        if self.storage_config.failure_log_path:
            paths.append(os.path.dirname(self.storage_config.failure_log_path))

        for path in paths:
            if os.path.exists(path):
                try:
                    shutil.rmtree(path)
                    logger.info(f"Cleared storage directory: {path}")
                except Exception as e:
                    logger.error(f"Failed to clear storage directory {path}: {str(e)}")

    def _init_storage(self) -> None:
        """初始化所有存储组件。"""
        # 创建请求队列
        self.request_queue: QueueStorage[WriteRequest] = StorageFactory.create_queue(
            backend=self.storage_config.storage_type, path=self.storage_config.request_queue_path, name="requests"
        )

        # 创建成功日志队列
        self.success_log_queue: QueueStorage[WriteRequest] = StorageFactory.create_queue(
            backend=self.storage_config.storage_type, path=self.storage_config.success_log_path, name="success_log"
        )

        # 创建状态存储
        self.state_storage: StateStorage = StorageFactory.create_state(
            backend=self.storage_config.storage_type,
            path=os.path.join(self.storage_config.success_log_path, "state"),
            name="expected_state",
        )

        logger.info(f"Storage components initialized (storage_type={self.storage_config.storage_type})")

    def generate_requests(self, count: int, show_progress: bool = True) -> None:
        """生成指定数量的写请求。"""
        logger.info(f"Starting request generation (count={count})")

        # 创建生成器
        generator = MarkovRequestGenerator(config=self.generator_config, state_storage=self.state_storage)

        try:
            with tqdm(
                total=count,
                desc="生成请求",
                unit="个",
                disable=not show_progress,
                mininterval=1.0,  # 最小更新间隔1秒
                maxinterval=5.0,  # 最大更新间隔5秒
            ) as pbar:
                for _ in range(count):
                    request = generator.generate_request()
                    self.request_queue.put(request)
                    pbar.update(1)

            logger.info(f"Request generation completed (count={count})")
        except Exception as e:
            logger.error(f"Request generation failed: {str(e)}")
            raise

    def process_requests(self, max_requests: int | None = None, show_progress: bool = True) -> None:
        """处理队列中的请求。"""
        try:
            # 连接 Milvus
            self.milvus_client.connect()

            # 运行处理器
            self.processor.run(max_requests=max_requests, show_progress=show_progress)
        except Exception as e:
            logger.error(f"Request processing failed: {str(e)}")
            raise
        finally:
            self.milvus_client.disconnect()

    def calculate_expected_state(self, show_progress: bool = True) -> None:
        """计算预期的最终状态。"""
        try:
            self.calculator.calculate_final_state(show_progress=show_progress)
        except Exception as e:
            logger.error(f"State calculation failed: {str(e)}")
            raise

    def verify_state(self, sample_size: int | None = None, show_progress: bool = True) -> tuple[bool, dict[str, int]]:
        """验证预期状态与 Milvus 实际状态的一致性。"""
        try:
            # 连接 Milvus
            self.milvus_client.connect()

            # 执行验证
            return self.calculator.verify_against_milvus(
                milvus_client=self.milvus_client,
                batch_size=self.batch_size,
                sample_size=sample_size,
                show_progress=show_progress,
            )
        except Exception as e:
            logger.error(f"State verification failed: {str(e)}")
            raise
        finally:
            self.milvus_client.disconnect()

    def get_statistics(self) -> dict[str, Any]:
        """获取框架的统计信息。"""
        try:
            stats = {
                "request_queue_size": self.request_queue.qsize(),
                "success_log_queue_size": self.success_log_queue.qsize(),
                "processed_count": self.processor._processed_count,
                "success_count": self.processor._success_count,
                "retry_count": self.processor._retry_count,
                "error_count": self.processor._error_count,
            }

            # 添加 Milvus 集合统计信息
            if self.milvus_client._is_connected:
                stats.update(self.milvus_client.get_collection_stats())

            return stats
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}

    def cleanup(self) -> None:
        """清理资源。"""
        try:
            # 关闭存储
            if hasattr(self.request_queue, "close"):
                self.request_queue.close()
            if hasattr(self.success_log_queue, "close"):
                self.success_log_queue.close()
            if hasattr(self.state_storage, "close"):
                self.state_storage.close()

            # 断开 Milvus 连接
            self.milvus_client.disconnect()

            logger.info("Framework cleanup completed")
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")
            raise
