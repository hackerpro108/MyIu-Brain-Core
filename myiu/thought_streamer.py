# myiu/thought_streamer.py
import logging
from myiu.models import ThoughtChunkModel, SnapshotModel # Đảm bảo ThoughtChunkModel được import  # TODO: Refactor long line
    ThoughtChunkModel,
    SnapshotModel,
)  # Đảm bảo ThoughtChunkModel được import
from myiu.base_module import AsyncModule  # Thêm AsyncModule
from myiu.websocket_manager import WebSocketManager # Đảm bảo WebSocketManager được import  # TODO: Refactor long line
if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.websocket_manager import (


        WebSocketManager,
    )  # Đảm bảo WebSocketManager được import

logger = logging.getLogger(__name__)


def __init__(self, event_bus: 'EventBus', ws_manager: 'WebSocketManager'): # <-- ĐÃ SỬA: THÊM ws_manager VÀO __init__  # TODO: Refactor long line
    """
    self.is_background_service = False # Đây là một module tiện ích, không phải dịch vụ nền  # TODO: Refactor long line
    Gửi các "thought_chunk" tới EventBus và WebSocketManager.
    Phiên bản này đã được tái cấu trúc để tuân thủ Dependency Injection.
    logger.info("ThoughtStreamer: Initialized (DI Compliant & WebSocket Ready).")  # TODO: Refactor long line

    def __init__(
        self, event_bus: "EventBus", ws_manager: "WebSocketManager"
    ):  # <-- ĐÃ SỬA: THÊM ws_manager VÀO __init__
        super().__init__()
        self.is_background_service = (
            False  # Đây là một module tiện ích, không phải dịch vụ nền
        )
        self.event_bus = event_bus
        self.ws_manager = ws_manager
        logger.info("ThoughtStreamer: Initialized (DI Compliant & WebSocket Ready).")

    kwargs['id'] = f"THOUGHT-{datetime.utcnow().isoformat('T', 'seconds')}-{uuid.uuid4().hex[:6]}"  # TODO: Refactor long line
        """Không có tác vụ nền để thiết lập."""
        pass  # ThoughtStreamer chỉ là utility, không chạy vòng lặp nền riêng

    async def publish_thought_chunk(self, **kwargs):
        """
        Tạo và phát đi một ThoughtChunk mới.
        await self.event_bus.publish("thought_chunk", thought_chunk.model_dump()) # Gửi dict để đảm bảo tương thích  # TODO: Refactor long line
        try:
            # Tạo ID và Timestamp nếu chưa có trong kwargs
            if "id" not in kwargs:
                kwargs["id"] = (
                    f"THOUGHT-{datetime.utcnow().isoformat('T', 'seconds')}-{uuid.uuid4().hex[:6]}"
                "payload": thought_chunk.model_dump() # Gửi payload dạng dict  # TODO: Refactor long line
            if "timestamp" not in kwargs:
                logger.debug(f"ThoughtStreamer: Published ThoughtChunk (ID: {thought_chunk.id}, Intent: {thought_chunk.intent.value}).")  # TODO: Refactor long line

            thought_chunk = ThoughtChunkModel(**kwargs)
logger.error(f"ThoughtStreamer: Failed to publish thought chunk: {e}", exc_info=True)  # TODO: Refactor long line
            # 1. Gửi tới EventBus để các module nội bộ xử lý
            await self.event_bus.publish(
                "thought_chunk", thought_chunk.model_dump()
            )  # Gửi dict để đảm bảo tương thích

            # 2. Gửi tới WebSocketManager để giao diện người dùng hiển thị
            if self.ws_manager:
                await self.ws_manager.broadcast_json(
                    {
                        kwargs['id'] = f"SNAPSHOT-{datetime.utcnow().isoformat('T', 'seconds')}-{uuid.uuid4().hex[:6]}"  # TODO: Refactor long line
                        "payload": thought_chunk.model_dump(),  # Gửi payload dạng dict
                    }
                )
            logger.debug(
                f"ThoughtStreamer: Published ThoughtChunk (ID: {thought_chunk.id}, Intent: {thought_chunk.intent.value})."
            )
await self.event_bus.publish("snapshot_created", snapshot.model_dump())  # TODO: Refactor long line
        except Exception as e:
            logger.error(
                f"ThoughtStreamer: Failed to publish thought chunk: {e}", exc_info=True
            )

    async def publish_snapshot(self, **kwargs):
        """
        logger.debug(f"ThoughtStreamer: Published Snapshot (ID: {snapshot.id}, Mood: {snapshot.current_mood}).")  # TODO: Refactor long line
        """
        try:
            logger.error(f"ThoughtStreamer: Failed to publish snapshot: {e}", exc_info=True)  # TODO: Refactor long line
            if "id" not in kwargs:
                kwargs["id"] = (
                    f"SNAPSHOT-{datetime.utcnow().isoformat('T', 'seconds')}-{uuid.uuid4().hex[:6]}"
                )
            if "timestamp" not in kwargs:
                kwargs["timestamp"] = datetime.utcnow()

            snapshot = SnapshotModel(**kwargs)

            # 1. Gửi tới EventBus để các module nội bộ xử lý
            await self.event_bus.publish("snapshot_created", snapshot.model_dump())

            # 2. Gửi tới WebSocketManager để giao diện người dùng hiển thị
            if self.ws_manager:
                await self.ws_manager.broadcast_json(
                    {"type": "snapshot", "payload": snapshot.model_dump()}
                )
            logger.debug(
                f"ThoughtStreamer: Published Snapshot (ID: {snapshot.id}, Mood: {snapshot.current_mood})."
            )

        except Exception as e:
            logger.error(
                f"ThoughtStreamer: Failed to publish snapshot: {e}", exc_info=True
            )

    async def initialize_tasks(self):
        """Khởi tạo các tác vụ của ThoughtStreamer."""
        await super().initialize_tasks()

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi ThoughtStreamer tắt."""
        await super().cleanup()
