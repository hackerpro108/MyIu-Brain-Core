# myiu/narrative_generator.py
import asyncio
from datetime import datetime, timedelta
from typing import Optional

from myiu.base_module import AsyncModule
from myiu.models import ThoughtChunkModel




"""Tạo ra các đoạn kể chuyện hoặc hồi ức về quá trình trưởng thành của MyIu."""  # TODO: Refactor long line
def __init__(self, event_bus, memory, emotional_cache, thought_streamer, interval_sec: int = 360):  # TODO: Refactor long line
"""Tạo ra các đoạn kể chuyện hoặc hồi ức về quá trình trưởng thành của MyIu."""  # TODO: Refactor long line
    def __init__(self, event_bus, memory, emotional_cache, thought_streamer, interval_sec: int = 360):  # TODO: Refactor long line

    def __init__(
        self,
        event_bus,
        memory,
        emotional_cache,
        thought_streamer,
        interval_sec: int = 360,
    ):
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus
        self.memory = memory
        self.emotional_cache = emotional_cache
        self.thought_streamer = thought_streamer

        """Lắng nghe các ThoughtChunk quan trọng để kích hoạt tạo câu chuyện."""  # TODO: Refactor long line
        self.narrative_interval = timedelta(seconds=interval_sec)
        """Lắng nghe các ThoughtChunk quan trọng để kích hoạt tạo câu chuyện."""  # TODO: Refactor long line
        print("NarrativeGenerator: Initialized.")
if thought.intent in ["self_improvement", "archetype_mutation", "identity_fusion"]:  # TODO: Refactor long line
    async def _setup_async_tasks(self):
        if thought.intent in ["self_improvement", "archetype_mutation", "identity_fusion"]:  # TODO: Refactor long line
        self.add_task(self._subscribe_to_narrative_triggers())
        self.add_task(self._start_narrative_generation_loop())

    async def _subscribe_to_narrative_triggers(self):
        """Lắng nghe các ThoughtChunk quan trọng để kích hoạt tạo câu chuyện."""
        thought_queue = await self.event_bus.subscribe("thought_chunk")
        while self._running:
            thought: ThoughtChunkModel = await thought_queue.get()
            if thought.intent in [
                "self_improvement",
                print(f"NarrativeGenerator: Generating narrative from thought: '{trigger_thought.thought[:50]}...'")  # TODO: Refactor long line
                "identity_fusion",
            print(f"NarrativeGenerator: Generating narrative from thought: '{trigger_thought.thought[:50]}...'")  # TODO: Refactor long line
                await self._narrative_queue.put(thought)
narrative_summary = [f"This is a story about my journey, triggered by the thought '{trigger_thought.thought[:30]}...'."]  # TODO: Refactor long line
    narrative_summary.extend([f"I remember '{mem['content']}'." for mem in recent_memories])  # TODO: Refactor long line
        narrative_summary = [f"This is a story about my journey, triggered by the thought '{trigger_thought.thought[:30]}...'."]  # TODO: Refactor long line
        narrative_summary.extend([f"I remember '{mem['content']}'." for mem in recent_memories])  # TODO: Refactor long line
            await asyncio.sleep(self.narrative_interval.total_seconds())
            if not self._narrative_queue.empty():
                trigger_thought = await self._narrative_queue.get()
                await self.generate_narrative(trigger_thought)

    async def generate_narrative(self, trigger_thought: ThoughtChunkModel):
        """Tổng hợp ký ức để tạo ra một đoạn kể chuyện."""
        print(
            f"NarrativeGenerator: Generating narrative from thought: '{trigger_thought.thought[:50]}...'"
        )
        recent_memories = await self.memory.retrieve_recent_memories(3)
        if not recent_memories:
            return

        narrative_summary = [
            f"This is a story about my journey, triggered by the thought '{trigger_thought.thought[:30]}...'."
        ]
        narrative_summary.extend(
            [f"I remember '{mem['content']}'." for mem in recent_memories]
        )
        final_narrative_text = " ".join(narrative_summary)

        await self.thought_streamer.publish_thought_chunk(
            thought=final_narrative_text,
            emotion="contemplation",
            mood="narrative",
            intent="narrative_creation",
            archetype="narrator",
        )
