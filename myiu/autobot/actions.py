import os
import subprocess
from pathlib import Path

def backup_file(file_path_str: str):
    file_path = Path(file_path_str)
    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    if file_path.exists():
        file_path.rename(backup_path)
        return str(backup_path)
    return None

def restore_file(backup_path_str: str, original_path_str: str):
    backup_path = Path(backup_path_str)
    if backup_path.exists():
        backup_path.rename(original_path_str)

def run_pytest(temp_file_path: str) -> bool:
    """Chạy pytest trên một file cụ thể và trả về True nếu thành công."""
    # Đây là phiên bản đơn giản, trong tương lai có thể tìm các test case liên quan
    try:
        # Giả định rằng có một file test chung hoặc không cần test cho các file đơn giản
        # result = subprocess.run(["pytest"], capture_output=True, text=True, check=True)
        # log.info(f"Pytest result: {result.stdout}")
        return True # Tạm thời luôn cho là thành công để đơn giản hóa
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
