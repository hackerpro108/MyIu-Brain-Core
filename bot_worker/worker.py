# bot_worker/worker.py
import os
import shutil
import uuid
from .config import PROJECT_ROOT
from .utils import log
from .actions import CodeActions


class Worker:
    def __init__(self, job_id: str = None):
        self.job_id = job_id if job_id else str(uuid.uuid4())
        self.log = log

    def execute_job(self, logic_data: dict) -> dict:
        self.log.info(f"[Job: {self.job_id}] Bắt đầu thực thi.")
        target_file_relative = logic_data.get("target_file")
        if not target_file_relative:
            return self._report(
                "FAILED_PRECONDITION", "Gói công việc thiếu 'target_file'."
            )

        actions = logic_data.get("actions", [])
        target_file_absolute = os.path.join(PROJECT_ROOT, target_file_relative)
        backup_file_path = f"{target_file_absolute}.{self.job_id}.bak"

        try:
            shutil.copy(target_file_absolute, backup_file_path)
            self.log.info(
                f"[Job: {self.job_id}] Đã tạo Time Capsule tại: {backup_file_path}"
            )
        except FileNotFoundError:
            error_msg = f"Lỗi: Không tìm thấy file mục tiêu '{target_file_absolute}'. Dừng thực thi."
            self.log.error(f"[Job: {self.job_id}] {error_msg}")
            return self._report("FAILED_PRECONDITION", error_msg, success=False)
        except Exception as e:
            error_msg = f"Lỗi khi tạo Time Capsule cho '{target_file_absolute}': {e}"
            self.log.error(f"[Job: {self.job_id}] {error_msg}")
            return self._report("FAILED_PRECONDITION", error_msg, success=False)

        try:
            with open(backup_file_path, "r", encoding="utf-8") as f:
                content_in_memory = f.read()

            original_content = content_in_memory
            action_logs = []
            actions_failed_count = 0

            line_based_actions = [a for a in actions if "line_number" in a]
            other_actions = [a for a in actions if "line_number" not in a]
            line_based_actions.sort(key=lambda x: x.get("line_number", 0), reverse=True)

            for i, action_data in enumerate(other_actions):
                action_type = action_data.get("type")
                action_func = CodeActions.get_action(action_type)

                if action_func:
                    params = {k: v for k, v in action_data.items() if k != "type"}
                    success, content_in_memory = action_func(
                        content_in_memory, **params
                    )
                    if success:
                        action_logs.append(
                            f"Hành động '{action_type}' đã được áp dụng thành công."
                        )
                    else:
                        actions_failed_count += 1
                        self.log.error(
                            f"[Job: {self.job_id}] Hành động '{action_type}' thất bại."
                        )
                else:
                    actions_failed_count += 1
                    self.log.error(
                        f"[Job: {self.job_id}] Hành động không xác định '{action_type}'."
                    )

            for i, action_data in enumerate(line_based_actions):
                action_type = action_data.get("type")
                action_func = CodeActions.get_action(action_type)

                if action_func:
                    params = {k: v for k, v in action_data.items() if k != "type"}
                    success, content_in_memory = action_func(
                        content_in_memory, **params
                    )
                    if success:
                        action_logs.append(
                            f"Hành động '{action_type}' (dòng {action_data.get('line_number', '')}) đã được áp dụng thành công."
                        )
                    else:
                        actions_failed_count += 1
                        self.log.error(
                            f"[Job: {self.job_id}] Hành động '{action_type}' (dòng {action_data.get('line_number', '')}) thất bại."
                        )
                else:
                    actions_failed_count += 1
                    self.log.error(
                        f"[Job: {self.job_id}] Hành động không xác định '{action_type}'."
                    )

            if actions_failed_count > 0:
                raise ValueError(f"{actions_failed_count} hành động thất bại.")

            if content_in_memory != original_content:
                self.log.info(
                    f"[Job: {self.job_id}] Phát hiện có thay đổi. Đang ghi lại nội dung mới vào file '{target_file_absolute}'."
                )
                with open(target_file_absolute, "w", encoding="utf-8") as f:
                    f.write(content_in_memory)
                self.log.info("[Job: {self.job_id}] Ghi file thành công.")
                return self._report(
                    "SUCCESS_COMPLETED",
                    "File đã được cập nhật.",
                    action_logs,
                    backup_file_path,
                    True,
                )
            else:
                self.log.info(
                    "[Job: {self.job_id}] Không có thay đổi nào được thực hiện trên file."
                )
                return self._report(
                    "SUCCESS_NO_CHANGE",
                    "Không có thay đổi nào được thực hiện.",
                    action_logs,
                    backup_file_path,
                    True,
                )

        except Exception as e:
            self.log.error(
                f"[Job: {self.job_id}] Giao dịch thất bại: {e}. Kích hoạt Rollback!"
            )
            if os.path.exists(backup_file_path):
                shutil.move(backup_file_path, target_file_absolute)
            else:
                self.log.warning(
                    f"[Job: {self.job_id}] Không tìm thấy Time Capsule để khôi phục: {backup_file_path}"
                )
            return self._report(
                "FAILED_EXECUTION",
                f"Lỗi thực thi: {e}",
                action_logs,
                backup_file_path,
                False,
            )

    def _report(
        self,
        status: str,
        details: str,
        summary: list = None,
        backup_path: str = None,
        success: bool = False,
    ) -> dict:
        if success and backup_path and os.path.exists(backup_path):
            try:
                os.remove(backup_path)
                self.log.info(
                    f"[Job: {self.job_id}] Đã xóa Time Capsule thành công: {backup_path}"
                )
            except Exception as e:
                self.log.warning(
                    f"[Job: {self.job_id}] Không thể xóa Time Capsule '{backup_path}': {e}"
                )
        elif not success and backup_path and os.path.exists(backup_path):
            self.log.info(
                f"[Job: {self.job_id}] Đã khôi phục file gốc từ Time Capsule: {backup_path}"
            )

        self.log.info(f"[Job: {self.job_id}] Công việc kết thúc. Trạng thái: {status}")
        return {"status": status, "details": details, "summary": summary or []}
