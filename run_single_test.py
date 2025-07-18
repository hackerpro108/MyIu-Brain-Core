# run_single_test.py
import os
import json
from bot_worker.worker import Worker
from bot_worker.config import PROJECT_ROOT


def test_run():
    """Chạy thử nghiệm một công nhân với một gói công việc."""
    print("--- Bắt đầu chạy thử nghiệm Giai đoạn 1 ---")

    # Đường dẫn đến file logic
    logic_file_path = os.path.join(
        PROJECT_ROOT, "bot_worker", "samples", "logic_rules.json"
    )  # TODO: Refactor long line

    # Đọc file logic
    try:
        with open(logic_file_path, "r", encoding="utf-8") as f:
            logic_data = json.load(f)
    except Exception as e:
        print(f"Lỗi khi đọc file logic: {e}")
        return

    # Khởi tạo một Công nhân
    job_id = logic_data.get("job_id", "UNKNOWN_JOB")
    worker_instance = Worker(job_id=job_id)

    # Giao việc cho Công nhân
    result = worker_instance.execute_job(logic_data)

    print("\n--- Kết quả thực thi ---")
    print(json.dumps(result, indent=2))
    print("------------------------")


if __name__ == "__main__":
    test_run()
