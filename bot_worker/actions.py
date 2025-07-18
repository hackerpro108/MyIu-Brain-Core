# bot_worker/actions.py
# PHIÊN BẢN HOÀN CHỈNH VÀ ĐẦY ĐỦ - 2025-07-15
import re
import subprocess
import os
from .config import PROJECT_ROOT
from .utils import log



class CodeActions:
    @staticmethod
    def get_action(action_type: str):
        action_map = {
            "replace_line": CodeActions.replace_line,
            "delete_line": CodeActions.delete_line,
            "insert_line": CodeActions.insert_line,
            "insert_blank_lines": CodeActions.insert_blank_lines,
            "trim_trailing_whitespace": CodeActions.trim_trailing_whitespace,
            "format_with_black": CodeActions.format_with_black,
            "replace_variable": CodeActions.replace_variable,
            "insert_function": CodeActions.insert_function,
            "replace_file_content": CodeActions.replace_file_content,
        }
        return action_map.get(action_type)

    @staticmethod
    def replace_file_content(content: str, **kwargs) -> tuple[bool, str]:
        source_file_path_relative = kwargs.get("source_file_path")
        if not source_file_path_relative:
            log.error("replace_file_content: Thiếu 'source_file_path'.")
            return False, content
source_file_absolute = os.path.join(PROJECT_ROOT, source_file_path_relative)  # TODO: Refactor long line
        try:
            with open(source_file_absolute, 'r', encoding='utf-8') as f_src:
                new_content = f_src.read()
            return True, new_content
        except Exception as e:
            log.error(f"Lỗi khi đọc file nguồn '{source_file_absolute}': {e}")
            return False, content

    @staticmethod
    def insert_line(content: str, **kwargs) -> tuple[bool, str]:
        line_number = kwargs.get("line_number")
        new_content = kwargs.get("new_content", "")
        if line_number is None:
            log.error("insert_line: Thiếu 'line_number'.")
            return False, content
        lines = content.split("\n")
        if 0 < line_number <= len(lines) + 1:
            lines.insert(line_number - 1, new_content)
            return True, "\n".join(lines)
        log.error(f"insert_line: Số dòng {line_number} không hợp lệ.")
        return False, content

    @staticmethod
    def replace_line(content: str, **kwargs) -> tuple[bool, str]:
        line_number = kwargs.get("line_number")
        new_content = kwargs.get("new_content")
        lines = content.split("\n")
        if 0 < line_number <= len(lines):
            lines[line_number - 1] = new_content
            return True, "\n".join(lines)
        return False, content

    @staticmethod
    def delete_line(content: str, **kwargs) -> tuple[bool, str]:
        line_number = kwargs.get("line_number")
        lines = content.split("\n")
        if 0 < line_number <= len(lines):
            del lines[line_number - 1]
            return True, "\n".join(lines)
        return False, content

    @staticmethod
    def insert_blank_lines(content: str, **kwargs) -> tuple[bool, str]:
        line_number = kwargs.get("line_number")
        num_lines = kwargs.get("num_lines", 1)
        lines = content.split("\n")
        if 0 < line_number <= len(lines):
            for _ in range(num_lines):
                lines.insert(line_number - 1, "")
            return True, "\n".join(lines)
        return False, content

    @staticmethod
    def trim_trailing_whitespace(content: str, **kwargs) -> tuple[bool, str]:
        lines = [line.rstrip() for line in content.split("\n")]
        return True, "\n".join(lines)

    @staticmethod
    def format_with_black(content: str, **kwargs) -> tuple[bool, str]:
        try:
            process = subprocess.run(
                ["black", "-"],
                input=content,
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            return True, process.stdout
        except FileNotFoundError:
            log.error("Lỗi: Lệnh 'black' không tìm thấy.")
            return False, content
        except subprocess.CalledProcessError as e:
            log.error(f"Lỗi khi chạy 'black': {e.stderr}")
            return False, content

    @staticmethod
    def replace_variable(content: str, **kwargs) -> tuple[bool, str]:
        name = kwargs.get("name")
        value = kwargs.get("value")
        if name is None or value is None:
            return False, content
        pattern = re.compile(rf"^{re.escape(name)}\s*=\s*.*$", re.MULTILINE)
        new_line = f"{name} = {value}"
        if pattern.search(content):
            return True, pattern.sub(new_line, content)
        return False, content

    @staticmethod
    def insert_function(content: str, **kwargs) -> tuple[bool, str]:
        func_content = kwargs.get("func_content")
        position = kwargs.get("position")
        if not func_content or not position:
            return False, content
        if position == "end":
            return True, content.rstrip() + f"\n\n\n{func_content.strip()}\n"
        return False, content
