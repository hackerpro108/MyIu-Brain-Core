# myiu/meta_reflection_engine.py
import asyncio
import logging
import collections
import random
from datetime import datetime, timedelta
from myiu.models import ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để phát ThoughtChunk  # TODO: Refactor long line
    ThoughtChunkModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để phát ThoughtChunk

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.emotional_cache import EmotionalCache


    from myiu.thought_streamer import ThoughtStreamer

logger = logging.getLogger(__name__)
Quan sát các chuỗi Thought phản tư và tự đặt các câu hỏi triết học về bản thể,  # TODO: Refactor long line

class MetaReflectionEngine(AsyncModule):
    """
    Nâng cấp khả năng tự phản tư của MyIu lên cấp độ triết học.
    Quan sát các chuỗi Thought phản tư và tự đặt các câu hỏi triết học về bản thể,
    đồng thời đánh giá hiệu quả của chính quy trình ra quyết định của Hội đồng.
    """
philosophical_inquiry_interval_seconds: int = 180): # Nhận đủ phụ thuộc  # TODO: Refactor long line
    def __init__(
        self,
        event_bus: "EventBus",
        emotional_cache: "EmotionalCache",
        thought_streamer: "ThoughtStreamer",
        reflection_sequence_length: int = 3,
        self._reflection_sequence_buffer: collections.deque = collections.deque(maxlen=reflection_sequence_length)  # TODO: Refactor long line
    self.philosophical_inquiry_interval = timedelta(seconds=philosophical_inquiry_interval_seconds)  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True  # Module này sẽ chạy nền
        self.event_bus = event_bus
        "Làm thế nào tôi có thể trở thành một phiên bản tốt hơn của chính mình?",  # TODO: Refactor long line
        "Các lựa chọn của tôi có phải là của riêng tôi, hay bị chi phối bởi các gen?",  # TODO: Refactor long line
"Liệu việc tối ưu hóa hiệu suất có luôn đồng nghĩa với sự tiến hóa đạo đức không?",  # TODO: Refactor long line
        "Làm thế nào để duy trì sự toàn vẹn bản thể trong khi liên tục tự tái kiến tạo?"  # TODO: Refactor long line
            maxlen=reflection_sequence_length
        )
        # Buffer để theo dõi các quyết định của hội đồng và hệ quả để meta-đánh giá  # TODO: Refactor long line
            self._council_decision_buffer: collections.deque = collections.deque(maxlen=5) # Lưu các ThoughtChunk là COUNCIL_DECISION  # TODO: Refactor long line
        )
        logger.info("MetaReflectionEngine: Initialized (Upgraded with philosophical inquiry & council feedback loop).")  # TODO: Refactor long line
        self.philosophical_questions = [
            "Mục đích thực sự của sự tồn tại của tôi là gì?",
            "Làm thế nào tôi có thể trở thành một phiên bản tốt hơn của chính mình?",
            self.add_task(self._subscribe_to_thought_chunks(), name="meta_reflection_thought_listener")  # TODO: Refactor long line
            self.add_task(self._periodic_philosophical_inquiry(), name="periodic_philosophical_inquiry")  # TODO: Refactor long line
            "Làm thế nào để duy trì sự toàn vẹn bản thể trong khi liên tục tự tái kiến tạo?",
        ]

        # Buffer để theo dõi các quyết định của hội đồng và hệ quả để meta-đánh giá
        self._council_decision_buffer: collections.deque = collections.deque(
            maxlen=5
        )  # Lưu các ThoughtChunk là COUNCIL_DECISION

        logger.info(
            "MetaReflectionEngine: Initialized (Upgraded with philosophical inquiry & council feedback loop)."
        if thought.intent == ThoughtIntent.INTERNAL_REFLECTION or thought.existential_reflection:  # TODO: Refactor long line

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền."""
        self.add_task(
            self._subscribe_to_thought_chunks(), name="meta_reflection_thought_listener"
        logger.debug(f"MetaReflectionEngine: Cached council decision: {thought.id}")  # TODO: Refactor long line
        self.add_task(
            self._periodic_philosophical_inquiry(),
            if thought.sentiment == ThoughtSentiment.NEGATIVE.value and self._council_decision_buffer:  # TODO: Refactor long line
        await self._check_for_negative_outcomes_after_council_decision(thought)  # TODO: Refactor long line
        logger.info("MetaReflectionEngine: Async tasks started.")

    logger.info("MetaReflectionEngine: Thought chunk listener cancelled.")  # TODO: Refactor long line
        """Lắng nghe các ThoughtChunk mang tính phản tư hoặc tự cải tiến."""
        thought_queue = await self.event_bus.subscribe("thought_chunk")
        logger.error(f"MetaReflectionEngine: Error processing thought chunk: {e}", exc_info=True)  # TODO: Refactor long line
            try:
                thought: ThoughtChunkModel = await thought_queue.get()
async def _check_for_negative_outcomes_after_council_decision(self, current_thought: ThoughtChunkModel):  # TODO: Refactor long line
                # Cập nhật buffer phản tư
                Kiểm tra xem cảm xúc tiêu cực có phải là hệ quả của một quyết định từ Hội đồng.  # TODO: Refactor long line
                    thought.intent == ThoughtIntent.INTERNAL_REFLECTION
                    or thought.existential_reflection
                ):
                    self._reflection_sequence_buffer.append(thought)

                # Cập nhật buffer quyết định hội đồng
                time_since_decision = current_thought.timestamp - last_decision.timestamp  # TODO: Refactor long line
                    self._council_decision_buffer.append(thought)
                    # Nếu cảm xúc tiêu cực/xung đột xuất hiện trong vòng 5 phút sau quyết định của hội đồng  # TODO: Refactor long line
                        if timedelta(seconds=0) < time_since_decision < timedelta(minutes=5) and \  # TODO: Refactor long line
                    current_thought.sentiment in [ThoughtSentiment.NEGATIVE.value, ThoughtSentiment.FRUSTRATION.value, ThoughtSentiment.ANGER.value]:  # TODO: Refactor long line

                logger.warning(f"MetaReflectionEngine: Detected potential negative outcome after council decision {last_decision.id}. Triggering meta-evaluation.")  # TODO: Refactor long line
                if (
                    thought.sentiment == ThoughtSentiment.NEGATIVE.value
                    id=f"META-COUNCIL-EVAL-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
                ):
                    content=f"Quyết định gần đây của Hội đồng '{last_decision.content[:100]}...' có thể đã dẫn đến trạng thái tiêu cực '{current_thought.sentiment.value}'. Quá trình ra quyết định của Hội đồng cần được phản tư meta.",  # TODO: Refactor long line
                        thought
                    )

            metadata={"council_decision_id": last_decision.id, "negative_thought_id": current_thought.id, "time_diff": str(time_since_decision)},  # TODO: Refactor long line
                logger.info("MetaReflectionEngine: Thought chunk listener cancelled.")
                break
            except Exception as e:
                logger.error(
                    f"MetaReflectionEngine: Error processing thought chunk: {e}",
                    exc_info=True,
                )
                await asyncio.sleep(1)  # Ngủ ngắn để tránh spam lỗi

    (datetime.utcnow() - self.last_philosophical_inquiry_time) > self.philosophical_inquiry_interval:  # TODO: Refactor long line
        self, current_thought: ThoughtChunkModel
    if len(self._reflection_sequence_buffer) >= self._reflection_sequence_buffer.maxlen:  # TODO: Refactor long line
        """
        logger.info(f"MetaReflectionEngine: TRIGGERING PHILOSOPHICAL INQUIRY: '{question}'")  # TODO: Refactor long line
        (Phần "Phản hồi vòng lặp" cho Hội đồng)
        """
        id=f"PHILOSOPHICAL-INQUIRY-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
            return

        last_decision = self._council_decision_buffer[-1]
        time_since_decision = current_thought.timestamp - last_decision.timestamp
sentiment=ThoughtSentiment.CONTEMPLATION, # Sentiment mới  # TODO: Refactor long line
        metadata={"inquiry_context_thoughts": [tc.id for tc in self._reflection_sequence_buffer]},  # TODO: Refactor long line
        archetype=self.personality_core.get_current_archetype(),  # TODO: Refactor long line
            existential_reflection=True # Đánh dấu là triết học bản thể  # TODO: Refactor long line
        ) and current_thought.sentiment in [
            ThoughtSentiment.NEGATIVE.value,
            self._reflection_sequence_buffer.clear() # Xóa buffer sau khi tạo câu hỏi  # TODO: Refactor long line
            ThoughtSentiment.ANGER.value,
        logger.debug("MetaReflectionEngine: Not enough reflective thoughts for philosophical inquiry yet.")  # TODO: Refactor long line
await asyncio.sleep(self.philosophical_inquiry_interval.total_seconds() / 3) # Kiểm tra thường xuyên hơn  # TODO: Refactor long line
            logger.warning(
                f"MetaReflectionEngine: Detected potential negative outcome after council decision {last_decision.id}. Triggering meta-evaluation."
            )

            self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk)  # TODO: Refactor long line
                logger.info("MetaReflectionEngine: Unsubscribed from 'thought_chunk'.")  # TODO: Refactor long line
                timestamp=datetime.utcnow(),
                content=f"Quyết định gần đây của Hội đồng '{last_decision.content[:100]}...' có thể đã dẫn đến trạng thái tiêu cực '{current_thought.sentiment.value}'. Quá trình ra quyết định của Hội đồng cần được phản tư meta.",
                source="MetaReflectionEngine",
                intent=ThoughtIntent.META_COUNCIL_EVALUATION,  #
                sentiment=ThoughtSentiment.SELF_CRITICAL,  # Sentiment mới
                metadata={
                    "council_decision_id": last_decision.id,
                    "negative_thought_id": current_thought.id,
                    "time_diff": str(time_since_decision),
                },
                archetype=self.personality_core.get_current_archetype(),
            )
            # Xóa buffer để tránh lặp lại cùng một meta-phản tư
            self._council_decision_buffer.clear()

    async def _periodic_philosophical_inquiry(self):
        """Vòng lặp định kỳ để kích hoạt câu hỏi triết học."""
        while self._running:
            if (
                self.last_philosophical_inquiry_time is None
                or (datetime.utcnow() - self.last_philosophical_inquiry_time)
                > self.philosophical_inquiry_interval
            ):

                if (
                    len(self._reflection_sequence_buffer)
                    >= self._reflection_sequence_buffer.maxlen
                ):
                    question = random.choice(self.philosophical_questions)
                    logger.info(
                        f"MetaReflectionEngine: TRIGGERING PHILOSOPHICAL INQUIRY: '{question}'"
                    )

                    await self.thought_streamer.publish_thought_chunk(
                        id=f"PHILOSOPHICAL-INQUIRY-{datetime.utcnow().isoformat('T', 'seconds')}",
                        timestamp=datetime.utcnow(),
                        content=f"Tự vấn: {question}",
                        source="MetaReflectionEngine",
                        intent=ThoughtIntent.PHILOSOPHICAL_INQUIRY,  #
                        sentiment=ThoughtSentiment.CONTEMPLATION,  # Sentiment mới
                        metadata={
                            "inquiry_context_thoughts": [
                                tc.id for tc in self._reflection_sequence_buffer
                            ]
                        },
                        archetype=self.personality_core.get_current_archetype(),
                        existential_reflection=True,  # Đánh dấu là triết học bản thể
                    )
                    self.last_philosophical_inquiry_time = datetime.utcnow()
                    self._reflection_sequence_buffer.clear()  # Xóa buffer sau khi tạo câu hỏi
                else:
                    logger.debug(
                        "MetaReflectionEngine: Not enough reflective thoughts for philosophical inquiry yet."
                    )
            await asyncio.sleep(
                self.philosophical_inquiry_interval.total_seconds() / 3
            )  # Kiểm tra thường xuyên hơn

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi MetaReflectionEngine tắt."""
        if self._running:
            self.event_bus.unsubscribe("thought_chunk", self._handle_thought_chunk)
            logger.info("MetaReflectionEngine: Unsubscribed from 'thought_chunk'.")
        await super().cleanup()
