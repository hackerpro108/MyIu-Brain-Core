import asyncio
from myiu.app_context import AppContext
from myiu.logging_config import get_logger

class AsyncModule:
    def __init__(self, app_context: AppContext):
        self.app_context = app_context
        self.log = get_logger(self.__class__.__name__)
        self._is_running = False
        self._background_tasks = []

    @property
    def is_running(self):
        return self._is_running

    def add_task(self, coro, name: str = None):
        task = asyncio.create_task(coro, name=name)
        self._background_tasks.append(task)
        return task

    async def start(self):
        self.log.info(f"Module '{self.__class__.__name__}' đang bắt đầu.")
        self._is_running = True

    async def stop(self):
        self.log.info(f"Module '{self.__class__.__name__}' đang dừng.")
        self._is_running = False
        if not self._background_tasks:
            return
        for task in self._background_tasks:
            task.cancel()
        await asyncio.gather(*self._background_tasks, return_exceptions=True)
        self._background_tasks.clear()
