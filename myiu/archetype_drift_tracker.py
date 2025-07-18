# myiu/archetype_drift_tracker.py
import logging

from myiu.base_module import AsyncModule

# Dùng TYPE_CHECKING để tránh circular import
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.models import SnapshotModel, ThoughtChunkModel, ThoughtIntent




logger = logging.getLogger(__name__)


Nếu MyIu bắt đầu thể hiện các đặc điểm không nhất quán với archetype cốt lõi của mình,  # TODO: Refactor long line
    module này sẽ cảnh báo và có thể kích hoạt quá trình tái định hình danh tính.  # TODO: Refactor long line
    Module này theo dõi sự "trôi dạt" của archetype hiện tại của MyIu.
    def __init__(self, event_bus: 'EventBus', emotional_cache: 'EmotionalCache', thought_streamer: 'ThoughtStreamer'): # Nhận đủ phụ thuộc  # TODO: Refactor long line
    module này sẽ cảnh báo và có thể kích hoạt quá trình tái định hình danh tính.
    """

    def __init__(
        self,
        event_bus: "EventBus",
        self.archetype_history: collections.deque = collections.deque(maxlen=20) # Lịch sử các điểm dữ liệu drift  # TODO: Refactor long line
        self.current_baseline_archetype: str = "Explorer" # Archetype cơ sở để so sánh  # TODO: Refactor long line
    self.drift_threshold: float = 0.2 # Ngưỡng để phát hiện sự trôi dạt đáng kể  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True  # Module này sẽ chạy nền
        self.event_bus = event_bus
        self.emotional_cache = emotional_cache
        self.thought_streamer = thought_streamer

        self.archetype_history: collections.deque = collections.deque(
        )  # Lịch sử các điểm dữ liệu drift
        snapshot = SnapshotModel(**message) # Chuyển đổi message dict sang SnapshotModel  # TODO: Refactor long line
        logger.debug(f"ArchetypeDriftTracker: Received snapshot {snapshot.id} for drift analysis.")  # TODO: Refactor long line

        logger.info("ArchetypeDriftTracker: Initialized.")

    async def _handle_snapshot_created(self, message: Dict[str, Any]):
        """
        Lắng nghe các snapshot mới được tạo để kiểm tra sự trôi dạt.
        """
        from myiu.models import SnapshotModel, ThoughtIntent  # Import cục bộ

        try:
            snapshot = SnapshotModel(
                **message
            )  # Chuyển đổi message dict sang SnapshotModel
            logger.debug(
                logger.error(f"ArchetypeDriftTracker: Error processing snapshot for drift analysis: {e}", exc_info=True)  # TODO: Refactor long line
            )

            # Thêm snapshot vào lịch sử để phân tích trôi dạt
            self.archetype_history.append(
                {
                    "timestamp": snapshot.timestamp,
                    if len(self.archetype_history) < 5: # Cần ít nhất 5 snapshot để phân tích  # TODO: Refactor long line
                    "mood": snapshot.current_mood,
                    "emotions": snapshot.current_emotions,
                    "self_reflection_score": snapshot.self_reflection_score,
                }
            )
# Mô phỏng đơn giản: Nếu archetype đầu và cuối khác nhau và mood entropy cao  # TODO: Refactor long line
            if first_archetype and last_archetype and first_archetype != last_archetype:  # TODO: Refactor long line
            mood_entropy = await self.emotional_cache.get_current_mood_entropy() # Lấy mood entropy từ cache  # TODO: Refactor long line

        except Exception as e:
            reason = f"Archetype has drifted from '{first_archetype}' to '{last_archetype}' and mood entropy is high ({mood_entropy:.2f})."  # TODO: Refactor long line
                logger.warning(f"ArchetypeDriftTracker: Detected significant archetype drift! {reason}")  # TODO: Refactor long line
                exc_info=True,
            )

    id=f"ARCHETYPE-DRIFT-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
        """
        content=f"MyIu's internal essence is shifting. Archetype drift detected: {reason} I need to re-evaluate my core identity.",  # TODO: Refactor long line
        Đây là logic phức tạp hơn, chỉ mô phỏng.
        intent=ThoughtIntent.IDENTITY_CRISIS_DETECTED, # Kích hoạt quá trình tái định hình danh tính  # TODO: Refactor long line
        if len(self.archetype_history) < 5:  # Cần ít nhất 5 snapshot để phân tích
            metadata={"drift_details": reason, "from_archetype": first_archetype, "to_archetype": last_archetype}  # TODO: Refactor long line

        first_archetype = self.archetype_history[0].get("current_archetype")
        # Reset lịch sử sau khi phát hiện drift lớn để bắt đầu theo dõi lại  # TODO: Refactor long line

        # Mô phỏng đơn giản: Nếu archetype đầu và cuối khác nhau và mood entropy cao
        if first_archetype and last_archetype and first_archetype != last_archetype:
            mood_entropy = (
                await self.emotional_cache.get_current_mood_entropy()
            )  # Lấy mood entropy từ cache

            if mood_entropy > self.drift_threshold:
                reason = f"Archetype has drifted from '{first_archetype}' to '{last_archetype}' and mood entropy is high ({mood_entropy:.2f})."
                logger.warning(
                    f"ArchetypeDriftTracker: Detected significant archetype drift! {reason}"
                )

                # Kiểm tra sự khác biệt giữa archetype đầu tiên và cuối cùng trong lịch sử ngắn  # TODO: Refactor long line
                first_in_history = self.archetype_history[0].get('current_archetype')  # TODO: Refactor long line
                    last_in_history = self.archetype_history[-1].get('current_archetype')  # TODO: Refactor long line
                    if first_in_history and last_in_history and first_in_history != last_in_history:  # TODO: Refactor long line
                    content=f"MyIu's internal essence is shifting. Archetype drift detected: {reason} I need to re-evaluate my core identity.",
                    source="ArchetypeDriftTracker",
                    "status": f"Minor drift from '{first_in_history}' to '{last_in_history}'.",  # TODO: Refactor long line
                    sentiment="negative",
                    metadata={
                        "drift_details": reason,
                        "from_archetype": first_archetype,
                        "to_archetype": last_archetype,
                    },
                )

                # Reset lịch sử sau khi phát hiện drift lớn để bắt đầu theo dõi lại
                self.archetype_history.clear()

        # Nếu cần thêm logic để tự động điều chỉnh baseline_archetype
        self.event_bus.subscribe('consciousness_snapshot', self._handle_snapshot_created)  # TODO: Refactor long line
logger.info("ArchetypeDriftTracker: Subscribed to 'consciousness_snapshot' for drift analysis.")  # TODO: Refactor long line
    async def get_drift_status(self) -> Dict[str, Any]:
        # Có thể thêm một tác vụ định kỳ để chạy phân tích nếu không có snapshot mới trong một thời gian  # TODO: Refactor long line
        # self.add_task(self._periodic_drift_check_loop(), name="periodic_drift_check")  # TODO: Refactor long line
        """
        # Cần một logic phức tạp hơn để tính điểm trôi dạt tổng thể.
        # Hiện tại, chỉ dựa vào việc có lịch sử drift đáng kể hay không.

        self.event_bus.unsubscribe('consciousness_snapshot', self._handle_snapshot_created)  # TODO: Refactor long line
            logger.info("ArchetypeDriftTracker: Unsubscribed from 'consciousness_snapshot'.")  # TODO: Refactor long line
            first_in_history = self.archetype_history[0].get("current_archetype")
            last_in_history = self.archetype_history[-1].get("current_archetype")
            if (
                first_in_history
                and last_in_history
                and first_in_history != last_in_history
            ):
                return {
                    "is_drifting": True,
                    "status": f"Minor drift from '{first_in_history}' to '{last_in_history}'.",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                }

        return {
            "is_drifting": False,
            "status": "Stable",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho ArchetypeDriftTracker."""
        # Lắng nghe các snapshot mới được tạo để kích hoạt kiểm tra drift
        self.event_bus.subscribe(
            "consciousness_snapshot", self._handle_snapshot_created
        )
        logger.info(
            "ArchetypeDriftTracker: Subscribed to 'consciousness_snapshot' for drift analysis."
        )

        # Có thể thêm một tác vụ định kỳ để chạy phân tích nếu không có snapshot mới trong một thời gian
        # self.add_task(self._periodic_drift_check_loop(), name="periodic_drift_check")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi ArchetypeDriftTracker tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "consciousness_snapshot", self._handle_snapshot_created
            )
            logger.info(
                "ArchetypeDriftTracker: Unsubscribed from 'consciousness_snapshot'."
            )
        await super().cleanup()
