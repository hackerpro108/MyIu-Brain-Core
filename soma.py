import asyncio
import json
from myiu.app_context import AppContext
from myiu.event_bus import EventBus
from myiu.logging_config import get_logger
from myiu.llm_core import LLMCore
from myiu.memory import Memory
from myiu.affect import Affect
from myiu.cortex import Cortex
from myiu.emotional_cache import EmotionalCache
# --- SỬA LỖI: Đường dẫn import đúng ---
from myiu.perception.thought_stream import ThoughtStream

class Soma:
    def __init__(self):
        self.app_context = AppContext()
        self.log = get_logger("Soma")
        self.internal_bus = EventBus()
        self.app_context.set_service("event_bus", self.internal_bus)
        self._load_config()

    def _load_config(self):
        try:
            with open("genome_static.json", "r", encoding="utf-8") as f:
                self.app_context.set_service("genome_static_config", json.load(f))
        except Exception as e:
            self.log.error(f"Không thể tải genome_static.json: {e}")

    async def start(self):
        self.log.info("Soma: Bắt đầu khởi tạo các module theo thứ tự an toàn...")
        
        module_definitions = [
            ("llm_core", LLMCore),
            ("memory", Memory),
            ("thought_stream", ThoughtStream),
            ("emotional_cache", EmotionalCache),
            ("affect", Affect),
            ("cortex", Cortex)
        ]
        
        for name, module_class in module_definitions:
            try:
                instance = module_class(self.app_context)
                self.app_context.set_service(name, instance)
            except Exception as e:
                self.log.error(f"Lỗi khi TẠO module {name}: {e}", exc_info=True)
                return

        self.log.info("Soma: Tất cả module đã được tạo. Bắt đầu KHỞI ĐỘNG...")

        for name, _ in module_definitions:
            try:
                instance = self.app_context.get_service(name)
                await instance.start()
                self.log.info(f"Module '{name.capitalize()}' đã khởi động thành công.")
            except Exception as e:
                 self.log.error(f"Lỗi khi KHỞI ĐỘNG module {name}: {e}", exc_info=True)

        self.log.info("Soma: Tất cả các module cốt lõi đã khởi động xong.")

    async def stop(self):
        self.log.info("Soma: Đang dừng các module...")
        modules = self.app_context.get_all_services()
        stoppable_modules = [s for s in modules.values() if hasattr(s, 'stop') and asyncio.iscoroutinefunction(s.stop)]
        
        for module_instance in reversed(stoppable_modules):
            try:
                await module_instance.stop()
            except Exception as e:
                self.log.error(f"Lỗi khi dừng module {module_instance.__class__.__name__}: {e}")
        self.log.info("Soma: Đã dừng xong.")
