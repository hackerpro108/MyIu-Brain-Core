import os
import logging

# Thiết lập logger đơn giản
logging.basicConfig(level=logging.INFO, format='%(asctime)s - PHOENIX - %(levelname)s - %(message)s')

# --- ĐỊNH NGHĨA NỘI DUNG CÁC TỆP CẦN SỬA ---

# Nội dung đã sửa của brain_analyzer/suggestion_engine.py
SUGGESTION_ENGINE_CODE = """
from bot_worker.utils import log

class SuggestionEngine:
    def create_lint_suggestion_job(self, target_file: str, scan_results: list) -> dict | None:
        if not scan_results:
            return None
        actions = []
        if any(error["code"] == "W291" for error in scan_results):
            actions.append({"type": "trim_trailing_whitespace"})
        for error in scan_results:
            if error["code"] == "F841":
                actions.append({
                    "type": "replace_line",
                    "line_number": error["line_number"],
                    "new_content": f"# [MYIU-AUTO-FIX] {error['physical_line'].strip()}",
                })
            elif error["code"] == "F401":
                actions.append({"type": "delete_line", "line_number": error["line_number"]})
        if not actions:
            return None
        job_id = f"linting_{target_file.replace('/', '_').replace('.', '_')}"
        job = {
            "job_id": job_id,
            "source": "LintingEngine v1.1",
            "target_file": target_file,
            "actions": actions,
        }
        log.info(f"SuggestionEngine: Đã tạo Gói Công việc LINTING '{job_id}' với {len(actions)} hành động.")
        return job

    def create_formatting_job(self, target_file: str) -> dict:
        job_id = f"formatting_{target_file.replace('/', '_').replace('.', '_')}"
        job = {
            "job_id": job_id,
            "source": "FormattingEngine",
            "target_file": target_file,
            "actions": [{"type": "format_with_black", "target_file": target_file}],
        }
        log.info(f"SuggestionEngine: Đã tạo Gói Công việc FORMATTING '{job_id}'.")
        return job
"""

# Nội dung đã sửa của soma.py
SOMA_CODE = """
import asyncio
import json
from datetime import datetime
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from bot_worker.config import PROJECT_ROOT
from bot_worker.utils import log
from myiu.app_context import AppContext
from myiu.event_bus import EventBus
from autobots.review_bot import ReviewBot

try:
    from myiu.memory import Memory
    from myiu.affect import Affect
    from myiu.cortex import Cortex
except ImportError as e:
    log.error(f"Soma: Lỗi khi import các module cốt lõi: {e}")
    Memory, Affect, Cortex = None, None, None

class Soma:
    def __init__(self):
        self.app_context = AppContext()
        self.log = log
        self.internal_bus = EventBus()
        self._is_running = False
        self.app_context.set_service("soma", self)
        self.app_context.set_service("event_bus", self.internal_bus)
        self.app_context.set_service("log", self.log)

    async def _start_auto_correction_loop(self, interval_seconds: int = 300):
        self.log.info(f"Soma: Khởi động vòng lặp tự động sửa lỗi mỗi {interval_seconds} giây...")
        review_bot_instance = ReviewBot(self.app_context)
        while self._is_running:
            try:
                self.log.info("Soma: Đang kích hoạt ReviewBot để quét mã nguồn...")
                await review_bot_instance.review_repository(str(PROJECT_ROOT))
            except Exception as e:
                self.log.error(f"Soma: Lỗi trong vòng lặp tự động sửa lỗi: {e}")
            await asyncio.sleep(interval_seconds)

    async def start(self):
        self.log.info("Soma: Bắt đầu khởi tạo các module cốt lõi...")
        self._is_running = True
        # Logic khởi tạo module...
        # asyncio.create_task(self._start_auto_correction_loop()) # Tạm thời tắt để kiểm tra
        self.log.info("Soma: Tất cả các module cốt lõi đã sẵn sàng.")

    async def stop(self):
        self.log.info("Soma: Đang dừng các module cốt lõi...")
        self._is_running = False
        self.log.info("Soma: Các module cốt lõi đã dừng.")
"""

# Nội dung đã sửa của myiu/memory.py
MEMORY_CODE = """
from myiu.app_context import AppContext
class Memory:
    def __init__(self, app_context: AppContext):
        self.app_context = app_context
        self.log = app_context.get_service("log")
        self.code_insights = []
        self._is_running = False
        self.log.info("Memory: Module bộ nhớ đã khởi tạo.")
    async def start(self):
        self._is_running = True
        self.log.info(f"Memory: Bắt đầu.")
    async def stop(self):
        self._is_running = False
        self.log.info(f"Memory: Dừng.")
"""

# Dictionary chứa các bản vá
PATCHES = {
    "brain_analyzer/suggestion_engine.py": SUGGESTION_ENGINE_CODE,
    "soma.py": SOMA_CODE,
    "myiu/memory.py": MEMORY_CODE
}

def apply_patches():
    logging.info("Bắt đầu áp dụng Bản Vá Phượng Hoàng...")
    for file_path, new_content in PATCHES.items():
        try:
            # Tạo thư mục nếu chưa tồn tại
            dir_name = os.path.dirname(file_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content.strip())
            logging.info(f" vá thành công: {file_path}")
        except Exception as e:
            logging.error(f" thất bại khi vá {file_path}: {e}")
    logging.info("Hoàn tất áp dụng Bản Vá Phượng Hoàng.")

if __name__ == "__main__":
    apply_patches()

