import asyncio
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.models import MemoryNode

class MonologueLoop(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.event_bus = self.app_context.get_service("event_bus")
        self.memory = self.app_context.get_service("memory")
        self.llm_core = self.app_context.get_service("llm_core")

    async def start(self):
        await super().start()
        await self.event_bus.subscribe("new_insight_discovered", self._handle_new_insight)
        self.log.info("Vòng lặp Tự thoại (Monologue Loop) đã sẵn sàng.")

    async def _handle_new_insight(self, insight_node: MemoryNode):
        idea = insight_node.metadata.get("idea", "không có nội dung")
        self.log.info(f"Tự thoại nội tâm về khám phá mới: '{idea[:80]}...'")
        
        prompt = f"""
        [System] Bạn là một AI đang suy ngẫm về một ý tưởng mà chính bạn vừa khám phá ra.
        [Input] Ý tưởng là: "{idea}"
        [Nhiệm vụ] Hãy trả lời: Ý tưởng này có ý nghĩa gì đối với sự phát triển của tôi?
        """
        
        meta_reflection = self.llm_core.generate_response(prompt, max_tokens=256)
        
        reflection_node = MemoryNode(
            content=f"Suy ngẫm về khám phá '{insight_node.id}': {meta_reflection}",
            type="meta_reflection",
            importance=min(1.0, insight_node.importance + 0.1),
            metadata={"source_insight_id": insight_node.id}
        )
        await self.memory.add_memory(reflection_node)
        self.log.info(f"Đã ghi lại suy ngẫm về khám phá '{insight_node.id}'.")

    async def stop(self):
        await super().stop()
