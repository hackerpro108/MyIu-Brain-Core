# myiu/code_quality_assurance.py
from pyflakes.api import checkPath
from pyflakes.reporter import Reporter
import io
import logging

from myiu.base_module import AsyncModule

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myiu.event_bus import EventBus

logger = logging.getLogger(__name__)


class CodeQualityAssurance(AsyncModule):
    """
    Kiểm soát chất lượng mã nguồn nội bộ.
    Nâng cấp: Khi phát hiện lỗi, sẽ phát đi một sự kiện khẩn cấp
    để kích hoạt cơ chế phục hồi tự động.
    """

    def __init__(self, event_bus: "EventBus"):
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus
        logger.info(
"CodeQualityAssurance: Initialized (Upgraded with emergency broadcast)."  # TODO: Refactor long line
        )  # TODO: Refactor long line

    async def _setup_async_tasks(self):
        """Lắng nghe các sự kiện hoàn thành sửa đổi code."""
        self.add_task(self._subscribe_to_code_mutation_events())

    async def _subscribe_to_code_mutation_events(self):
        """Lắng nghe sự kiện từ CodeMutator."""
        request_queue = await self.event_bus.subscribe(
            "CODE_MUTATION_COMPLETED"
        )  # TODO: Refactor long line
        while self._running:
            event_data = await request_queue.get()
            await self.review_code(event_data)

    async def review_code(self, event_data: dict):
"""Sử dụng Pyflakes để kiểm tra chất lượng file code và phát đi sự kiện phù hợp."""  # TODO: Refactor long line  # TODO: Refactor long line
        file_path = event_data.get("file_path")
        backup_path = event_data.get("backup_path")
        if not file_path or not backup_path:
            logger.error("CodeQualityAssurance: Invalid event data received.")
            return

        logger.info(f"CodeQualityAssurance: Reviewing '{file_path}'...")

        error_stream = io.StringIO()
        reporter = Reporter(error_stream, error_stream)

        num_errors = checkPath(file_path, reporter)

        if num_errors > 0:
            errors = error_stream.getvalue()
            logger.critical(
f"CodeQualityAssurance: CRITICAL - {num_errors} issues found in '{file_path}'. Triggering automatic rollback."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            # NÂNG CẤP: Publish sự kiện khẩn cấp để rollback
            await self.event_bus.publish(
                "CODE_INTEGRITY_FAILED",
{"file_path": file_path, "backup_path": backup_path, "errors": errors},  # TODO: Refactor long line
            )
        else:
            logger.info(
f"CodeQualityAssurance: Code quality check passed for '{file_path}'."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await self.event_bus.publish(
                "CODE_QUALITY_PASSED",
                {"file_path": file_path, "backup_path": backup_path},
            )
