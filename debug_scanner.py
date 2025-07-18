import subprocess
import os

print("--- BẮT ĐẦU KIỂM TRA CHẨN ĐOÁN SCANNER ---")

# Bước 1: Xác định vị trí của flake8
try:
    which_result = subprocess.run(["which", "flake8"], capture_output=True, text=True, check=True)
    flake8_path = which_result.stdout.strip()
    print(f"✅ Đã tìm thấy 'flake8' tại: {flake8_path}")
except Exception as e:
    print(f"❌ LỖI: Không tìm thấy lệnh 'flake8'. Vui lòng kiểm tra lại cài đặt. Lỗi: {e}")
    print("--- KẾT THÚC KIỂM TRA ---")
    exit()

# Bước 2: Chạy lệnh flake8 và in tất cả output
file_to_scan = "test_file_unused_import.py"
print(f"\\n--- Đang thực thi lệnh với file '{file_to_scan}' ---")

try:
    command = [flake8_path, "--format=json", file_to_scan]
    result = subprocess.run(
        command, 
        capture_output=True, 
        text=True, 
        check=False,
        timeout=15
    )
    
    print("\\n--- KẾT QUẢ THỰC THI ---")
    print(f"Mã thoát (Exit Code): {result.returncode}")
    
    print("\\n--- DỮ LIỆU OUTPUT CHUẨN (STDOUT) ---")
    print("Bắt đầu output chuẩn >>>")
    print(result.stdout)
    print("<<< Kết thúc output chuẩn")
    
    print("\\n--- DỮ LIỆU OUTPUT LỖI (STDERR) ---")
    print("Bắt đầu output lỗi >>>")
    print(result.stderr)
    print("<<< Kết thúc output lỗi")

except Exception as e:
    print(f"\\n*** LỖI NGOẠI LỆ KHI CHẠY KỊCH BẢN: {e} ***")

print("\\n--- KẾT THÚC KIỂM TRA ---")
