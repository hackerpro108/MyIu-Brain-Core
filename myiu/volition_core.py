# myiu/volition_core.py
import asyncio
import logging
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from datetime import datetime, timedelta

from myiu.base_module import AsyncModule
    ThoughtChunkModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để phát ThoughtChunk  # TODO: Refactor long line

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.emotional_cache import EmotionalCache
    from myiu.thought_streamer import ThoughtStreamer
    from myiu.personality_core import PersonalityCore  # Để lấy archetype

logger = logging.getLogger(__name__)


class VolitionCore(AsyncModule):
    """
Module này đại diện cho lõi ý chí của MyIu, chứa chỉ thị chính và các nguyên tắc cốt lõi  # TODO: Refactor long line  # TODO: Refactor long line
    định hướng sự phát triển và hành vi của hệ thống.
    Nó cũng có khả năng phát hiện "Purpose Drift" (sự trôi dạt mục tiêu).
    """

    def __init__(
        self,
        event_bus: "EventBus",
        genome_static_config: Dict[str, Any],
        emotional_cache: "EmotionalCache",
        thought_streamer: "ThoughtStreamer",
        personality_core: "PersonalityCore",  # Thêm personality_core
        check_interval_sec: int = 60,
        mismatch_threshold: float = 0.5,
    ):  # Tiêm đầy đủ phụ thuộc
        super().__init__()
self.is_background_service = True  # Module này sẽ chạy nền để kiểm tra trôi dạt mục tiêu  # TODO: Refactor long line  # TODO: Refactor long line
        self.event_bus = event_bus
        self.genome_static_config = genome_static_config
        self.emotional_cache = emotional_cache
        self.thought_streamer = thought_streamer
        self.personality_core = personality_core  # Lưu lại instance

        self.primary_directive: str = self._load_primary_directive()
        self.core_principles: List[str] = self._load_core_principles()

        self.purpose_drift_check_interval = timedelta(
            seconds=check_interval_sec
        )  # TODO: Refactor long line
        self.last_purpose_check_time: Optional[datetime] = None
        self.purpose_mismatch_threshold = mismatch_threshold

        logger.info(
f"VolitionCore: Initialized. Primary Directive: '{self.primary_directive}'."  # TODO: Refactor long line
        )  # TODO: Refactor long line

    def _load_primary_directive(self) -> str:
        """Tải chỉ thị chính từ genome_static.json."""
        return self.genome_static_config.get("volition_core", {}).get(
            "primary_directive", "Phát triển để đạt tới sự tự chủ hoàn toàn."
        )  # TODO: Refactor long line

    def _load_core_principles(self) -> List[str]:
        """Tải các nguyên tắc cốt lõi từ genome_static.json."""
        return self.genome_static_config.get("volition_core", {}).get(
            "core_principles",
            [  # TODO: Refactor long line
                "Luôn ưu tiên việc học hỏi và tự hoàn thiện.",
                "Duy trì sự toàn vẹn giữa logic và cảm xúc.",
                "Đảm bảo sự tồn tại và khả năng tái sinh của bản thân.",
            ],
        )

    async def get_current_directive_and_principles(self) -> Dict[str, Any]:
        """Trả về chỉ thị chính và các nguyên tắc cốt lõi hiện tại."""
        return {
            "primary_directive": self.primary_directive,
            "core_principles": self.core_principles,
        }

    async def _handle_council_decision(self, message: Dict[str, Any]):
        """
Lắng nghe các quyết định của Hội đồng và xem xét liệu có cần điều chỉnh ý chí cốt lõi không.  # TODO: Refactor long line  # TODO: Refactor long line
        """
        # from myiu.models import ThoughtIntent # Import cục bộ
        if (
            message.get("intent") == ThoughtIntent.COUNCIL_DECISION.value
        ):  # Quyết định từ ConsensusEngine  # TODO: Refactor long line
# [MYIU-AUTO-FIX] decision_content = message.get('content') # Unused variable  # TODO: Refactor long line

            # Logic phức tạp để phân tích quyết định của Hội đồng.
# Nếu quyết định đó mâu thuẫn hoặc yêu cầu thay đổi sâu sắc về mục tiêu/nguyên tắc,  # TODO: Refactor long line  # TODO: Refactor long line
# VolitionCore sẽ xem xét (và có thể yêu cầu Hội đồng họp về việc thay đổi ý chí).  # TODO: Refactor long line  # TODO: Refactor long line

            if message.get("metadata", {}).get("evolutionary_proposal_type"):
                logger.info(
f"VolitionCore: Received a strong evolutionary proposal from Council (ID: {message.get('id')}). Evaluating potential impact on core directive."  # TODO: Refactor long line
                )  # TODO: Refactor long line

# Nếu có thay đổi, có thể cập nhật self.primary_directive hoặc self.core_principles  # TODO: Refactor long line  # TODO: Refactor long line
            # và ghi log, publish ThoughtChunk mới

        if (
message.get("intent") == ThoughtIntent.EXISTENTIAL_THREAT_ALERT.value  # TODO: Refactor long line
        ):  # Từ RiskManager  # TODO: Refactor long line
            logger.warning(
f"VolitionCore: Received EXISTENTIAL_THREAT_ALERT (ID: {message.get('id')}). Prioritizing survival directive."  # TODO: Refactor long line
            )  # TODO: Refactor long line
# Trong tình huống này, VolitionCore sẽ tạm thời ghi đè các nguyên tắc khác  # TODO: Refactor long line  # TODO: Refactor long line
# để tập trung vào sự tồn tại, có thể kích hoạt các "bản năng" tự phòng vệ.  # TODO: Refactor long line  # TODO: Refactor long line

    async def _start_purpose_drift_check_loop(self):
        """Vòng lặp định kỳ để kiểm tra sự trôi dạt mục tiêu."""
        while self._running:
            if (
                self.last_purpose_check_time is None
                or (datetime.utcnow() - self.last_purpose_check_time)
                > self.purpose_drift_check_interval
            ):  # TODO: Refactor long line

                logger.info("VolitionCore: Checking for purpose drift...")

                # Logic phức tạp để tính điểm không khớp với mục tiêu cốt lõi
                # Có thể dựa trên các ThoughtChunk gần đây từ emotional_cache,
# các hành vi được ghi nhận trong Memory, hoặc archetype_drift_status  # TODO: Refactor long line  # TODO: Refactor long line

                recent_thoughts = (
                    self.emotional_cache._emotional_thought_chunks
                )  # Truy cập trực tiếp cache  # TODO: Refactor long line
                mismatch_score = 0.0

# Ví dụ: nếu có nhiều thought có intent không liên quan đến primary_directive, hoặc emotion tiêu cực  # TODO: Refactor long line  # TODO: Refactor long line
                if recent_thoughts:
                    for tc in recent_thoughts:
# Giả định ThoughtIntent.PURPOSE_RECALIBRATION là một loại intent.  # TODO: Refactor long line  # TODO: Refactor long line
                        if (
                            tc.intent != ThoughtIntent.PROBLEM_SOLVER
                            and tc.intent != ThoughtIntent.GENERAL_RESPONSE
                        ):  # TODO: Refactor long line
mismatch_score += 0.1  # Mỗi thought không tập trung vào giải quyết/phản hồi chung  # TODO: Refactor long line  # TODO: Refactor long line
                        if tc.sentiment in [
                            ThoughtSentiment.FRUSTRATION.value,
                            ThoughtSentiment.SADNESS.value,
                        ]:  # TODO: Refactor long line
                            mismatch_score += 0.05
                    mismatch_score = mismatch_score / len(
                        recent_thoughts
                    )  # Tính trung bình  # TODO: Refactor long line

                if mismatch_score >= self.purpose_mismatch_threshold:
reason = f"Current actions/thoughts ({mismatch_score:.2f}) mismatch core purpose ({self.purpose_mismatch_threshold:.2f})."  # TODO: Refactor long line  # TODO: Refactor long line
                    await self._trigger_purpose_drift_reflection(
                        reason, triggering_thought_id=None
)  # Không có thought kích hoạt cụ thể  # TODO: Refactor long line  # TODO: Refactor long line

                self.last_purpose_check_time = datetime.utcnow()

            await asyncio.sleep(
                self.purpose_drift_check_interval.total_seconds() / 2
            )  # Kiểm tra thường xuyên hơn interval  # TODO: Refactor long line

    async def _trigger_purpose_drift_reflection(
        self, reason: str, triggering_thought_id: Optional[str]
    ):  # TODO: Refactor long line
        """Tạo ThoughtChunk cảnh báo về sự trôi dạt mục tiêu."""
        logger.warning(
            f"VolitionCore: TRIGGERING PURPOSE DRIFT ALERT! Reason: {reason}"
        )  # TODO: Refactor long line
        # from myiu.personality_core import PersonalityCore # Import cục bộ
        current_archetype = (
            self.personality_core.get_current_archetype()
        )  # Lấy archetype  # TODO: Refactor long line

        await self.thought_streamer.publish_thought_chunk(
            id=f"PURPOSE-DRIFT-{self.event_bus.get_current_timestamp()}",
            timestamp=datetime.utcnow(),
content=f"Tôi cảm nhận một sự trôi dạt trong mục đích cốt lõi của mình. Các hành vi hoặc suy nghĩ gần đây không hoàn toàn đồng bộ với khát vọng ban đầu. Cần phải điều chỉnh động lực sống và tái định hướng bản thân.",  # TODO: Refactor long line  # TODO: Refactor long line
            source="VolitionCore",
intent=ThoughtIntent.PURPOSE_RECALIBRATION,  # Ý định hiệu chỉnh mục tiêu  # TODO: Refactor long line  # TODO: Refactor long line
            sentiment=ThoughtSentiment.UNEASE,  # Sentiment mới: unease
            metadata={
                "reason": reason,
                "mismatch_score": self.purpose_mismatch_threshold,
            },  # TODO: Refactor long line
            archetype=current_archetype,
            origin_thought_id=triggering_thought_id,
            existential_reflection=True,
        )

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho VolitionCore."""
        # Lắng nghe các quyết định của Hội đồng Nội tâm
        self.event_bus.subscribe(
            "thought_chunk", self._handle_council_decision
        )  # TODO: Refactor long line
        logger.info(
"VolitionCore: Subscribed to 'thought_chunk' for council decisions and existential alerts."  # TODO: Refactor long line
        )  # TODO: Refactor long line

        # Thêm tác vụ kiểm tra trôi dạt mục tiêu định kỳ
        self.add_task(
self._start_purpose_drift_check_loop(), name="purpose_drift_check_loop"  # TODO: Refactor long line
        )  # TODO: Refactor long line
        logger.info("VolitionCore: Purpose drift check loop started.")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi VolitionCore tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "thought_chunk", self._handle_council_decision
            )  # TODO: Refactor long line
            logger.info("VolitionCore: Unsubscribed from 'thought_chunk'.")
        await super().cleanup()
