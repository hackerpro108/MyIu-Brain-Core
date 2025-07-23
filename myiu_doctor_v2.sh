#!/bin/bash
# === KỊCH BẢN MYIU DOCTOR v2.1 (Phiên bản vá lỗi) ===
# Nâng cấp và Chẩn đoán Toàn diện Hệ thống MyIu

set -e

# ==============================================================================
# HÀM 1: NÂNG CẤP HỆ THỐNG VỚI "LƯỚI BẪY LỖI"
# ==============================================================================
upgrade_system() {
    echo "--- BẮT ĐẦU NÂNG CẤP HỆ THỐNG LÊN PHIÊN BẢN PHÒNG THỦ v2.1 ---"

    # --- 1.1: Nâng cấp `main.py` với Health Check Endpoint ---
    echo "▶️ Nâng cấp API Server với Health Check..."
    cat > /root/myiu-brain-core/main.py << 'EOF'
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from myiu.logging_config import setup_logging
from soma import Soma
from fortress_api import router as fortress_api_router
from myiu.websocket_manager import manager as websocket_manager
from fastapi import WebSocket, WebSocketDisconnect

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from soma import Soma
    app.state.soma = Soma(mode="api")
    await app.state.soma.start()
    yield
    await app.state.soma.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(fortress_api_router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API Server is running"}

@app.websocket("/ws/live_stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
EOF

    # --- 1.2: Nâng cấp `inference_worker.py` với Cơ chế "Nhịp tim" (ĐÃ SỬA LỖI) ---
    echo "▶️ Nâng cấp Worker với cơ chế Heartbeat (Phiên bản vá lỗi)..."
    cat > /root/myiu-brain-core/inference_worker.py << 'EOF'
import time, json, os
from pathlib import Path
from myiu.llm_core import LLMCore
from myiu.app_context import AppContext
from myiu.logging_config import setup_logging, get_logger

setup_logging()
log = get_logger("InferenceWorker")
app_context = AppContext()
with open("genome_static.json", "r") as f:
    app_context.set_service("genome_static_config", json.load(f))

TASKS_DIR = Path("tasks")
PENDING_DIR = TASKS_DIR / "inference/pending"
COMPLETED_DIR = TASKS_DIR / "inference/completed"
HEARTBEAT_FILE = TASKS_DIR / "worker_heartbeat.txt"

def process_task(task_path, llm):
    task_id = task_path.name
    result_path = COMPLETED_DIR / task_id
    response = ""
    try:
        log.info(f"Nhận tác vụ mới: {task_id}")
        with open(task_path, 'r', encoding='utf-8') as f:
            task_data = json.load(f)
        prompt = task_data.get("prompt")
        if not prompt or not prompt.strip():
            raise ValueError("Nhiệm vụ nhận được không có nội dung (prompt rỗng).")
        response = llm.generate_response(prompt)
        log.info(f"Hoàn thành tác vụ: {task_id}")
    except Exception as e:
        log.error(f"Lỗi khi xử lý tác vụ {task_id}: {e}", exc_info=True)
        response = f"Xin lỗi sếp, tôi đã gặp lỗi khi đang suy nghĩ: {e}"
    finally:
        with open(result_path, 'w', encoding='utf-8') as f:
            json.dump({"response": response}, f, ensure_ascii=False)
        os.remove(task_path)

def main_loop():
    log.info("Inference Worker đang khởi tạo...")
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    COMPLETED_DIR.mkdir(parents=True, exist_ok=True)
    
    llm = LLMCore(app_context)
    llm.llm = llm._load_model()
    if not llm.llm:
        log.critical("Không thể tải model. Worker thoát.")
        return
    log.info("✅ Worker (Hardened) đã sẵn sàng.")
    while True:
        try:
            with open(HEARTBEAT_FILE, "w") as f:
                f.write(str(time.time()))
            
            tasks = list(PENDING_DIR.glob("*.json"))
            if tasks:
                for task in tasks:
                    process_task(task, llm)
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error(f"Lỗi trong vòng lặp chính: {e}", exc_info=True)
            time.sleep(5)

if __name__ == "__main__":
    main_loop()
EOF

    echo "▶️ Đang khởi động lại dịch vụ để áp dụng nâng cấp..."
    sudo systemctl restart myiu-api.service
    sudo systemctl restart myiu-worker.service
    sleep 2
    echo "✅ HỆ THỐNG ĐÃ ĐƯỢC NÂNG CẤP THÀNH CÔNG!"
}

# ==============================================================================
# HÀM 2: CHẠY "LƯỚI BẪY LỖI" ĐỂ CHẨN ĐOÁN TOÀN DIỆN
# ==============================================================================
run_diagnostics() {
    echo "--- BẮT ĐẦU CHẨN ĐOÁN TOÀN DIỆN HỆ THỐNG ---"
    
    echo -e "\n\n=== 1. KIỂM TRA TRẠNG THÁI DỊCH VỤ (SYSTEMD) ==="
    sudo systemctl status myiu-api.service --no-pager
    echo "--------------------------------------------------"
    sudo systemctl status myiu-worker.service --no-pager

    echo -e "\n\n=== 2. KIỂM TRA SỨC KHỎE API SERVER (HEALTH CHECK) ==="
    curl -s http://localhost:8000/health || echo "LỖI: Không thể kết nối đến Health Check API."
    
    echo -e "\n\n=== 3. KIỂM TRA NHỊP TIM CỦA WORKER (HEARTBEAT) ==="
    if [ -f tasks/worker_heartbeat.txt ]; then
        LAST_BEAT=$(cat tasks/worker_heartbeat.txt)
        CURRENT_TIME=$(date +%s)
        TIME_DIFF=$(($CURRENT_TIME - $(printf "%.0f" $LAST_BEAT)))
        if [ $TIME_DIFF -lt 10 ]; then
            echo "✅ Worker đang hoạt động tốt (Nhịp tim cuối: $TIME_DIFF giây trước)."
        else
            echo " LỖI: Worker có thể đã bị treo (Nhịp tim cuối: $TIME_DIFF giây trước)."
        fi
    else
        echo " LỖI: Không tìm thấy file nhịp tim của Worker."
    fi

    echo -e "\n\n=== 4. PHÂN TÍCH LOG GẦN NHẤT ==="
    echo "--- Log của API Server (20 dòng cuối):"
    sudo journalctl -u myiu-api.service -n 20 --no-pager
    echo -e "\n--- Log của Worker (20 dòng cuối):"
    sudo journalctl -u myiu-worker.service -n 20 --no-pager
    
    echo -e "\n\n=== 5. KIỂM TRA TÀI NGUYÊN HỆ THỐNG ==="
    echo "--- Bộ nhớ RAM & Swap:"
    free -h
    echo -e "\n--- Dung lượng ổ đĩa:"
    df -h /

    echo -e "\n--- HOÀN TẤT CHẨN ĐOÁN ---"
}


# --- Main Logic ---
case "$1" in
    upgrade)
        upgrade_system
        ;;
    diagnose)
        run_diagnostics
        ;;
    *)
        echo "Sử dụng: $0 {upgrade|diagnose}"
        echo "  upgrade:   Nâng cấp đồng loạt hệ thống với cơ chế Health Check & Heartbeat."
        echo "  diagnose:  Chạy lưới bẫy lỗi để kiểm tra sức khỏe toàn bộ hệ thống."
        exit 1
        ;;
esac