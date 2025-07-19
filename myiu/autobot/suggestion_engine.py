import json
import uuid
from pathlib import Path

# BƯỚC 3: Linh hoạt hóa Logic - Tách các quy tắc ra khỏi logic chính
# Hệ thống quy tắc này giúp việc thêm/sửa/xóa các đề xuất cực kỳ dễ dàng
# mà không cần thay đổi code của hàm.
RULES = {
    "F401": {
        "action": "delete_line",
        "reason_template": "Unused import: '{module_name}'",
        "confidence": 0.99
    },
    "F841": {
        "action": "delete_line",
        "reason_template": "Unused local variable: '{variable_name}'",
        "confidence": 0.98
    }
    # Thêm các quy tắc mới cho các mã lỗi khác ở đây.
    # Ví dụ: "E302": {"action": "insert_line", "content": "\n", ...}
}

class SuggestionEngine:
    """
    SuggestionEngine phân tích các vấn đề (issues) từ linter và đề xuất
    các hành động sửa lỗi tự động (autofix).
    """
    @staticmethod
    def create_autofix_task(file_path: str, issues: list, source_code: str) -> str:
        """
        Tạo một tác vụ sửa lỗi tự động dựa trên danh sách các vấn đề.

        Args:
            file_path (str): Đường dẫn đến file cần phân tích.
            issues (list): Danh sách các vấn đề, mỗi vấn đề là một dict
                           chứa 'code', 'line_number', 'text', v.v.
            source_code (str): Nội dung mã nguồn của file.

        Returns:
            str: Đường dẫn đến file tác vụ JSON đã được tạo, hoặc None nếu
                 không có hành động nào được đề xuất.
        """
        actions_to_perform = []
        for issue in issues:
            rule = RULES.get(issue['code'])
            if rule:
                # BƯỚC 2: Mở rộng Trí tuệ - Thêm "Lý do" và "Độ tự tin"
                # Tự động điền lý do và độ tự tin từ hệ thống RULES.
                # 'issue' chứa thông tin chi tiết để điền vào 'reason_template'.
                # (Phần này có thể nâng cấp thêm để trích xuất tên biến/module)
                reason = rule['reason_template'].format(
                    module_name=issue.get('text', '').split("'")[1] if 'F401' in issue['code'] else 'unknown',
                    variable_name=issue.get('text', '').split("'")[1] if 'F841' in issue['code'] else 'unknown'
                )

                actions_to_perform.append({
                    "action": rule['action'],
                    "line": issue['line_number'],
                    "reason": reason,
                    "confidence": rule['confidence']
                })

        if not actions_to_perform:
            return None

        task_id = str(uuid.uuid4())
        task = {
            "task_id": task_id,
            "target_file": file_path,
            "source_code": source_code,
            "actions": actions_to_perform
        }

        # BƯỚC 1: "Dọn nhà" - Đảm bảo thư mục tồn tại trước khi ghi file
        task_dir = Path("tasks/pending")
        task_dir.mkdir(parents=True, exist_ok=True)
        task_file_path = task_dir / f"{task_id}.json"

        with open(task_file_path, 'w', encoding='utf-8') as f:
            json.dump(task, f, indent=4, ensure_ascii=False)

        return str(task_file_path)
