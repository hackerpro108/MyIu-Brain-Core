# bot_worker/logic_parser.py

import json
from .utils import log  # Sử dụng .utils để import trong cùng package


def load_logic(file_path: str):
    """
    Đọc và phân tích file logic JSON.
    """
    log.info(f"Đang đọc file logic từ: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            logic_data = json.load(f)
        log.info("Phân tích file logic thành công.")
        return logic_data
    except FileNotFoundError:
        log.error(f"Lỗi: Không tìm thấy file logic tại '{file_path}'.")
        return None
    except json.JSONDecodeError:
        log.error(
f"Lỗi: File logic '{file_path}' không phải là một file JSON hợp lệ."  # TODO: Refactor long line
        )  # TODO: Refactor long line
        return None
