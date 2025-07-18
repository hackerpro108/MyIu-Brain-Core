import asyncio
import os
import re
from glob import glob
from pathlib import Path
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.models import MemoryNode
from myiu.perception.thought_chunk import ThoughtChunk
from myiu.autobot.scanner import CodeScanner
from myiu.autobot.suggestion_engine import SuggestionEngine
from myiu.websocket_manager import manager as websocket_manager

class Cortex(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.event_bus = None
        self.memory = None
        self.thought_stream = None
        self.llm_core = None
        self.exclude_dirs = []

    async def start(self):
        await super().start()
        self.event_bus = self.app_context.get_service("event_bus")
        self.memory = self.app_context.get_service("memory")
        self.thought_stream = self.app_context.get_service("thought_stream")
        self.llm_core = self.app_context.get_service("llm_core")
        
        genome = self.app_context.get_service("genome_static_config")
        self.exclude_dirs = genome.get("self_reflection_config", {}).get("exclude_dirs", [])
        
        await self.event_bus.subscribe("user_message", self._handle_user_message)
        self.log.info("Cortex đã sẵn sàng nhận lệnh.")

    # --- HÀM MỚI ĐỂ NHẬN LỆNH TỪ WEBSOCKET ---
    async def handle_command_from_websocket(self, command_text: str):
        """
        Cổng vào mới cho lệnh từ UI.
        Hàm này nhận lệnh và đưa nó vào EventBus để tái sử dụng luồng xử lý cũ.
        """
        await self._log_thought(f"Lệnh '{command_text}' nhận qua WebSocket.")
        # Đưa lệnh vào EventBus, giống hệt như API /ipc/message đang làm
        await self.event_bus.publish("user_message", {"text": command_text})


    # --- CÁC HÀM CŨ GIỮ NGUYÊN ---
    async def _log_thought(self, content: str, origin: str = "Cortex"):
        chunk = ThoughtChunk(origin=origin, content=content)
        if self.thought_stream:
            self.thought_stream.record(chunk)
        await websocket_manager.broadcast(content)

    async def _handle_user_message(self, event_data: dict):
        message = event_data.get("text", "").strip()
        await self._log_thought(f"Nhận được lệnh: '{message}'")
        
        if "phân tích" in message.lower() and "sửa lỗi" in message.lower() and "file" in message.lower():
            match = re.search(r'file\s+([\w\./\\]+)', message)
            if match:
                target_file = match.group(1).strip()
                if not os.path.exists(target_file):
                    await self._log_thought(f"Lỗi: File '{target_file}' không tồn tại. Vui lòng tạo file trước.")
                    return
                
                await self._log_thought(f"Đã hiểu lệnh tự vá lỗi cho file: {target_file}")
                asyncio.create_task(self.run_targeted_reflection(target_file))
            else:
                await self._log_thought("Lệnh không hợp lệ. Không thể xác định tên file.")
        else:
            await self._log_thought("Đang xử lý như một câu hội thoại thông thường...")
            response = self.llm_core.generate_response(f"Người dùng nói: '{message}'. Hãy trả lời như một AI.")
            await self._log_thought(f"MyIu: {response}")

    async def run_targeted_reflection(self, file_path: str):
        await self._log_thought(f"Bắt đầu quét {file_path}...")
        issues = CodeScanner.scan_with_flake8(file_path)
        if not issues:
            await self._log_thought(f"Quét xong, không tìm thấy vấn đề có thể sửa tự động.")
            return
        
        await self._log_thought(f"Tìm thấy {len(issues)} vấn đề. Đang tạo tác vụ cho Autobot...")
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        task_path = SuggestionEngine.create_autofix_task(file_path, issues, source_code)
        if task_path:
            await self._log_thought(f"Đã tạo tác vụ {os.path.basename(task_path)} và gửi cho Foreman.")

    async def stop(self):
        await super().stop()
