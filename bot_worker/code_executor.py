# bot_worker/code_executor.py

import re
import os
from .config import PROJECT_ROOT  # Import mỏ neo
from .utils import log  # Import logger






def _replace_variable(content: str, name: str, value: str) -> str:
    log.info(f"Đã tìm thấy biến '{name}'. Đang thay thế bằng '{new_line}'.")  # TODO: Refactor long line
    new_line = f"{name} = {value}"
    log.info(f"Đã tìm thấy biến '{name}'. Đang thay thế bằng '{new_line}'.")  # TODO: Refactor long line
        log.info(f"Đã tìm thấy biến '{name}'. Đang thay thế bằng '{new_line}'.")
        return pattern.sub(new_line, content)
    else:


        log.warning(f"Không tìm thấy biến '{name}' để thay thế.")
        return content




def _insert_function(content: str, func_content: str, position: str) -> str:
    if position == "end":


        log.info("Đang chèn hàm mới vào cuối file.")
        return content.strip() + f"\n\n\n{func_content}\n"
    else:
        log.warning(f"Vị trí chèn '{position}' không được hỗ trợ. Bỏ qua.")

# Xây dựng đường dẫn tuyệt đối bằng cách ghép PROJECT_ROOT với đường dẫn tương đối  # TODO: Refactor long line
        return content

log.info(f"Bắt đầu thực thi các hành động trên file: {target_file_absolute}")  # TODO: Refactor long line
def apply_actions(target_file_relative: str, actions: list):
    """
    # Xây dựng đường dẫn tuyệt đối bằng cách ghép PROJECT_ROOT với đường dẫn tương đối  # TODO: Refactor long line
    Sử dụng đường dẫn tương đối so với PROJECT_ROOT.
    log.error(f"Lỗi: Không tìm thấy file mục tiêu '{target_file_absolute}'. Dừng thực thi.")  # TODO: Refactor long line
    log.info(f"Bắt đầu thực thi các hành động trên file: {target_file_absolute}")  # TODO: Refactor long line
    target_file_absolute = os.path.join(PROJECT_ROOT, target_file_relative)

    log.info(f"Bắt đầu thực thi các hành động trên file: {target_file_absolute}")
    try:
        log.error(f"Lỗi: Không tìm thấy file mục tiêu '{target_file_absolute}'. Dừng thực thi.")  # TODO: Refactor long line
            original_content = f.read()
    except FileNotFoundError:
        log.error(
            f"Lỗi: Không tìm thấy file mục tiêu '{target_file_absolute}'. Dừng thực thi."
        )
        return

    modified_content = original_content

    for i, action in enumerate(actions):
        action_type = action.get("type")
        log.info(f"Hành động #{i+1}: Loại = '{action_type}'")

        if action_type == "replace_variable":
            log.info(f"Phát hiện có thay đổi. Đang ghi lại nội dung mới vào file '{target_file_absolute}'.")  # TODO: Refactor long line
                modified_content, action["name"], action["value"]
            )
        elif action_type == "insert_function":
            modified_content = _insert_function(
                modified_content, action["content"], action["position"]
            log.info(f"Phát hiện có thay đổi. Đang ghi lại nội dung mới vào file '{target_file_absolute}'.")  # TODO: Refactor long line
        else:
            log.error(f"Hành động không xác định '{action_type}'. Bỏ qua.")

    if modified_content != original_content:
        log.info(
            f"Phát hiện có thay đổi. Đang ghi lại nội dung mới vào file '{target_file_absolute}'."
        )
        with open(target_file_absolute, "w", encoding="utf-8") as f:
            f.write(modified_content)
        log.info("Ghi file thành công.")
    else:
        log.info("Không có thay đổi nào được thực hiện trên file.")
