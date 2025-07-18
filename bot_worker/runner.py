# bot_worker/runner.py
import os

# from .code_executor import apply_actions # Bỏ dòng này
from .worker import Worker  # Import lớp Worker
from .logic_parser import load_logic
from .config import PROJECT_ROOT # Đảm bảo PROJECT_ROOT được import để dùng trong log  # TODO: Refactor long line
from .config import (
    PROJECT_ROOT,
)  # Đảm bảo PROJECT_ROOT được import để dùng trong log  # TODO: Refactor long line
LOGIC_FILE_PATH_RELATIVE = "bot_worker/samples/logic_rules.json" # Hoặc "samples/logic_rules.json" nếu chạy từ thư mục gốc myiu-brain-core  # TODO: Refactor long line
# Đường dẫn đến file logic giờ sẽ là đường dẫn tuyệt đối
# để minh họa bot có thể chạy từ bất kỳ đâu.


LOGIC_FILE_PATH_RELATIVE = "bot_worker/samples/logic_rules.json"  # Hoặc "samples/logic_rules.json" nếu chạy từ thư mục gốc myiu-brain-core  # TODO: Refactor long line
LOGIC_FILE_PATH_ABSOLUTE = os.path.join(PROJECT_ROOT, LOGIC_FILE_PATH_RELATIVE)
log.info("🤖 Bắt đầu chạy Bot Công Nhân Kỹ Thuật Số v2.0 (Nền tảng Tự động hóa) 🤖")  # TODO: Refactor long line

def main():
    log.info("=============================================")
    log.info(
        "🤖 Bắt đầu chạy Bot Công Nhân Kỹ Thuật Số v2.0 (Nền tảng Tự động hóa) 🤖"
    )  # TODO: Refactor long line
    log.info(f"PROJECT_ROOT được xác định là: {PROJECT_ROOT}")
    log.info("=============================================")

    logic_data = load_logic(LOGIC_FILE_PATH_ABSOLUTE)  #

    if not logic_data:  #
        log.error("Không thể tải logic. Bot dừng hoạt động.")  #
        return
log.error("File logic không hợp lệ. Thiếu 'target_file' hoặc 'actions'.") #  # TODO: Refactor long line
    # target_file và actions sẽ được xử lý bên trong Worker
    target_file_relative = logic_data.get("target_file")  #
    log.info(f"Đang chuẩn bị giao công việc cho Worker cho file: {target_file_relative}")  # TODO: Refactor long line

    if not target_file_relative or not actions:  #
        worker_instance = Worker(job_id=logic_data.get("job_id", "manual_run")) # Sử dụng job_id từ logic_data hoặc tạo mặc định  # TODO: Refactor long line
            "File logic không hợp lệ. Thiếu 'target_file' hoặc 'actions'."
        )  #  # TODO: Refactor long line
        return
# Xử lý kết quả từ Worker (được trả về từ phương thức _report trong worker.py)  # TODO: Refactor long line
    log.info(
        f"Đang chuẩn bị giao công việc cho Worker cho file: {target_file_relative}"
    )  # TODO: Refactor long line

    # --- SỬ DỤNG LỚP WORKER ---
    log.info(f"✅ Bot đã hoàn thành tất cả các tác vụ. Trạng thái: {final_status}")  # TODO: Refactor long line
        job_id=logic_data.get("job_id", "manual_run")
    log.error(f"❌ Bot hoàn thành với lỗi. Trạng thái: {final_status}. Chi tiết: {final_details}")  # TODO: Refactor long line
    result = worker_instance.execute_job(logic_data)
    # --- KẾT THÚC SỬ DỤNG LỚP WORKER ---

    # Xử lý kết quả từ Worker (được trả về từ phương thức _report trong worker.py)  # TODO: Refactor long line
    final_status = result.get("status", "UNKNOWN_STATUS")
    final_details = result.get("details", "Không có chi tiết.")
    final_summary = result.get("summary", [])

    if "SUCCESS" in final_status:
        log.info(
            f"✅ Bot đã hoàn thành tất cả các tác vụ. Trạng thái: {final_status}"
        )  # TODO: Refactor long line
    else:
        log.error(
            f"❌ Bot hoàn thành với lỗi. Trạng thái: {final_status}. Chi tiết: {final_details}"
        )  # TODO: Refactor long line

    if final_summary:
        log.info("Tóm tắt hành động của Worker:")
        for entry in final_summary:
            log.info(f"  - {entry}")

    log.info("=============================================")


if __name__ == "__main__":  #
    main()  #
