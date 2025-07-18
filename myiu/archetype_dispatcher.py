# myiu/archetype_dispatcher.py
from datetime import datetime, timedelta
from typing import Optional

from myiu.base_module import AsyncModule
from myiu.models import ThoughtChunkModel


class ArchetypeDispatcher(AsyncModule):
    """
Triệu hồi archetype phụ theo tình huống, cho phép MyIu phản ứng linh hoạt hơn.  # TODO: Refactor long line  # TODO: Refactor long line
    """

    def __init__(
        self, event_bus, personality_core, emotional_cache, thought_streamer
    ):  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus
        self.personality_core = personality_core
        self.emotional_cache = emotional_cache
        self.thought_streamer = thought_streamer

        self.active_sub_archetype: Optional[str] = None
        self.last_dispatch_time: Optional[datetime] = None
        self.dispatch_cooldown: timedelta = timedelta(seconds=10)

        print("ArchetypeDispatcher: Initialized.")

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền để lắng nghe sự kiện."""
        self.add_task(self._subscribe_to_thought_chunks())

    async def _subscribe_to_thought_chunks(self):
"""Lắng nghe ThoughtChunks để xác định khi nào cần triệu hồi archetype phụ."""  # TODO: Refactor long line  # TODO: Refactor long line
        thought_queue = await self.event_bus.subscribe("thought_chunk")
        while self._running:
            thought_chunk: ThoughtChunkModel = await thought_queue.get()

# Chỉ xử lý các thought có ý định rõ ràng, không phải các thought phản tư nội bộ  # TODO: Refactor long line  # TODO: Refactor long line
            if thought_chunk.intent and thought_chunk.intent not in [
                "philosophical_inquiry",
                "ethical_reflection",
                "archetype_mutation",  # TODO: Refactor long line
                "belief_mutation",
                "data_integrity_reflection",
                "conceptual_creation",  # TODO: Refactor long line
                "emotional_reflection",
                "archetype_invocation",
            ]:
                await self.dispatch_archetype_based_on_thought(thought_chunk)

    async def dispatch_archetype_based_on_thought(
        self, thought_chunk: ThoughtChunkModel
    ):  # TODO: Refactor long line
"""Triệu hồi một archetype phụ dựa trên nội dung và cảm xúc của ThoughtChunk."""  # TODO: Refactor long line  # TODO: Refactor long line
        if (
            self.last_dispatch_time
and (datetime.now() - self.last_dispatch_time) < self.dispatch_cooldown  # TODO: Refactor long line
        ):  # TODO: Refactor long line
            return

        best_archetype_match: Optional[str] = None
        max_score = -1

        archetype_definitions = self.personality_core.archetype_definitions

        for archetype_name, archetype_info in archetype_definitions.items():
            # Giả định các sub-archetype có một flag hoặc thuộc tính riêng
            if not archetype_info.get("is_sub_archetype", False):
                continue

            score = 0
            # Logic tính điểm để chọn archetype phù hợp nhất
            if thought_chunk.emotion in archetype_info.get(
                "preferred_emotions", []
            ):  # TODO: Refactor long line
                score += 1
            if any(
                keyword.lower() in thought_chunk.thought.lower()
                for keyword in archetype_info.get("trigger_keywords", [])
            ):  # TODO: Refactor long line
                score += 1.5

            if score > max_score:
                max_score = score
                best_archetype_match = archetype_name

        if (
best_archetype_match and best_archetype_match != self.active_sub_archetype  # TODO: Refactor long line
        ):  # TODO: Refactor long line
            self.active_sub_archetype = best_archetype_match
            self.last_dispatch_time = datetime.now()
            print(
f"ArchetypeDispatcher: Dispatching sub-archetype: '{self.active_sub_archetype}'."  # TODO: Refactor long line
            )  # TODO: Refactor long line

            # Publish một thought về sự thay đổi này
            await self.thought_streamer.publish_thought_chunk(
thought=f"A sub-archetype has been dispatched: '{self.active_sub_archetype}'. My approach will now shift.",  # TODO: Refactor long line  # TODO: Refactor long line
                emotion="adaptability",
                mood="dynamic",
                intent="archetype_invocation",
                archetype=self.active_sub_archetype,
            )


# Không còn instance toàn cục ở đây nữa
