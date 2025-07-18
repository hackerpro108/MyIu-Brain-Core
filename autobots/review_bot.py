import os
import sys
from pathlib import Path
import json

# Đảm bảo project_root được xác định đúng
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from brain_analyzer.scanner import CodeScanner
from brain_analyzer.suggestion_engine import SuggestionEngine
from bot_worker.config import TASKS_PENDING_DIR
from bot_worker.utils import log
from myiu.app_context import AppContext

class ReviewBot:
    def __init__(self, app_context: AppContext):
        self.app_context = app_context
        self.scanner = CodeScanner()
        self.suggestion_engine = SuggestionEngine()
        self.log = log

    async def review_repository(self, repo_path: str):
        self.log.info(f"ReviewBot: Bắt đầu quét kho lưu trữ tại: {repo_path}")
        python_files = []
        # --- TỐI ƯU HÓA: Thêm danh sách loại trừ ---
        exclude_dirs = {"node_modules", "myiu_env", ".git", "tasks", "nano_extracted", "frontend", "__pycache__"}

        for root, dirs, files in os.walk(repo_path):
            # --- TỐI ƯU HÓA: Bỏ qua các thư mục không cần thiết ngay từ đầu ---
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith(".py"):
                    try:
                        abs_file_path = Path(root) / file
                        relative_path = abs_file_path.relative_to(project_root)
                        python_files.append(str(relative_path))
                    except ValueError:
                        continue

        if not python_files:
            self.log.info("ReviewBot: Không tìm thấy file Python nào để quét.")
            return

        for file_relative_path in python_files:
            self.log.info(f"ReviewBot: Đang quét file: {file_relative_path}")
            scan_results = self.scanner.scan_file(file_relative_path)
            
            lint_job = self.suggestion_engine.create_lint_suggestion_job(file_relative_path, scan_results)
            if lint_job:
                self.save_job_to_pending(lint_job)
            
            formatting_job = self.suggestion_engine.create_formatting_job(file_relative_path)
            if formatting_job:
                self.save_job_to_pending(formatting_job)

        self.log.info("ReviewBot: Hoàn thành quét kho lưu trữ.")

    def save_job_to_pending(self, job_data: dict):
        os.makedirs(TASKS_PENDING_DIR, exist_ok=True)
        job_id = job_data.get("job_id", f"job_{len(os.listdir(TASKS_PENDING_DIR)) + 1}")
        file_path = os.path.join(TASKS_PENDING_DIR, f"{job_id}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(job_data, f, indent=2)
            self.log.info(f"ReviewBot: Đã lưu gói công việc '{job_id}' vào: {file_path}")
        except Exception as e:
            self.log.error(f"ReviewBot: Lỗi khi lưu gói công việc '{job_id}': {e}")
