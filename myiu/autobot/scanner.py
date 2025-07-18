import subprocess
import json
from pathlib import Path

class CodeScanner:
    @staticmethod
    def scan_with_flake8(file_path: str) -> list:
        if not Path(file_path).is_file():
            return []
            
        try:
            # --- NÂNG CẤP CUỐI CÙNG: Ra lệnh trực tiếp cho flake8 ---
            # Chỉ tìm chính xác các lỗi F401 (unused import) và F841 (unused variable)
            command = ["flake8", "--select=F401,F841", file_path]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            
            issues = []
            if result.stdout:
                lines = result.stdout.strip().split('\\n')
                for line in lines:
                    if not line: continue
                    try:
                        parts = line.split(':', 3)
                        if len(parts) == 4:
                            code_part = parts[3].strip()
                            code = code_part.split(' ')[0]
                            text = code_part[len(code):].strip()
                            issues.append({
                                "line_number": int(parts[1]),
                                "column_number": int(parts[2]),
                                "code": code,
                                "text": text
                            })
                    except (ValueError, IndexError): continue
            return issues
        except Exception:
            return []
