# Tên file: soma.py
# Phiên bản: Kiến trúc Tinh gọn & An toàn khi Import

import asyncio
import json
from myiu.app_context import AppContext
from myiu.event_bus import EventBus
from myiu.logging_config import get_logger

class Soma:
    """
    Soma là trái tim của hệ thống MyIu, chịu trách nhiệm khởi tạo,
    quản lý vòng đời và điều phối các module cốt lõi.
    """
    def __init__(self, mode="full"):
        """
        Khởi tạo Soma với một chế độ hoạt động.
        'full': Tải tất cả module, dành cho Inference Worker.
        'api': Chỉ tải các module giao tiếp, không tải LLMCore, giúp API Server siêu nhẹ.
        """
        self.mode = mode
        self.app_context = AppContext()
        self.log = get_logger("Soma")
        self.internal_bus = EventBus()
        self.app_context.set_service("event_bus", self.internal_bus)
        self._load_config()

    def _load_config(self):
        """Tải cấu hình tĩnh từ genome."""
        try:
            with open("genome_static.json", "r", encoding="utf-8") as f:
                self.app_context.set_service("genome_static_config", json.load(f))
        except Exception as e:
            self.log.error(f"Không thể tải genome_static.json: {e}")

    async def start(self):
        """
        Khởi động Soma và các module con theo đúng chế độ hoạt động.
        Các module được import bên trong hàm này để tránh lỗi Circular Import.
        """
        # --- Giải pháp Kiến trúc: Import trễ các module nặng ---
        from myiu.llm_core import LLMCore
        from myiu.memory import Memory
        from myiu.affect import Affect
        from myiu.cortex import Cortex
        from myiu.emotional_cache import EmotionalCache
        from myiu.perception.thought_stream import ThoughtStream # Đường dẫn import đã sửa

        self.log.info(f"Soma: Bắt đầu khởi tạo các module ở chế độ '{self.mode}'...")

        all_module_definitions = [
            ("llm_core", LLMCore),
            ("memory", Memory),
            ("thought_stream", ThoughtStream),
            ("emotional_cache", EmotionalCache),
            ("affect", Affect),
            ("cortex", Cortex)
        ]

        # Lọc các module cần tải dựa trên chế độ
        if self.mode == "api":
            module_definitions = [m for m in all_module_definitions if m[0] != "llm_core"]
            self.log.warning("Soma (API Mode): Bỏ qua việc tải LLMCore để tiết kiệm RAM.")
        else: # Chế độ "full"
            module_definitions = all_module_definitions

        # Tạo instance cho các module
        for name, module_class in module_definitions:
            try:
                instance = module_class(self.app_context)
                self.app_context.set_service(name, instance)
            except Exception as e:
                self.log.error(f"Lỗi khi TẠO module {name}: {e}", exc_info=True)
                return

        self.log.info("Soma: Tất cả module đã được tạo. Bắt đầu KHỞI ĐỘNG...")

        # Khởi động các module đã tạo
        for name, _ in module_definitions:
            try:
                instance = self.app_context.get_service(name)
                if hasattr(instance, 'start') and asyncio.iscoroutinefunction(instance.start):
                    await instance.start()
                    self.log.info(f"Module '{name.capitalize()}' đã khởi động thành công.")
            except Exception as e:
                self.log.error(f"Lỗi khi KHỞI ĐỘNG module {name}: {e}", exc_info=True)

        self.log.info(f"Soma: Đã khởi động xong ở chế độ '{self.mode}'.")

    async def stop(self):
        """Dừng tất cả các module theo thứ tự ngược lại."""
        self.log.info("Soma: Đang dừng các module...")
        modules = self.app_context.get_all_services()
        stoppable_modules = [s for s in modules.values() if hasattr(s, 'stop') and asyncio.iscoroutinefunction(s.stop)]

        for module_instance in reversed(stoppable_modules):
            try:
                await module_instance.stop()
            except Exception as e:
                self.log.error(f"Lỗi khi dừng module {module_instance.__class__.__name__}: {e}")
        self.log.info("Soma: Đã dừng xong.")