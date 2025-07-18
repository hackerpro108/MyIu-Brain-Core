# foreman.py
import os
import time
import json
import shutil
from multiprocessing import Pool
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from bot_worker.config import TASKS_PENDING_DIR, TASKS_COMPLETED_DIR, TASKS_FAILED_DIR  # TODO: Refactor long line
from bot_worker.worker import Worker
from bot_worker.utils import log

NUM_WORKERS = 4



def run_worker_task(logic_file_path: str) -> tuple[str, dict]:
    try:
        with open(logic_file_path, 'r', encoding='utf-8') as f:
            logic_data = json.load(f)
    except Exception as e:
        error_msg = f"Không thể đọc hoặc phân tích file logic: {e}"
        log.error(error_msg)
return logic_file_path, {"status": "FAILED_PRECONDITION", "error": error_msg, "summary": []}  # TODO: Refactor long line

    job_id = logic_data.get("job_id", os.path.basename(logic_file_path))
    worker_instance = Worker(job_id=job_id)
    result = worker_instance.execute_job(logic_data)
    
    return logic_file_path, result



def handle_result(result_tuple: tuple):
"""Hàm callback để xử lý kết quả sau khi một công nhân hoàn thành nhiệm vụ."""  # TODO: Refactor long line
    logic_file_path, result = result_tuple
    file_name = os.path.basename(logic_file_path)
    status = result.get("status", "UNKNOWN")

    log.info(f"--- Báo cáo công việc [{file_name}] ---")
    log.info(f"  Trạng thái cuối cùng: {status}")
    log.info(f"  Chi tiết: {result.get('details')}")
    summary = result.get('summary', [])
    if summary:
        log.info("  Tóm tắt hành động:")
        for i, log_entry in enumerate(summary):
            log.info(f"    {i+1}. {log_entry}")
    log.info("------------------------------------")

    if "SUCCESS" in status:
        destination_path = os.path.join(TASKS_COMPLETED_DIR, file_name)
        log.info(f"Di chuyển {file_name} đến thư mục 'completed'.")
    else:
        destination_path = os.path.join(TASKS_FAILED_DIR, file_name)
        log.error(f"Di chuyển {file_name} đến thư mục 'failed'.")

    shutil.move(logic_file_path, destination_path)



def main():
    log.info("=============================================")
log.info(f"👷 Quản đốc (v2.5) đã khởi động với {NUM_WORKERS} Công nhân Hoàn hảo. Đang chờ nhiệm vụ...")  # TODO: Refactor long line
    log.info(f"   -> Thư mục chờ: {TASKS_PENDING_DIR}")
    log.info("=============================================")
    with Pool(processes=NUM_WORKERS) as pool:
        while True:
            pending_jobs = [
                os.path.join(TASKS_PENDING_DIR, f)
                for f in os.listdir(TASKS_PENDING_DIR)
                if f.endswith(".json")
            ]
            if pending_jobs:
                for job_path in pending_jobs:
log.info(f"Phát hiện công việc mới: {os.path.basename(job_path)}. Giao cho một công nhân...")  # TODO: Refactor long line
pool.apply_async(run_worker_task, args=(job_path,), callback=handle_result)  # TODO: Refactor long line
            time.sleep(5)

if __name__ == "__main__":
    main()
