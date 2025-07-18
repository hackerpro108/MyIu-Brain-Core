import json
import uuid
from datetime import datetime
from pathlib import Path

class SuggestionEngine:
    @staticmethod
    def create_autofix_task(file_path: str, issues: list, source_code: str) -> str:
        actions_to_perform = []
        for issue in issues:
            if issue['code'] in ['F401', 'F841']:
                actions_to_perform.append({
                    "action": "delete_line",
                    "line": issue['line_number'],
                })
        
        if not actions_to_perform:
            return None

        task_id = str(uuid.uuid4())
        task = {
            "task_id": task_id,
            "target_file": file_path,
            # --- NÂNG CẤP: Gửi kèm nội dung code trong tác vụ ---
            "source_code": source_code,
            "actions": actions_to_perform
        }
        
        task_file_path = Path("tasks/pending") / f"{task_id}.json"
        with open(task_file_path, 'w', encoding='utf-8') as f:
            json.dump(task, f, indent=2)
            
        return str(task_file_path)
