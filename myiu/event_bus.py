import asyncio
from collections import defaultdict
from typing import Callable, Dict, List, Any
from myiu.logging_config import get_logger

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        self.log = get_logger(self.__class__.__name__)
    async def subscribe(self, topic: str, handler: Callable):
        self._subscribers[topic].append(handler)
        self.log.info(f"Handler '{handler.__name__}' đã đăng ký vào chủ đề '{topic}'.")
    async def publish(self, topic: str, message: Any):
        if topic in self._subscribers:
            self.log.debug(f"Phát sự kiện trên '{topic}': {message}")
            tasks = [asyncio.create_task(handler(message)) for handler in self._subscribers[topic]]
            await asyncio.gather(*tasks)
