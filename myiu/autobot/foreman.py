import asyncio
import os
from glob import glob
from multiprocessing import Pool
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.autobot.worker import worker_process
from myiu.autobot import actions
# --- SỬA LỖI: Import ThoughtChunk để đóng gói suy nghĩ ---
from myiu.perception.thought_chunk import ThoughtChunk

class Foreman(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.event_bus = self.app_context.get_service("event_bus")
        self.thought_stream = None # Sẽ lấy trong hàm start
        self.task_dir = "tasks/pending"

    async def start(self):
        await super().start()
        self.thought_stream = self.app_context.get_service("thought_stream")
        self.add_task(self._dispatch_tasks_loop(), "foreman_dispatch_loop")

    async def _dispatch_tasks_loop(self):
        while self.is_running:
            task_files = glob(f"{self.task_dir}/*.json")
            if task_files:
                # --- SỬA LỖI: Đóng gói suy nghĩ vào ThoughtChunk ---
                chunk = ThoughtChunk(origin="Foreman", content=f"Phát hiện {len(task_files)} tác vụ mới.")
                if self.thought_stream: self.thought_stream.record(chunk)
                
                with Pool(processes=os.cpu_count()) as pool:
                    results = pool.map(worker_process, task_files)
                
                for report in results:
                    # ... (logic xử lý báo cáo)
                    os.remove(report['task_path'])
            await asyncio.sleep(10)
