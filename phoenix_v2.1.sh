#!/bin/bash
# === KỊCH BẢN MYIU PHOENIX v2.1 (Phiên bản vá lỗi systemd) ===
# Tái sinh với Quy trình Tải file Chuyên nghiệp & Thẩm định Nghiêm ngặt

set -e

# --- CÁC BIẾN CẤU HÌNH ---
MODEL_REPO="TheBloke/phi-2-GGUF"
MODEL_FILENAME="phi-2.Q4_K_M.gguf"
MODEL_DIR="/root/models/phi-2"
MODEL_FULL_PATH="${MODEL_DIR}/${MODEL_FILENAME}"
EXPECTED_SHA256="324356668fa5ba9f4135de348447bb2bbe2467eaa1b8fcfb53719de62fbd2499"
PYTHON_EXEC="/root/myiu-brain-core/myiu_env/bin/python3"

echo "--- BẮT ĐẦU KỊCH BẢN PHOENIX v2.1 ---"
read -p "Sếp có chắc chắn muốn TÁI SINH toàn bộ hệ thống? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Đã hủy bỏ."
    exit 1
fi

# --- GIAI ĐOẠN 1: "GÂY MÊ" HỆ THỐNG ---
echo "▶️ [1/4] Đang giải phóng tài nguyên hệ thống..."
sudo systemctl stop myiu-api.service || true
sudo systemctl stop myiu-worker.service || true
echo "✅ Đã dừng các dịch vụ để giải phóng RAM."

# --- GIAI ĐOẠN 2: "PHẪU THUẬT" NÃO BỘ ---
echo "▶️ [2/4] Bắt đầu quá trình TÁI SINH Não bộ..."

# 2.1: Dọn dẹp file cũ và cache
echo "    - Đang dọn dẹp các file model cũ/hỏng và cache..."
sudo rm -f "${MODEL_DIR}/*.gguf"
sudo rm -rf ~/.cache/huggingface/hub
sudo mkdir -p "$MODEL_DIR"

# 2.2: Tải "Não bộ" với quy trình chuyên nghiệp
# ... (Phần này giữ nguyên, đã hoạt động tốt)
# ...
export HF_HUB_ENABLE_HF_TRANSFER=0 
if huggingface-cli download "$MODEL_REPO" "$MODEL_FILENAME" --local-dir "$MODEL_DIR" --local-dir-use-symlinks False --revision main; then
    echo "    - ✅ Tải bằng huggingface-cli thành công."
else
    echo "    - ⚠️ huggingface-cli thất bại. Chuyển sang aria2c (dự phòng 2)..."
    if ! command -v aria2c &> /dev/null; then sudo apt-get update && sudo apt-get install -y aria2; fi
    MODEL_DOWNLOAD_URL="https://huggingface.co/${MODEL_REPO}/resolve/main/${MODEL_FILENAME}"
    if aria2c -x 4 -s 4 -k 1M --retry-wait=5 --max-tries=0 "$MODEL_DOWNLOAD_URL" -d "$MODEL_DIR" -o "$MODEL_FILENAME"; then
        echo "    - ✅ Tải bằng aria2c thành công."
    else
        echo "    - ❌ LỖI NGHIÊM TRỌNG: Cả hai phương pháp tải đều thất bại."
        exit 1
    fi
fi

# 2.3: Thẩm định "Não bộ"
echo "    - Đang thẩm định tính toàn vẹn của file model (SHA256)..."
DOWNLOADED_SHA256=$(sha256sum "$MODEL_FULL_PATH" | awk '{print $1}')
if [ "$DOWNLOADED_SHA256" = "$EXPECTED_SHA256" ]; then
    echo "    - ✅ THẨM ĐỊNH THÀNH CÔNG. NÃO BỘ KHỎE MẠNH."
else
    echo "    - ❌ LỖI NGHIÊM TRỌNG: File model mới tải về vẫn bị hỏng!"
    exit 1
fi

# 2.4: Nâng cấp các file cấu hình và mã nguồn
echo "    - Đang cập nhật mã nguồn và cấu hình..."
# ... (Nội dung các file code giữ nguyên như cũ)
# ...
cat > /root/myiu-brain-core/genome_static.json << 'EOF'
{"llm_config": {"model_path": "/root/models/phi-2/phi-2.Q4_K_M.gguf", "n_ctx": 2048, "n_threads": 2, "response_timeout_seconds": 120}}
EOF
cat > /root/myiu-brain-core/myiu/llm_core.py << 'EOF'
import os; from llama_cpp import Llama; from myiu.async_module import AsyncModule
class LLMCore(AsyncModule):
    def __init__(self, app_context):
        super().__init__(app_context); self.llm=None; genome=app_context.get_service("genome_static_config"); cfg=genome.get("llm_config",{}); self.model_path=cfg.get("model_path"); self.model_params={"n_ctx":cfg.get("n_ctx",2048),"n_threads":cfg.get("n_threads",2),"n_gpu_layers":0,"verbose":False}
    def _load_model(self): self.log.info(f"LLMCore: Tải model với cấu hình: {self.model_params}"); return Llama(model_path=self.model_path,**self.model_params)
    def generate_response(self,prompt,max_tokens=256):
        if not self.llm: return "Lỗi: Lõi suy luận chưa sẵn sàng."
        manual_prompt=f"Instruct: {prompt}\nOutput:"; output=self.llm(prompt=manual_prompt,max_tokens=max_tokens,stop=["Instruct:","\n"],echo=False)
        return output['choices'][0]['text'].strip()
EOF

# === DÒNG SỬA LỖI QUAN TRỌNG NHẤT ===
# Sửa lại cú pháp file systemd cho đúng chuẩn
cat > /etc/systemd/system/myiu-worker.service << 'EOF'
[Unit]
Description=MyIu Inference Worker (Optimized)
After=network.target

[Service]
User=root
WorkingDirectory=/root/myiu-brain-core
ExecStart=/root/myiu-brain-core/myiu_env/bin/python inference_worker.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
# ====================================

echo "✅ Hoàn tất quá trình phẫu thuật."

# --- GIAI ĐOẠN 3: "HỒI SỨC" HỆ THỐNG ---
echo "▶️ [3/3] Đang khởi động lại hệ thống với Não bộ mới..."
sudo systemctl daemon-reload
sudo systemctl restart myiu-worker.service
sudo systemctl restart myiu-api.service
sleep 5
echo "▶️ [4/4] Kiểm tra trạng thái cuối cùng..."
sudo systemctl status myiu-worker.service --no-pager

echo "--- HOÀN TẤT KỊCH BẢN PHOENIX v2.1 ---"