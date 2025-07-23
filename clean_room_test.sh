#!/bin/bash
# === KỊCH BẢN CLEAN ROOM TEST v1.0 ===
# Thẩm định Lõi Suy luận trong một môi trường hoàn toàn bị cô lập

set -e

# --- CÁC BIẾN CẤU HÌNH ---
VENV_DIR="/tmp/myiu_test_env"
TEST_SCRIPT_PATH="/tmp/test_core.py"
MODEL_PATH="/root/models/phi-2/phi-2.Q4_K_M.gguf"
FLAG_FILE="/root/models/test_failed.flag"
PYTHON_EXEC="${VENV_DIR}/bin/python3"

echo "--- BẮT ĐẦU QUY TRÌNH THẨM ĐỊNH LÕI SUY LUẬN ---"

# --- GIAI ĐOẠN 1: TẠO MÔI TRƯỜNG SẠCH ---
echo "▶️ [1/4] Đang tạo môi trường ảo bị cô lập tại ${VENV_DIR}..."
rm -rf "$VENV_DIR"
python3 -m venv "$VENV_DIR"
echo "✅ Môi trường đã được tạo."

# --- GIAI ĐOẠN 2: CÀI ĐẶT TỐI THIỂU ---
echo "▶️ [2/4] Đang cài đặt các thư viện cần thiết..."
$PYTHON_EXEC -m pip install --upgrade pip
$PYTHON_EXEC -m pip install llama-cpp-python psutil
echo "✅ Cài đặt hoàn tất."

# --- GIAI ĐOẠN 3: TẠO "ROBOT THỬ NGHIỆM" ---
echo "▶️ [3/4] Đang tạo kịch bản test_core.py với các cơ chế an toàn..."
cat > "$TEST_SCRIPT_PATH" << 'EOF'
#!/usr/bin/env python3
import signal
import sys
import os
import psutil
from llama_cpp import Llama

# === CẤU HÌNH ===
MODEL_PATH = "/root/models/phi-2/phi-2.Q4_K_M.gguf"
FLAG_FILE = "/root/models/test_failed.flag"
TIMEOUT_SECONDS = 45

# === CƠ CHẾ AN TOÀN: TIMEOUT ===
def timeout_handler(signum, frame):
    print("❌ LỖI: QUÁ TRÌNH SUY LUẬN BỊ TREO (TIMEOUT)!", file=sys.stderr)
    with open(FLAG_FILE, "w") as f:
        f.write("timeout")
    sys.exit(1)

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(TIMEOUT_SECONDS)

# === HÀM GIÁM SÁT TÀI NGUYÊN ===
def get_memory_usage():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 * 1024) # Trả về MB

# === QUY TRÌNH THỬ NGHIỆM CHÍNH ===
try:
    print(f"--- Bắt đầu thử nghiệm với model: {MODEL_PATH} ---")
    
    if not os.path.exists(MODEL_PATH):
        print(f"❌ LỖI: Không tìm thấy file model tại '{MODEL_PATH}'", file=sys.stderr)
        with open(FLAG_FILE, "w") as f: f.write("model_not_found")
        sys.exit(1)

    mem_before = get_memory_usage()
    print(f"RAM trước khi tải model: {mem_before:.2f} MB")
    
    # Tải model với cấu hình tối giản nhất
    llm = Llama(model_path=MODEL_PATH, n_gpu_layers=0, verbose=False)
    
    mem_after = get_memory_usage()
    print(f"RAM sau khi tải model: {mem_after:.2f} MB")
    
    # Thử nghiệm suy luận
    prompt = "Instruct: Calculate 2 + 2.\nOutput:"
    print(f"\nPrompt đầu vào:\n{prompt}")
    
    response = llm(prompt=prompt, max_tokens=10, stop=["\n", "Instruct:"], temperature=0.0)
    
    result_text = response["choices"][0]["text"].strip()
    print(f"\nPhản hồi thô từ model:\n{result_text}")
    
    # Xác thực kết quả
    assert "4" in result_text, f"Kết quả không chính xác! Không tìm thấy '4' trong '{result_text}'"
    
    print("\n✅ THỬ NGHIỆM THÀNH CÔNG! Lõi suy luận hoạt động đúng.")

except Exception as e:
    print(f"❌ LỖI NGHIÊM TRỌNG TRONG QUÁ TRÌNH THỬ NGHIỆM: {e}", file=sys.stderr)
    with open(FLAG_FILE, "w") as f:
        f.write(str(e))
    sys.exit(2)
finally:
    # Tắt chuông báo timeout
    signal.alarm(0)
EOF
echo "✅ Robot thử nghiệm đã được tạo."

# --- GIAI ĐOẠN 4: THỰC THI & DỌN DẸP ---
echo "▶️ [4/4] BẮT ĐẦU THỰC THI THỬ NGHIỆM..."
echo "--------------------------------------------------"
if $PYTHON_EXEC "$TEST_SCRIPT_PATH"; then
    echo "--------------------------------------------------"
    echo " KẾT LUẬN: Lỗi nằm ở KIẾN TRÚC MYIU (Soma, Cortex, Worker)."
    rm -f "$FLAG_FILE" # Xóa cờ lỗi nếu thành công
else
    echo "--------------------------------------------------"
    echo " KẾT LUẬN: Lỗi nằm ở THƯ VIỆN LLAMA.CPP hoặc FILE MODEL."
fi

echo "▶️ Đang dọn dẹp môi trường thử nghiệm..."
rm -rf "$VENV_DIR" "$TEST_SCRIPT_PATH"
echo "✅ Dọn dẹp hoàn tất."
echo "--- KẾT THÚC QUY TRÌNH THẨM ĐỊNH ---"
