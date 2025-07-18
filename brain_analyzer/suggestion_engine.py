from bot_worker.utils import log

class SuggestionEngine:
    def create_lint_suggestion_job(self, target_file: str, scan_results: list) -> dict | None:
        if not scan_results:
            return None
        actions = []
        if any(error["code"] == "W291" for error in scan_results):
            actions.append({"type": "trim_trailing_whitespace"})
        for error in scan_results:
            if error["code"] == "F841":
                actions.append({
                    "type": "replace_line",
                    "line_number": error["line_number"],
                    "new_content": f"# [MYIU-AUTO-FIX] {error['physical_line'].strip()}",
                })
            elif error["code"] == "F401":
                actions.append({"type": "delete_line", "line_number": error["line_number"]})
        if not actions:
            return None
        job_id = f"linting_{target_file.replace('/', '_').replace('.', '_')}"
        job = {
            "job_id": job_id,
            "source": "LintingEngine v1.1",
            "target_file": target_file,
            "actions": actions,
        }
        log.info(f"SuggestionEngine: Đã tạo Gói Công việc LINTING '{job_id}' với {len(actions)} hành động.")
        return job

    def create_formatting_job(self, target_file: str) -> dict:
        job_id = f"formatting_{target_file.replace('/', '_').replace('.', '_')}"
        job = {
            "job_id": job_id,
            "source": "FormattingEngine",
            "target_file": target_file,
            "actions": [{"type": "format_with_black", "target_file": target_file}],
        }
        log.info(f"SuggestionEngine: Đã tạo Gói Công việc FORMATTING '{job_id}'.")
        return job