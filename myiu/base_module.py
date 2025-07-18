import asyncio
from bot_worker.utils import log
class AsyncModule:
    def __init__(self):
        self._tasks = []
        self._is_running = False
        self.log = log
    def add_task(self, coro, name=None):
        task = asyncio.create_task(coro, name=name)
        self._tasks.append(task)
        return task
    async def start(self):
        self._is_running = True
        self.log.info(f"{self.__class__.__name__}: Started.")
        await self._setup_async_tasks()
    async def _setup_async_tasks(self):
        pass
    async def stop(self):
        self._is_running = False
        for task in self._tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self.log.info(f"{self.__class__.__name__}: Stopped.")