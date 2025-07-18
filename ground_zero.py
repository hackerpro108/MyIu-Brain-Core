import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - GROUND ZERO - %(levelname)s - %(message)s')

# Định nghĩa nội dung chuẩn cho TẤT CẢ các tệp cốt lõi
CORE_FILES = {
    "bot_worker/utils.py": """
import logging
import sys
def setup_logger():
    logger = logging.getLogger("MyIu")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Use a consistent log file name
        file_handler = logging.FileHandler("myiu_system.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger
log = setup_logger()
""",
    "myiu/app_context.py": """
class AppContext:
    def __init__(self):
        self.services = {}
    def set_service(self, name, service):
        self.services[name] = service
    def get_service(self, name):
        return self.services.get(name)
""",
    "myiu/base_module.py": """
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
""",
    "myiu/affect.py": """
from myiu.base_module import AsyncModule
from myiu.app_context import AppContext
class Affect(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__()
        self.log.info("Affect module initialized.")
    async def start(self):
        await super().start()
    async def stop(self):
        await super().stop()
""",
    "myiu/memory.py": """
from myiu.base_module import AsyncModule
from myiu.app_context import AppContext
class Memory(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__()
        self.log.info("Memory module initialized.")
    async def start(self):
        await super().start()
    async def stop(self):
        await super().stop()
""",
    "myiu/cortex.py": """
from myiu.base_module import AsyncModule
from myiu.app_context import AppContext
class Cortex(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__()
        self.log.info("Cortex module initialized.")
    async def start(self):
        await super().start()
    async def stop(self):
        await super().stop()
""",
    "soma.py": """
import asyncio
from bot_worker.utils import log
from myiu.app_context import AppContext
from myiu.event_bus import EventBus
from myiu.memory import Memory
from myiu.affect import Affect
from myiu.cortex import Cortex

class Soma:
    def __init__(self):
        self.app_context = AppContext()
        self.log = log
        self.internal_bus = EventBus()
        self._is_running = False
        self.app_context.set_service("soma", self)
        self.app_context.set_service("event_bus", self.internal_bus)
        self.app_context.set_service("log", self.log)
        self.modules = {}

    async def start(self):
        self.log.info("Soma: Bắt đầu khởi tạo các module cốt lõi...")
        self._is_running = True
        core_modules = {"memory": Memory, "affect": Affect, "cortex": Cortex}
        for name, module_class in core_modules.items():
            try:
                instance = module_class(self.app_context)
                self.app_context.set_service(name, instance)
                self.modules[name] = instance
                await instance.start()
                self.log.info(f"Soma: Module {name.capitalize()} đã khởi tạo.")
            except Exception as e:
                self.log.error(f"Soma: Lỗi khi khởi tạo module {name}: {e}", exc_info=True)
        self.log.info("Soma: Tất cả các module cốt lõi đã sẵn sàng.")

    async def stop(self):
        self.log.info("Soma: Đang dừng các module cốt lõi...")
        self._is_running = False
        for instance in self.modules.values():
            await instance.stop()
        self.log.info("Soma: Các module cốt lõi đã dừng.")
""",
    "main.py": """
import uvicorn
import asyncio
from fastapi import FastAPI
from bot_worker.utils import log
from soma import Soma

app = FastAPI()
soma_instance = None

@app.on_event("startup")
async def startup_event():
    global soma_instance
    log.info("Ứng dụng FastAPI khởi động. Bắt đầu khởi tạo MyIu Soma...")
    soma_instance = Soma()
    asyncio.create_task(soma_instance.start())
    log.info("MyIu Soma đã được yêu cầu khởi động.")

@app.on_event("shutdown")
async def shutdown_event():
    global soma_instance
    if soma_instance:
        await soma_instance.stop()
    log.info("MyIu Soma đã dừng.")

if __name__ == "__main__":
    log.info("Đang khởi động Uvicorn cho main application...")
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=False, workers=1)
"""
}

def regenerate_core():
    logging.info("Tái tạo toàn bộ lõi hệ thống...")
    for file_path, new_content in CORE_FILES.items():
        try:
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content.strip())
            logging.info(f"TÁI TẠO THÀNH CÔNG: {file_path}")
        except Exception as e:
            logging.error(f"TÁI TẠO THẤT BẠI cho {file_path}: {e}")
    logging.info("Hoàn tất Kế Hoạch Tái Tạo.")

if __name__ == "__main__":
    regenerate_core()

