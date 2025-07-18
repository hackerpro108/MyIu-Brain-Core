import asyncio
import logging
import signal
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from myiu.base_module import AsyncModule
from myiu.event_bus import EventBus
from myiu.memory import MemorySystem
from myiu.app_context import AppContext

logger = logging.getLogger(__name__)


class ReflectionEngine(AsyncModule):
    """
    Module này cho phép MyIu thực hiện quá trình phản tư về các tương tác
    và trạng thái nội bộ của mình. Nó lắng nghe các sự kiện trên EventBus,
    phân tích chúng và tạo ra những suy ngẫm mới.
    """

    def __init__(self, event_bus: EventBus, memory_system: MemorySystem):
        super().__init__()
        self.event_bus = event_bus
        self.memory_system = memory_system
        self.reflection_queue = asyncio.Queue()
        self._is_running = False
        self._loop_task = None
        self.log.info("ReflectionEngine initialized.")

    async def _reflection_loop(self):
        self.log.info("Reflection loop started.")
        while self._is_running:
            try:
                event_data = await self.reflection_queue.get()
                self.log.info(f"Reflecting on event: {event_data}")
                self.reflection_queue.task_done()
            except asyncio.CancelledError:
                self.log.info("Reflection loop was cancelled.")
                break
            except Exception as e:
                self.log.error(f"Error during reflection process: {e}", exc_info=True)
        self.log.info("Reflection loop stopped.")

    async def on_new_thought(self, thought_data: Dict[str, Any]):
        await self.reflection_queue.put(thought_data)
        self.log.debug(f"Queued new thought for reflection: {thought_data.get('id')}")

    async def start(self):
        if self._is_running:
            return
        self._is_running = True
        await super().start()
        await self.event_bus.subscribe("new_thought", self.on_new_thought)
        self._loop_task = asyncio.create_task(self._reflection_loop())
        self.log.info("ReflectionEngine started and subscribed to events.")

    async def stop(self):
        if not self._is_running:
            return
        self._is_running = False
        await self.event_bus.unsubscribe("new_thought", self.on_new_thought)
        if self._loop_task:
            self._loop_task.cancel()
            await asyncio.sleep(0)
        await self.reflection_queue.join()
        await super().stop()
        self.log.info("ReflectionEngine unsubscribed and shutting down.")

async def main():
    """Hàm chính để thiết lập và chạy engine."""
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    app_context = AppContext()
    event_bus = EventBus()
    memory_system = MemorySystem(app_context=app_context)
    engine = ReflectionEngine(event_bus=event_bus, memory_system=memory_system)

    try:
        if isinstance(app_context, AsyncModule):
            await app_context.start()

        await event_bus.start()
        await memory_system.start()
        await engine.start()
        logger.info("Reflection service is now running. Press Ctrl+C to stop.")
        await stop_event.wait()
    except Exception as e:
        logger.error(f"An error occurred during startup or runtime: {e}", exc_info=True)
    finally:
        logger.info("Shutting down services...")
        await engine.stop()
        await memory_system.stop()
        await event_bus.stop()
        if isinstance(app_context, AsyncModule):
            await app_context.stop()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
