# brain_analyzer/scanner.py
import os
import re
import subprocess
from bot_worker.config import PROJECT_ROOT
from bot_worker.utils import log


class CodeScanner:
    """Quét mã nguồn bằng cách gọi flake8 như một tiến trình con độc lập."""

    def __init__(self):
        log.info("CodeScanner (Subprocess Mode) đã được khởi tạo.")

    def parse_error_string(self, error_str: str) -> dict | None:
        """Dùng regex để phân tích chuỗi lỗi một cách mạnh mẽ và chính xác."""
        # Regex pattern: (file):(line):(col): (code) (text)
        pattern = re.compile(r"^.+?:(\d+):\d+: (\w\d+ .*)")
        match = pattern.match(error_str)

        if not match:
            return None

        line_number, error_text_with_code = match.groups()
        error_code = error_text_with_code.split(" ", 1)[0]
        error_text = error_text_with_code.split(" ", 1)[1]

        return {
            "code": error_code,
            "line_number": int(line_number),
            "text": error_text,
            "physical_line": "",  # Sẽ được điền sau
        }

    def scan_file(self, file_path_relative: str) -> list:
        """
        Quét một file cụ thể bằng cách chạy `python3 -m flake8` và bắt output.
        """
        full_path = os.path.join(PROJECT_ROOT, file_path_relative)
        log.info(f"Scanner: Bắt đầu quét file bằng subprocess: {full_path}")

        if not os.path.exists(full_path):
            log.error(f"Scanner: File không tồn tại: {full_path}")
            return []

        # Thêm --isolated để flake8 báo cáo đầy đủ hơn
        command = ["python3", "-m", "flake8", "--isolated", full_path]
        result = subprocess.run(command, capture_output=True, text=True)

        output_text = result.stdout.strip()

        if not output_text:
            log.info(f"Scanner: Quét xong. Không tìm thấy vấn đề nào.")
            return []

        error_strings = output_text.split("\n")
        parsed_errors = []
        for err_str in error_strings:
            if not err_str or not err_str.strip():
                continue

            parsed_error = self.parse_error_string(err_str)
            if parsed_error:
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        if 0 < parsed_error["line_number"] <= len(lines):
                            parsed_error["physical_line"] = lines[
                                parsed_error["line_number"] - 1
                            ].strip()
                    parsed_errors.append(parsed_error)
                except Exception as e:
                    log.error(f"Lỗi khi đọc file để lấy nội dung dòng: {e}")

        log.info(f"Scanner: Quét xong. Tìm thấy {len(parsed_errors)} vấn đề.")
        return parsed_errors
