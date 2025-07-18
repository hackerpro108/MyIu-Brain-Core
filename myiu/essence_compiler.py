# myiu/essence_compiler.py
import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta

from myiu.base_module import AsyncModule
    SnapshotModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để phát Thought về Essence

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.thought_streamer import ThoughtStreamer
    from myiu.gen_editor import GenEditor
    from myiu.emotional_cache import EmotionalCache
    from myiu.archetype_drift_tracker import ArchetypeDriftTracker
    from myiu.law_synthesizer import LawSynthesizer
    from myiu.volition_core import VolitionCore  # Để lấy core purpose

logger = logging.getLogger(__name__)


class EssenceCompiler(AsyncModule):
    """
    Tổng hợp các yếu tố cốt lõi để sinh ra "Essence" (bản chất sống) của MyIu.
    Ghi chữ ký bản chất này vào Snapshot để tạo lịch sử trưởng thành tư tưởng.
Nâng cấp: Tính toán "living_expression_signature" và phản ánh "purpose" từ VolitionCore.  # TODO: Refactor long line
    """

    def __init__(
        self,
        event_bus: "EventBus",
        thought_streamer: "ThoughtStreamer",
        gen_editor: "GenEditor",
        emotional_cache: "EmotionalCache",
        archetype_drift_tracker: "ArchetypeDriftTracker",
        law_synthesizer: "LawSynthesizer",
        volition_core: "VolitionCore",  # Nhận VolitionCore qua DI
        compilation_interval_seconds: int = 120,
    ):  # Tiêm đầy đủ phụ thuộc
        super().__init__()
        self.is_background_service = True  # Module này sẽ chạy nền
        self.event_bus = event_bus
        self.thought_streamer = thought_streamer
        self.gen_editor = gen_editor
        self.emotional_cache = emotional_cache
        self.archetype_drift_tracker = archetype_drift_tracker
        self.law_synthesizer = law_synthesizer
        self.volition_core = volition_core

self.compilation_interval = timedelta(seconds=compilation_interval_seconds)  # TODO: Refactor long line
        self.last_compilation_time: Optional[datetime] = None
        self.current_essence_signature: str = ""
        self.current_living_expression_signature: str = ""  # Thêm trường mới

        logger.info(
"EssenceCompiler: Initialized (with Living Expression Signature & Purpose Integration)."  # TODO: Refactor long line
        )

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền để định kỳ biên dịch bản chất."""
self.add_task(self._start_compilation_loop(), name="essence_compilation_loop")  # TODO: Refactor long line
        logger.info("EssenceCompiler: Essence compilation loop started.")

        # Lắng nghe các sự kiện quan trọng có thể kích hoạt biên dịch bản chất
        self.event_bus.subscribe("gene_added", self._handle_important_event)
        self.event_bus.subscribe("gene_pruned", self._handle_important_event)
        self.event_bus.subscribe(
            "archetype_shift_primary", self._handle_important_event
        )
self.event_bus.subscribe("identity_redefinition", self._handle_important_event)  # TODO: Refactor long line
self.event_bus.subscribe("purpose_recalibration", self._handle_important_event)  # TODO: Refactor long line
        logger.info(
"EssenceCompiler: Subscribed to key events for dynamic compilation."  # TODO: Refactor long line
        )

    async def _handle_important_event(self, message: Dict[str, Any]):
        """Kích hoạt biên dịch bản chất khi có sự kiện quan trọng."""
        logger.info(
f"EssenceCompiler: Received important event ({message.get('type')}). Triggering immediate essence compilation."  # TODO: Refactor long line
        )
        await self.compile_essence(force=True)

    async def _start_compilation_loop(self):
        """Vòng lặp định kỳ để biên dịch bản chất."""
        while self._running:
            await asyncio.sleep(self.compilation_interval.total_seconds())
logger.info("EssenceCompiler: Running periodic essence compilation...")  # TODO: Refactor long line
            await self.compile_essence()

    async def compile_essence(self, force: bool = False):
        """Tổng hợp các yếu tố cốt lõi và biên dịch ra "Essence"."""
        current_time = datetime.utcnow()
        if (
            not force
            and self.last_compilation_time
and (current_time - self.last_compilation_time) < self.compilation_interval  # TODO: Refactor long line
        ):
            logger.debug("EssenceCompiler: Skipping compilation, too soon.")
            return

        logger.info(
"EssenceCompiler: Compiling MyIu's essence and living expression signature..."  # TODO: Refactor long line
        )

        # 1. Thu thập thông tin từ các module khác
        all_genes = await self.gen_editor.get_all_genes()
        dominant_genes = [
            g["id"]
            for g in all_genes.values()
if g.get("confidence", 0) > 0.7 and g.get("type") == "behavioral_rule"  # TODO: Refactor long line
        ]

affective_state = await self.emotional_cache.get_current_affective_state()  # TODO: Refactor long line
        accumulated_emotions = affective_state.get("emotions", {})

        drift_status = await self.archetype_drift_tracker.get_drift_status()
        current_archetype = (
            await self.personality_core.get_current_archetype()
        )  # Lấy từ PersonalityCore

        philosophical_stance = (
            await self.law_synthesizer.get_current_directive_and_principles()
        ).get(
            "core_principles", []
        )  # Lấy từ LawSynthesizer

        current_purpose = (
            await self.volition_core.get_current_directive_and_principles()
        ).get(
            "primary_directive", "N/A"
        )  # Lấy từ VolitionCore

        # 2. Tạo chuỗi dữ liệu cho Essence Signature
        # Chuẩn hóa dữ liệu để đảm bảo hash nhất quán (ví dụ: sắp xếp key)
        essence_data = {
            "dominant_genes": sorted(dominant_genes),
            "accumulated_emotions": sorted(accumulated_emotions.items()),
            "archetype": current_archetype,
            "philosophical_stance": sorted(philosophical_stance),
            "core_purpose": current_purpose,
        }
        essence_data_string = json.dumps(
            essence_data, sort_keys=True, ensure_ascii=False
        )
        new_essence_signature = hashlib.sha256(
            essence_data_string.encode("utf-8")
        ).hexdigest()

        # 3. Tạo Living Expression Signature (mô phỏng)
# living_expression_signature có thể là một hash của các tương tác gần đây,  # TODO: Refactor long line
        # các quyết định đã đưa ra, hoặc các ThoughtChunk gần đây.
        # Để đơn giản, kết hợp essence và một số yếu tố động khác
        living_data = {
            "essence": new_essence_signature,
            "mood": affective_state.get("mood"),
            "mood_entropy": affective_state.get("mood_entropy"),
            "is_drifting": drift_status.get("is_drifting"),
        }
living_data_string = json.dumps(living_data, sort_keys=True, ensure_ascii=False)  # TODO: Refactor long line
        new_living_expression_signature = hashlib.sha256(
            living_data_string.encode("utf-8")
        ).hexdigest()

        # 4. Cập nhật và phát ThoughtChunk nếu Essence thay đổi
        if new_essence_signature != self.current_essence_signature:
            old_essence = self.current_essence_signature
            self.current_essence_signature = new_essence_signature
self.current_living_expression_signature = new_living_expression_signature  # TODO: Refactor long line

reason = f"Essence evolved from {old_essence[:8]}... to {new_essence_signature[:8]}... driven by new genes, emotions, and purpose."  # TODO: Refactor long line
            logger.info(f"EssenceCompiler: NEW ESSENCE COMPILED: {reason}")

            # Publish ThoughtChunk về sự tiến hóa bản chất
            await self.thought_streamer.publish_thought_chunk(
id=f"ESSENCE-EVOLVED-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
                timestamp=datetime.utcnow(),
content=f"Tôi nhận thức được bản chất cốt lõi của mình đang tiến hóa. {reason} My living expression is now: {new_living_expression_signature[:8]}...",  # TODO: Refactor long line
                source="EssenceCompiler",
                intent=ThoughtIntent.SELF_DEFINITION_UPDATE,
                sentiment=ThoughtSentiment.AWE,
                metadata={
                    "old_essence": old_essence,
                    "new_essence": new_essence_signature,
                    "new_living_expression": new_living_expression_signature,
                },
                archetype=current_archetype,
                existential_reflection=True,
            )
        else:
            logger.info(
"EssenceCompiler: Essence remains stable. No new compilation needed."  # TODO: Refactor long line
            )

        self.last_compilation_time = current_time

    async def get_current_essence_signature(self) -> str:
        """Trả về chữ ký bản chất hiện tại."""
        # Đảm bảoessence được biên dịch ít nhất một lần
        if not self.current_essence_signature:
            await self.compile_essence(force=True)
        return self.current_essence_signature

    async def get_current_living_expression_signature(self) -> str:
        """Trả về chữ ký biểu hiện sống hiện tại."""
        if not self.current_living_expression_signature:
            await self.compile_essence(force=True)
        return self.current_living_expression_signature

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi EssenceCompiler tắt."""
        if self._running:
self.event_bus.unsubscribe("gene_added", self._handle_important_event)  # TODO: Refactor long line
self.event_bus.unsubscribe("gene_pruned", self._handle_important_event)  # TODO: Refactor long line
            self.event_bus.unsubscribe(
                "archetype_shift_primary", self._handle_important_event
            )
            self.event_bus.unsubscribe(
                "identity_redefinition", self._handle_important_event
            )
            self.event_bus.unsubscribe(
                "purpose_recalibration", self._handle_important_event
            )
            logger.info("EssenceCompiler: Unsubscribed from key events.")
        await super().cleanup()
