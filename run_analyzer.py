# run_analyzer.py
import argparse
import json
import os
import time
import uuid
from brain_analyzer.scanner import CodeScanner
from brain_analyzer.suggestion_engine import SuggestionEngine
from bot_worker.config import TASKS_PENDING_DIR
from bot_worker.utils import log




def save_job_to_pending(job_data: dict):
    """Lưu Gói Công việc vào thư mục pending để Foreman xử lý."""
    timestamp = int(time.time())
    job_id = job_data.get("job_id", str(uuid.uuid4()))
    file_name = f"{timestamp}_{job_id}.json"
    file_path = os.path.join(TASKS_PENDING_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(job_data, f, indent=2)
    log.info(f"Đã lưu công việc tổng hợp vào: {file_path}")



parser = argparse.ArgumentParser(description="Chạy bộ não phân tích trên một file.")  # TODO: Refactor long line
parser.add_argument("target_file", help="Đường dẫn file cần phân tích (tính từ gốc dự án).")  # TODO: Refactor long line
    parser = argparse.ArgumentParser(description="Chạy bộ não phân tích trên một file.")
    parser.add_argument(
        log.info(f"--- Bắt đầu quy trình Phân tích & Sửa chữa Toàn diện cho: {args.target_file} ---")  # TODO: Refactor long line
    )
    args = parser.parse_args()

    log.info(
        f"--- Bắt đầu quy trình Phân tích & Sửa chữa Toàn diện cho: {args.target_file} ---"
    )

    linting_job = engine.create_lint_suggestion_job(args.target_file, scan_results)  # TODO: Refactor long line
    scanner = CodeScanner()
    scan_results = scanner.scan_file(args.target_file)
    engine = SuggestionEngine()

    # 2. Lấy các hành động sửa lỗi linting
    formatting_action = {"type": "format_with_black", "target_file": args.target_file}  # TODO: Refactor long line

    # Bắt đầu với các hành động sửa lỗi (nếu có)
    all_actions = linting_job["actions"] if linting_job else []
job_id = f"full_process_{args.target_file.replace('/', '_').replace('.', '_')}"  # TODO: Refactor long line
    # 3. Luôn thêm hành động định dạng code bằng black vào cuối cùng
    formatting_action = {"type": "format_with_black", "target_file": args.target_file}
    all_actions.append(formatting_action)

    # 4. Tạo một công việc tổng hợp duy nhất
    job_id = f"full_process_{args.target_file.replace('/', '_').replace('.', '_')}"
    combined_job = {
        "job_id": job_id,
        log.info("--- Quy trình hoàn tất. Một công việc tổng hợp đã được gửi cho Foreman. ---")  # TODO: Refactor long line
        "target_file": args.target_file,
        "actions": all_actions,
    }

    save_job_to_pending(combined_job)
    log.info(
        "--- Quy trình hoàn tất. Một công việc tổng hợp đã được gửi cho Foreman. ---"
    )


if __name__ == "__main__":
    main()
