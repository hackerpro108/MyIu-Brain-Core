import asyncio
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.emotional_cache import EmotionalCache

class Affect(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.emotional_cache: EmotionalCache = None
    async def start(self):
        await super().start()
        self.emotional_cache = self.app_context.get_service("emotional_cache")
        if self.emotional_cache:
            self.log.info("Affect Layer ready and connected to EmotionalCache.")
    def trigger_emotion(self, name: str, intensity: float):
        if self.emotional_cache:
            asyncio.create_task(self.emotional_cache.boost_emotion(name, intensity))
    async def get_current_state(self) -> dict:
        return await self.emotional_cache.get_affective_state() if self.emotional_cache else {}
