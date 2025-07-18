import json
import os
import difflib
import tempfile
from myiu.autobot import actions
from myiu.logging_config import get_logger

def worker_process(task_path: str) -> dict:
    log = get_logger(f"Worker-{os.getpid()}")
    try:
        with open(task_path, 'r', encoding='utf-8') as f:
            task = json.load(f)
        
        target_file = task["target_file"]
        source_code = task["source_code"]
        
        # Sửa code trong bộ nhớ
        source_lines = source_code.splitlines(True)
        fixed_lines = source_lines[:]
        for act in task.get("actions", []):
            line_idx = act['line'] - 1
            if act['action'] == 'delete_line' and 0 <= line_idx < len(fixed_lines):
                del fixed_lines[line_idx]
        fixed_code = "".join(fixed_lines)

        # --- NÂNG CẤP: Mô phỏng & Tự kiểm thử ---
        # Ghi code đã sửa vào một file tạm để kiểm thử
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py', dir='.') as temp_file:
            temp_file.write(fixed_code)
            temp_file_path = temp_file.name
        
        test_passed = actions.run_pytest(temp_file_path)
        os.remove(temp_file_path) # Dọn dẹp file tạm

        if not test_passed:
            raise Exception("Bản vá không vượt qua kiểm thử tự động.")

        diff_report = "".join(difflib.unified_diff(
            source_code.splitlines(True), fixed_code.splitlines(True),
            fromfile='a/' + target_file, tofile='b/' + target_file
        ))

        return {
            "status": "success", "task_path": task_path, "target_file": target_file,
            "fixed_code": fixed_code, "diff_report": diff_report
        }
    except Exception as e:
        return {"status": "error", "task_path": task_path, "error": str(e), "target_file": task.get("target_file")}
