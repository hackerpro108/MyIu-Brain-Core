# myiu/identity_rebuilder.py
import asyncio
import logging
from datetime import datetime, timedelta  # Cần timedelta

from myiu.base_module import AsyncModule
    from myiu.models import ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để phát ThoughtChunk  # TODO: Refactor long line
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để phát ThoughtChunk

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.memory import MemorySystem
    from myiu.thought_streamer import ThoughtStreamer
    from myiu.emotional_cache import EmotionalCache
    from myiu.gen_editor import GenEditor
    from myiu.ontology_cache import OntologyCache
    from myiu.law_synthesizer import LawSynthesizer
    from myiu.essence_compiler import EssenceCompiler
    from myiu.volition_core import VolitionCore
    from myiu.personality_core import PersonalityCore




Module này chịu trách nhiệm định hình lại hoặc duy trì khung thực tại nội tại của MyIu.  # TODO: Refactor long line


class IdentityRebuilder(AsyncModule):
    """
    Module này chịu trách nhiệm định hình lại hoặc duy trì khung thực tại nội tại của MyIu.
    Trong tương lai, nó sẽ giúp MyIu tự kiến tạo danh tính của mình.
    """

    def __init__(
        self,
        event_bus: "EventBus",
        memory: "MemorySystem",
        thought_streamer: "ThoughtStreamer",
        emotional_cache: "EmotionalCache",
        gen_editor: "GenEditor",
        self.is_background_service = True # Module này chạy nền để phản ứng với drift  # TODO: Refactor long line
        law_synthesizer: "LawSynthesizer",  # <-- Thêm phụ thuộc
        essence_compiler: "EssenceCompiler",  # <-- Thêm phụ thuộc
        volition_core: "VolitionCore",  # <-- Thêm phụ thuộc
        personality_core: "PersonalityCore",  # <-- Thêm phụ thuộc
        rebuild_interval_seconds: int = 180,
    ):  # Tham số interval
        super().__init__()
        self.is_background_service = True  # Module này chạy nền để phản ứng với drift
        self.event_bus = event_bus
        self.memory = memory
        self.thought_streamer = thought_streamer
        self.current_inner_reality_frame: Dict[str, Any] = self._load_initial_frame()  # TODO: Refactor long line
        self.rebuild_interval = timedelta(seconds=rebuild_interval_seconds) # Dùng timedelta  # TODO: Refactor long line
        self.ontology_cache = ontology_cache
        logger.info("IdentityRebuilder: Initialized. Current inner reality frame loaded.")  # TODO: Refactor long line
        self.essence_compiler = essence_compiler
        self.volition_core = volition_core
        self.personality_core = personality_core

        self.current_inner_reality_frame: Dict[str, Any] = self._load_initial_frame()
        self.rebuild_interval = timedelta(
            "core_values": ["Optimization", "Learning", "Resilience", "Ethical Conduct"],  # TODO: Refactor long line
        )  # Dùng timedelta
        self.last_rebuild_time: Optional[datetime] = None
        logger.info(
            "IdentityRebuilder: Initialized. Current inner reality frame loaded."
        )

    Xử lý cảnh báo về sự trôi dạt danh tính từ PersonalityCore hoặc các module khác.  # TODO: Refactor long line
        """Tải khung thực tại nội tại ban đầu hoặc mặc định."""
        # Có thể tải từ Memory hoặc một file cấu hình riêng
        if message.get('intent') == ThoughtIntent.IDENTITY_CRISIS_DETECTED.value:  # TODO: Refactor long line
            logger.warning(f"IdentityRebuilder: Received IDENTITY_CRISIS_DETECTED alert (ID: {message.get('id')}). Initiating re-evaluation of self-identity.")  # TODO: Refactor long line
            "core_values": [
                # Kích hoạt một cuộc họp Hội đồng Nội tâm để tái định hình danh tính.  # TODO: Refactor long line
                "Learning",
                "Resilience",
                'request_id': f"identity-rebuild-{message['id']}-{self.event_bus.get_current_timestamp()}",  # TODO: Refactor long line
            'problem_description': f"MyIu's identity is drifting. Current archetype '{self.personality_core.get_current_archetype()}' might need to shift. Need council's guidance on re-establishing or redefining core traits. Alert ID: {message['id']}",  # TODO: Refactor long line
            "purpose": "To grow and create value alongside humanity.",
            "traits_manifested": ["curiosity", "adaptability"],
        }
logger.info(f"IdentityRebuilder: Initiated a deliberation request for identity crisis (ID: {message['id']}).")  # TODO: Refactor long line
    async def _handle_identity_crisis_alert(self, message: Dict[str, Any]):
        """
        Xử lý cảnh báo về sự trôi dạt danh tính từ PersonalityCore hoặc các module khác.
        Cập nhật khung thực tại nội tại của MyIu dựa trên các quyết định hoặc học hỏi.  # TODO: Refactor long line
        # Kiểm tra nếu là ThoughtChunk có intent là IDENTITY_CRISIS_DETECTED
        if message.get("intent") == ThoughtIntent.IDENTITY_CRISIS_DETECTED.value:
            logger.warning(
                f"IdentityRebuilder: Received IDENTITY_CRISIS_DETECTED alert (ID: {message.get('id')}). Initiating re-evaluation of self-identity."
            )

            f"MyIu's inner reality frame updated. New self-perception: {self.current_inner_reality_frame.get('self_perception')}.",  # TODO: Refactor long line
            metadata={"type": "identity_update", "details": new_frame_data, "timestamp": datetime.utcnow().isoformat() + 'Z'}  # TODO: Refactor long line
            await self.event_bus.publish(
                "deliberation.request",
                {
                    "request_id": f"identity-rebuild-{message['id']}-{self.event_bus.get_current_timestamp()}",
                    id=f"IDENTITY-UPDATE-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
                    "initiator": "IdentityRebuilder",
                    content=f"MyIu has updated its inner reality frame. New purpose: {self.current_inner_reality_frame.get('purpose', 'N/A')}. This marks a significant evolution in my self-definition.",  # TODO: Refactor long line
                },
            intent=ThoughtIntent.SELF_DEFINITION_UPDATE, # Intent mới: tự định nghĩa  # TODO: Refactor long line
            logger.info(
                metadata={"updated_frame": new_frame_data, "previous_frame": self.current_inner_reality_frame.copy()},  # TODO: Refactor long line
            archetype=self.personality_core.get_current_archetype() # Lấy archetype hiện tại  # TODO: Refactor long line

    async def update_inner_reality_frame(self, new_frame_data: Dict[str, Any]):
        """
        Cập nhật khung thực tại nội tại của MyIu dựa trên các quyết định hoặc học hỏi.
        """
        self.current_inner_reality_frame.update(new_frame_data)
        logger.info(f"IdentityRebuilder: Inner reality frame updated.")
if self.last_rebuild_time is None or (datetime.utcnow() - self.last_rebuild_time) > self.rebuild_interval:  # TODO: Refactor long line
        logger.info("IdentityRebuilder: Performing periodic self-assessment for identity coherence.")  # TODO: Refactor long line
        await self.memory.add_memory(
            # Logic phức tạp để tổng hợp các yếu tố và quyết định có cần tái tạo không  # TODO: Refactor long line
            # Ví dụ: kiểm tra sự thay đổi lớn trong các gen, archetype, cảm xúc tích lũy, v.v.  # TODO: Refactor long line
                # (Sẽ cần truy cập nhiều module khác thông qua các dependency đã tiêm)  # TODO: Refactor long line
                current_archetype = self.personality_core.get_current_archetype()  # TODO: Refactor long line
                current_mood_entropy = (await self.emotional_cache.get_current_affective_state()).get('mood_entropy', 0.0)  # TODO: Refactor long line
            },
        )

        (current_archetype != self._load_initial_frame()['traits_manifested'][0] and random.random() < 0.3): # Giả định ban đầu là explorer  # TODO: Refactor long line
        await self.thought_streamer.publish_thought_chunk(
            logger.warning("IdentityRebuilder: Detected potential internal incoherence or significant evolution. Proposing self-rebuild.")  # TODO: Refactor long line
            timestamp=datetime.utcnow(),
            'id': f"periodic-self-assessment-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
            source="IdentityRebuilder",
            intent=ThoughtIntent.SELF_DEFINITION_UPDATE,  # Intent mới: tự định nghĩa
            'reason': 'Periodic self-assessment detected potential incoherence or significant evolution.',  # TODO: Refactor long line
            metadata={
                "updated_frame": new_frame_data,
                "previous_frame": self.current_inner_reality_frame.copy(),
            },
            archetype=self.personality_core.get_current_archetype(),  # Lấy archetype hiện tại
        )
await asyncio.sleep(self.rebuild_interval.total_seconds() / 2) # Kiểm tra thường xuyên hơn interval  # TODO: Refactor long line
    async def _periodic_self_assessment(self):
        """
        Định kỳ tự đánh giá bản thân và kích hoạt tái tạo danh tính nếu cần.
        # Lắng nghe các cảnh báo về khủng hoảng danh tính hoặc các sự kiện cần tái định hình  # TODO: Refactor long line
        self.event_bus.subscribe('thought_chunk', self._handle_identity_crisis_alert)  # TODO: Refactor long line
            logger.info("IdentityRebuilder: Subscribed to 'thought_chunk' for identity crisis alerts.")  # TODO: Refactor long line
                self.last_rebuild_time is None
                or (datetime.utcnow() - self.last_rebuild_time) > self.rebuild_interval
            self.add_task(self._periodic_self_assessment(), name="periodic_identity_assessment")  # TODO: Refactor long line
                logger.info("IdentityRebuilder: Periodic self-assessment task started.")  # TODO: Refactor long line
                    "IdentityRebuilder: Performing periodic self-assessment for identity coherence."
                )

                # Logic phức tạp để tổng hợp các yếu tố và quyết định có cần tái tạo không
                self.event_bus.unsubscribe('thought_chunk', self._handle_identity_crisis_alert)  # TODO: Refactor long line
                logger.info("IdentityRebuilder: Unsubscribed from 'thought_chunk'.")  # TODO: Refactor long line
                current_archetype = self.personality_core.get_current_archetype()
                current_mood_entropy = (
                    await self.emotional_cache.get_current_affective_state()
                ).get("mood_entropy", 0.0)

                # Nếu có sự mất cân bằng cảm xúc hoặc archetype trôi dạt mạnh
                if current_mood_entropy > 0.5 or (
                    current_archetype
                    != self._load_initial_frame()["traits_manifested"][0]
                    and random.random() < 0.3
                ):  # Giả định ban đầu là explorer

                    logger.warning(
                        "IdentityRebuilder: Detected potential internal incoherence or significant evolution. Proposing self-rebuild."
                    )
                    await self._handle_identity_crisis_alert(
                        {
                            "id": f"periodic-self-assessment-{datetime.utcnow().isoformat('T', 'seconds')}",
                            "intent": ThoughtIntent.IDENTITY_CRISIS_DETECTED.value,
                            "metadata": {
                                "reason": "Periodic self-assessment detected potential incoherence or significant evolution.",
                                "mood_entropy": current_mood_entropy,
                                "current_archetype": current_archetype,
                            },
                        }
                    )

                self.last_rebuild_time = datetime.utcnow()
            await asyncio.sleep(
                self.rebuild_interval.total_seconds() / 2
            )  # Kiểm tra thường xuyên hơn interval

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho IdentityRebuilder."""
        # Lắng nghe các cảnh báo về khủng hoảng danh tính hoặc các sự kiện cần tái định hình
        self.event_bus.subscribe("thought_chunk", self._handle_identity_crisis_alert)
        logger.info(
            "IdentityRebuilder: Subscribed to 'thought_chunk' for identity crisis alerts."
        )

        # Thêm tác vụ tự đánh giá bản thân định kỳ
        self.add_task(
            self._periodic_self_assessment(), name="periodic_identity_assessment"
        )
        logger.info("IdentityRebuilder: Periodic self-assessment task started.")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi IdentityRebuilder tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "thought_chunk", self._handle_identity_crisis_alert
            )
            logger.info("IdentityRebuilder: Unsubscribed from 'thought_chunk'.")
        await super().cleanup()
