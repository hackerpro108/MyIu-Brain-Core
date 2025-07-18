kk  # myiu/log_manager.py
import asyncio
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List, TYPE_CHECKING
import re  # Để khớp các tên file log

from myiu.base_module import AsyncModule

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    ThoughtStreamer,
)  # Có thể cần nếu muốn log errors dưới dạng ThoughtChunk  # TODO: Refactor long line  # TODO: Refactor long line


class LogManager(AsyncModule):
    """
    Log Manager chịu trách nhiệm định kỳ quét và xóa các file log cũ
trong các thư mục được quản lý để tiết kiệm dung lượng lưu trữ trên máy chủ.  # TODO: Refactor long line  # TODO: Refactor long line
    Nó cũng có thể lắng nghe các sự kiện lỗi hệ thống để ghi log đặc biệt.
    """

    def __init__(
        self,
        event_bus: "EventBus",
        log_dir: str = "data/",
        retention_days: int = 7,
        cleanup_interval_hours: int = 12,
    ):  # Tiêm đủ phụ thuộc  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = (
True  # Module này sẽ chạy nền để dọn dẹp log  # TODO: Refactor long line  # TODO: Refactor long line
        )
        self.event_bus = event_bus
        self.log_dir = log_dir
        self.retention_delta = timedelta(days=retention_days)
        self.cleanup_interval_sec = cleanup_interval_hours * 3600

# Danh sách các file log hoặc pattern log mà LogManager sẽ quản lý và dọn dẹp  # TODO: Refactor long line  # TODO: Refactor long line
        self.managed_log_patterns: List[str] = [
            r"myiu_error_full_log\.txt$",  # Log lỗi chính
            r"reflection_log\.txt$",  # Log phản tư của MonologueLoop
            r"access\.log$",  # Ví dụ: log truy cập web server
            r"error\.log$",  # Ví dụ: log lỗi web server
r"\.log$",  # Bất kỳ file nào kết thúc bằng .log (cẩn thận khi sử dụng)  # TODO: Refactor long line  # TODO: Refactor long line
        ]

        logger.info(
f"LogManager: Initialized. Managing logs in '{log_dir}', retaining for {retention_days} days."  # TODO: Refactor long line
        )  # TODO: Refactor long line

        # Đảm bảo thư mục log tồn tại
        os.makedirs(self.log_dir, exist_ok=True)

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền để chạy dọn dẹp log định kỳ."""
        self.add_task(self._start_cleanup_loop(), name="periodic_log_cleanup")
        logger.info("LogManager: Periodic log cleanup loop started.")

        # Lắng nghe các sự kiện lỗi hệ thống nghiêm trọng
        self.event_bus.subscribe(
            "system.critical_error", self._handle_critical_system_error
        )  # TODO: Refactor long line
        logger.info(
"LogManager: Subscribed to 'system.critical_error' for emergency logging."  # TODO: Refactor long line
        )  # TODO: Refactor long line

    async def _start_cleanup_loop(self):
        """Vòng lặp chính để thực hiện dọn dẹp log định kỳ."""
        while self._running:
            await asyncio.sleep(self.cleanup_interval_sec)  # Chạy mỗi X giờ
            logger.info("LogManager: Running periodic log cleanup...")
            await self.perform_log_cleanup()

    async def perform_log_cleanup(self):
        """Thực hiện quy trình quét và xóa các file log cũ."""
        now = datetime.utcnow()
        for filename in os.listdir(self.log_dir):
            file_path = os.path.join(self.log_dir, filename)

            if os.path.isfile(file_path):
                is_managed_log = False
                for pattern in self.managed_log_patterns:
                    if re.search(pattern, filename):
                        is_managed_log = True
                        break

                if not is_managed_log:
# logger.debug(f"LogManager: Skipping unmanaged file: {filename}")  # TODO: Refactor long line  # TODO: Refactor long line
                    continue

                file_modified_time = datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                )  # TODO: Refactor long line

                if (now - file_modified_time) > self.retention_delta:
                    try:
                        os.remove(file_path)
                        logger.info(
                            f"LogManager: Deleted old log file: {file_path}"
                        )  # TODO: Refactor long line
                    except OSError as e:
                        logger.error(
f"LogManager ERROR: Could not delete log file '{file_path}': {e}",  # TODO: Refactor long line
                            exc_info=True,
                        )  # TODO: Refactor long line
                # else:
# logger.debug(f"LogManager: Keeping log file: {filename} (Modified {file_modified_time.strftime('%Y-%m-%d')})")  # TODO: Refactor long line  # TODO: Refactor long line

    async def _handle_critical_system_error(self, message: Dict[str, Any]):
        """
        Lắng nghe sự kiện lỗi hệ thống nghiêm trọng và ghi log khẩn cấp.
        """
            ThoughtChunkModel,
            ThoughtIntent,
            ThoughtSentiment,
        )  # Import cục bộ  # TODO: Refactor long line

        error_message = message.get("message", "Unknown critical error")
        details = message.get("details", "No details provided")
        component = message.get("component", "Unknown")
        timestamp = message.get(
            "timestamp", datetime.utcnow().isoformat() + "Z"
        )  # TODO: Refactor long line

        log_entry = (
            f"[{timestamp}] - CRITICAL SYSTEM ERROR detected in {component}:\n"
            f"  Message: {error_message}\n"
            f"  Details: {details}\n"
            f"---"
        )

        error_log_file = os.path.join(self.log_dir, "myiu_critical_errors.log")
        try:
            with open(error_log_file, "a", encoding="utf-8") as f:
                f.write(log_entry + "\n")
            logger.critical(
f"LogManager: Recorded CRITICAL SYSTEM ERROR to {error_log_file}."  # TODO: Refactor long line
            )  # TODO: Refactor long line
        except Exception as e:
            logger.exception(
                f"LogManager: Failed to write critical error to log file: {e}"
            )  # TODO: Refactor long line

        # Tạo ThoughtChunk về lỗi nghiêm trọng
# Cần kiểm tra app_context.thought_streamer có tồn tại không trước khi dùng  # TODO: Refactor long line  # TODO: Refactor long line
        from myiu.app_context import app_context  # Import cục bộ

        if app_context.thought_streamer:
            await app_context.thought_streamer.publish_thought_chunk(
                id=f"SYSTEM-CRITICAL-ERROR-{timestamp}",
                timestamp=datetime.utcnow(),
content=f"Lỗi hệ thống nghiêm trọng trong '{component}': {error_message}",  # TODO: Refactor long line  # TODO: Refactor long line
                source="LogManager",
                intent=ThoughtIntent.SYSTEM_ERROR,
                sentiment=ThoughtSentiment.NEGATIVE,
                metadata={"error_details": details, "component": component},
            )
        else:
            logger.warning(
"LogManager: Cannot publish critical error thought chunk, ThoughtStreamer not available."  # TODO: Refactor long line
            )  # TODO: Refactor long line

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi LogManager tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "system.critical_error", self._handle_critical_system_error
            )  # TODO: Refactor long line
            logger.info(
                "LogManager: Unsubscribed from 'system.critical_error'."
            )  # TODO: Refactor long line
            # Chạy dọn dẹp lần cuối
            await self.perform_log_cleanup()
            logger.info("LogManager: Cleanup complete.")
        await super().cleanup()
