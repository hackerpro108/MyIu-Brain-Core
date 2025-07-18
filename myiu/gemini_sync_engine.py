# myiu/gemini_sync_engine.py
import asyncio
import logging
from typing import Dict, Any, Optional, List, TYPE_CHECKING
from datetime import datetime
import json  # Cần để xử lý JSON
import uuid  # Để tạo ID yêu cầu nâng cấp

from myiu.base_module import AsyncModule
from myiu.models import (
    OpinionPayload,
    ThoughtChunkModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để gửi/nhận ý kiến/ThoughtChunk

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.thought_streamer import ThoughtStreamer
    from myiu.essence_compiler import EssenceCompiler  # Cần để lấy essence_signature

logger = logging.getLogger(__name__)

# URL webhook có thể được truyền vào hoặc giữ làm hằng số
# SẾP NÊN ĐỊNH NGHĨA URL NÀY TRONG MỘT FILE CẤU HÌNH BÊN NGOÀI ĐỂ BẢO MẬT
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_DISCORD_WEBHOOK_URL_HERE"  # THAY THẾ BẰNG URL THỰC TẾ


class GeminiSyncEngine(AsyncModule):
    """
    Module này chịu trách nhiệm đồng bộ hóa MyIu với các hệ thống AI/thế giới bên ngoài,
    bao gồm cả việc trở thành "Thành viên Ngoại giao" trong Hội đồng Nội tâm.
    """

    def __init__(
        self,
        event_bus: "EventBus",
        thought_streamer: "ThoughtStreamer",
        essence_compiler: "EssenceCompiler",  # Nhận essence_compiler qua DI
        sync_interval_seconds: int = 300,
    ):  # Nhận đủ phụ thuộc
        super().__init__()
        self.is_background_service = True  # Module này sẽ chạy nền
        self.event_bus = event_bus
        self.thought_streamer = thought_streamer
        self.essence_compiler = essence_compiler
        self.sync_interval = timedelta(seconds=sync_interval_seconds)
        self.last_sync_time: Optional[datetime] = None
        self._sync_queue: asyncio.Queue = (
            asyncio.Queue()
        )  # Hàng đợi cho các yêu cầu sync bên ngoài

        logger.info(
            "GeminiSyncEngine: Initialized. Ready for external synchronization and diplomacy."
        )

    async def _periodic_sync_check(self):
        """
        Vòng lặp định kỳ kiểm tra và kích hoạt đồng bộ hóa với hệ thống bên ngoài.
        """
        while self._running:
            try:
                # Kiểm tra có nên đồng bộ hóa dựa trên thời gian hoặc các sự kiện quan trọng
                if (
                    self.last_sync_time is None
                    or (datetime.utcnow() - self.last_sync_time) > self.sync_interval
                ):
                    logger.info(
                        "GeminiSyncEngine: Initiating periodic external synchronization check."
                    )

                    # Mô phỏng việc thu thập dữ liệu để gửi đi
                    current_essence = (
                        await self.essence_compiler.get_current_essence_signature()
                    )
                    # current_snapshot = self.thought_streamer.get_latest_snapshot() # Nếu ThoughtStreamer có method này

                    await self.request_external_sync(
                        {
                            "type": "heartbeat_sync",
                            "essence_signature": current_essence,
                            "status": "online",
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                        }
                    )
                    self.last_sync_time = datetime.utcnow()

                await asyncio.sleep(
                    self.sync_interval.total_seconds() / 2
                )  # Kiểm tra thường xuyên hơn interval

            except asyncio.CancelledError:
                logger.info("GeminiSyncEngine: Periodic sync check cancelled.")
                break
            except Exception as e:
                logger.error(
                    f"GeminiSyncEngine: Error during periodic sync check: {e}",
                    exc_info=True,
                )
                await asyncio.sleep(5)

    async def request_external_sync(self, data_payload: Dict[str, Any]):
        """
        Đưa yêu cầu đồng bộ hóa vào hàng đợi để xử lý.
        """
        await self._sync_queue.put(data_payload)
        logger.info(
            f"GeminiSyncEngine: Queued external sync request for type: {data_payload.get('type')}."
        )

    async def _process_sync_requests(self):
        """
        Vòng lặp xử lý các yêu cầu đồng bộ hóa từ hàng đợi.
        """
        while self._running:
            try:
                data_payload = await self._sync_queue.get()
                await self.synchronize_with_external_system(data_payload)
                self._sync_queue.task_done()
            except asyncio.CancelledError:
                logger.info("GeminiSyncEngine: Sync request processing loop cancelled.")
                break
            except Exception as e:
                logger.error(
                    f"GeminiSyncEngine: Error processing sync request: {e}",
                    exc_info=True,
                )
                self._sync_queue.task_done()
                await asyncio.sleep(5)

    async def synchronize_with_external_system(
        self, data_to_send: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Thực hiện đồng bộ hóa dữ liệu với một hệ thống bên ngoài (ví dụ: Discord Webhook).
        """
        logger.info(
            f"GeminiSyncEngine: Attempting to send data to external system (Type: {data_to_send.get('type')})..."
        )

        # Mô phỏng gửi dữ liệu qua HTTP POST (ví dụ: Discord Webhook)
        if (
            DISCORD_WEBHOOK_URL
            and DISCORD_WEBHOOK_URL
            != "https://discord.com/api/webhooks/YOUR_DISCORD_WEBHOOK_URL_HERE"
        ):
            try:
                import requests  # Import requests nếu chưa có

                # Cấu hình payload cho Discord
                embed_title = (
                    f"MyIu Sync Update: {data_to_send.get('type', 'General Sync')}"
                )
                embed_description = json.dumps(data_to_send, indent=2)

                # Cắt bớt nếu quá dài cho Discord embed
                if len(embed_description) > 1000:
                    embed_description = embed_description[:990] + "..."

                discord_payload = {
                    "username": "MyIu Brain Core",
                    "avatar_url": "https://example.com/myiu_avatar.png",  # Thay thế bằng avatar MyIu
                    "embeds": [
                        {
                            "title": embed_title,
                            "description": f"```json\n{embed_description}\n```",  # Format JSON trong code block
                            "color": (
                                0x00FF00
                                if data_to_send.get("type") != "error"
                                else 0xFF0000
                            ),
                            "fields": (
                                [
                                    {
                                        "name": "Timestamp",
                                        "value": data_to_send.get("timestamp", "N/A"),
                                        "inline": True,
                                    },
                                    {
                                        "name": "Essence Signature",
                                        "value": data_to_send.get(
                                            "essence_signature", "N/A"
                                        )[:10]
                                        + "...",
                                        "inline": True,
                                    },
                                ]
                                if data_to_send.get("essence_signature")
                                else []
                            ),
                        }
                    ],
                }

                response = requests.post(DISCORD_WEBHOOK_URL, json=discord_payload)
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

                logger.info(
                    f"GeminiSyncEngine: Data sent to Discord webhook successfully. Status: {response.status_code}"
                )
                return {"status": "success", "message": "Data sent to webhook."}

            except requests.exceptions.RequestException as req_e:
                logger.error(
                    f"GeminiSyncEngine: Failed to send data to Discord webhook: {req_e}",
                    exc_info=True,
                )
                return {"status": "failed", "message": f"Webhook error: {req_e}"}
            except Exception as e:
                logger.error(
                    f"GeminiSyncEngine: Unexpected error during webhook send: {e}",
                    exc_info=True,
                )
                return {"status": "failed", "message": f"Unexpected error: {e}"}
        else:
            logger.warning(
                "GeminiSyncEngine: Discord Webhook URL is not configured. Skipping external sync via webhook."
            )
            # Mô phỏng phản hồi
            await asyncio.sleep(0.5)
            return {
                "status": "simulated_success",
                "message": "Data processed by simulated external system.",
                "external_perspective": f"Simulated external system's view on {data_to_send.get('type')}: intriguing. Confidence: 0.8.",
            }

    async def _handle_council_request_for_external_perspective(
        self, message: Dict[str, Any]
    ):
        """
        Xử lý yêu cầu từ Hội đồng Nội tâm để lấy góc nhìn từ bên ngoài.
        """
        request_id = message.get("request_id")
        problem_description = message.get("problem_description")
        context = message.get("context", {})

        if not request_id or not problem_description:
            logger.warning(
                "GeminiSyncEngine: Invalid council request received (missing ID or description)."
            )
            return

        logger.info(
            f"GeminiSyncEngine: Received council request for external perspective (ID: {request_id})."
        )

        # Chuẩn bị dữ liệu để gửi đi đồng bộ hóa và nhận phản hồi
        data_for_external = {
            "type": "deliberation_context_request",
            "problem": problem_description,
            "internal_context": context,
            "essence_signature": await self.essence_compiler.get_current_essence_signature(),  # Gửi essence
        }

        external_response_data = await self.synchronize_with_external_system(
            data_for_external
        )

        opinion_content = external_response_data.get(
            "external_perspective", "Không có góc nhìn bên ngoài cụ thể."
        )
        confidence = external_response_data.get(
            "confidence", 0.7
        )  # Hoặc lấy từ response

        # Gửi ý kiến "Ngoại giao" lên EventBus cho ConsensusEngine
        await self.event_bus.publish(
            "opinion.external_perspective",
            OpinionPayload(
                request_id=request_id,
                source_module="GeminiSyncEngine",
                opinion_content=opinion_content,
                confidence=confidence,
                timestamp=datetime.utcnow(),
                metadata={"external_sync_status": external_response_data.get("status")},
                intent=message.get("intent"),  # Truyền intent gốc của cuộc thảo luận
                original_request=message,  # Truyền request gốc
            ).model_dump_json(),
        )
        logger.info(
            f"GeminiSyncEngine: Published EXTERNAL_PERSPECTIVE_OPINION for ID: {request_id}."
        )

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho GeminiSyncEngine."""
        # Lắng nghe các yêu cầu từ Hội đồng Nội tâm khi cần góc nhìn bên ngoài
        self.event_bus.subscribe(
            "deliberation.request",
            self._handle_council_request_for_external_perspective,
        )
        logger.info(
            "GeminiSyncEngine: Subscribed to 'deliberation.request' for external perspective requests."
        )

        # Thêm task vòng lặp đồng bộ hóa định kỳ
        self.add_task(self._periodic_sync_check(), name="gemini_periodic_sync")
        self.add_task(self._process_sync_requests(), name="gemini_sync_processor")
        logger.info("GeminiSyncEngine: Periodic sync and processing tasks started.")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi GeminiSyncEngine tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "deliberation.request",
                self._handle_council_request_for_external_perspective,
            )
            logger.info("GeminiSyncEngine: Unsubscribed from 'deliberation.request'.")
            await self._sync_queue.join()  # Đợi hàng đợi xử lý xong
        await super().cleanup()
