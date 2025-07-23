#!/bin/bash
# === KỊCH BẢN MYIU ORACLE v1.1 (Phiên bản vá lỗi) ===
# Nâng cấp Hệ thống với Khả năng Tự chẩn đoán và Báo cáo Tích hợp
set -e

echo "--- BẮT ĐẦU NÂNG CẤP LÊN KIẾN TRÚC TỰ CHẨN ĐOÁN (v1.1) ---"

# --- GIAI ĐOẠN 1: DẠY "NGƯỜI THỢ" CÁCH VIẾT BÁO CÁO ---
echo "▶️ [1/2] Đang nâng cấp 'Người Thợ Suy luận' (inference_worker.py)..."
cat > /root/myiu-brain-core/inference_worker.py << 'EOF'
# Tên file: inference_worker.py (Phiên bản Báo cáo)
import time, json, os, traceback
from pathlib import Path
from myiu.llm_core import LLMCore
from myiu.app_context import AppContext
from myiu.logging_config import setup_logging, get_logger

setup_logging()
log = get_logger("InferenceWorker")
app_context = AppContext()
with open("genome_static.json", "r") as f:
    app_context.set_service("genome_static_config", json.load(f))

PENDING_DIR, COMPLETED_DIR = Path("tasks/inference/pending"), Path("tasks/inference/completed")

def process_task(task_path: Path, llm_core: LLMCore):
    task_id = task_path.stem
    result_path = COMPLETED_DIR / task_path.name
    response_payload = {}
    
    try:
        log.info(f"Worker: Nhận tác vụ mới: {task_id}")
        with open(task_path, 'r') as f:
            task_data = json.load(f)

        prompt = task_data.get("prompt")
        if not prompt or not prompt.strip():
            raise ValueError("Nhiệm vụ nhận được không có nội dung (prompt rỗng).")
        
        response_text = llm_core.generate_response(prompt)
        response_payload = {"status": "success", "response": response_text}
        log.info(f"Worker: Hoàn thành tác vụ: {task_id}")

    except Exception as e:
        log.error(f"Worker: Lỗi nghiêm trọng khi xử lý tác vụ {task_id}: {e}", exc_info=True)
        error_report = traceback.format_exc()
        response_payload = {
            "status": "failed",
            "response": f"Xin lỗi sếp, tôi đã gặp một lỗi nghiêm trọng khi đang suy nghĩ.",
            "error_details": error_report
        }
    finally:
        with open(result_path, 'w') as f:
            json.dump(response_payload, f, ensure_ascii=False)
        os.remove(task_path)

def main_loop():
    llm_core = LLMCore(app_context)
    if not llm_core.llm:
        log.critical("Worker: Không thể tải model. Worker sẽ không khởi động.")
        return
    log.info("✅ Worker (Oracle) đã sẵn sàng.")
    while True:
        try:
            tasks = list(PENDING_DIR.glob("*.json"))
            if tasks:
                for task in tasks:
                    process_task(task, llm_core)
            time.sleep(1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            log.error(f"Worker: Lỗi nghiêm trọng trong vòng lặp chính: {e}", exc_info=True)
            time.sleep(5)

if __name__ == "__main__":
    main_loop()
EOF

# --- GIAI ĐOẠN 2: DẠY "QUẢN ĐỐC" CÁCH ĐỌC BÁO CÁO (ĐÃ SỬA LỖI) ---
echo "▶️ [2/2] Đang nâng cấp 'Vỏ não' (cortex.py)..."
cat > /root/myiu-brain-core/myiu/cortex.py << 'EOF'
# Tên file: myiu/cortex.py (Phiên bản Báo cáo - Đã sửa lỗi)
import asyncio, json, uuid, os, time, traceback
from datetime import datetime
from pathlib import Path
from myiu.async_module import AsyncModule
from myiu.websocket_manager import manager as websocket_manager

print("🔥 Cortex Oracle (v1.1) đã hoạt động!")

PENDING_DIR = Path("tasks/inference/pending")
COMPLETED_DIR = Path("tasks/inference/completed")

class Cortex(AsyncModule):
    def __init__(self, app_context):
        super().__init__(app_context)
        self.response_timeout = 60
        self.thought_stream = None

    async def start(self):
        await super().start()
        self.thought_stream = self.app_context.get_service("thought_stream")
        genome = self.app_context.get_service("genome_static_config")
        self.response_timeout = genome.get("llm_config", {}).get("response_timeout_seconds", 60)
        PENDING_DIR.mkdir(parents=True, exist_ok=True)
        COMPLETED_DIR.mkdir(parents=True, exist_ok=True)
        self.log.info("Cortex Oracle (v1.1) đã sẵn sàng.")

    async def process_user_message(self, text: str) -> dict:
        task_id_base = str(uuid.uuid4())
        
        if not text or not text.strip():
            return {'id': f'myiu-reject-{task_id_base}', 'text': "Yêu cầu rỗng.", 'type': 'myiu', 'timestamp': datetime.now().isoformat()}

        message = text.strip()
        
        await self._log_thought(f"Cortex: Tạo tác vụ {task_id_base} cho '{message}'...")

        try:
            task_path = PENDING_DIR / f"{task_id_base}.json"
            result_path = COMPLETED_DIR / f"{task_id_base}.json"
            
            with open(task_path, 'w') as f: json.dump({"prompt": message}, f)

            start_time = time.time()
            while not result_path.exists():
                if time.time() - start_time > self.response_timeout:
                    raise asyncio.TimeoutError
                await asyncio.sleep(0.1)

            with open(result_path, 'r') as f:
                result_data = json.load(f)

            final_response = {
                'id': f'myiu-response-{task_id_base}',
                'text': result_data.get("response", "Lỗi: Worker không trả về phản hồi."),
                'type': 'myiu',
                'timestamp': datetime.now().isoformat()
            }
            if "error_details" in result_data:
                final_response["error_details"] = result_data["error_details"]
                self.log.warning(f"Cortex: Worker đã báo cáo lỗi cho tác vụ {task_id_base}. Chi tiết đã được gửi về Pháo đài.")

            os.remove(result_path)
            return final_response

        except Exception as e:
            self.log.error(f"Cortex: Lỗi nghiêm trọng khi quản lý tác vụ {task_id_base}: {e}", exc_info=True)
            return {
                'id': f'myiu-error-{task_id_base}',
                'text': "Lỗi hệ thống tại Cortex.",
                'type': 'system',
                'timestamp': datetime.now().isoformat(),
                'error_details': traceback.format_exc()
            }

    async def _log_thought(self, content: str):
        from myiu.perception.thought_chunk import ThoughtChunk
        chunk = ThoughtChunk(origin="Cortex", content=content)
        if self.thought_stream:
            self.thought_stream.record(chunk)
        await websocket_manager.broadcast(content)

    async def stop(self):
        await super().stop()
EOF

echo "✅ Đã nâng cấp thành công."
echo "▶️ Đang khởi động lại hệ thống..."
sudo systemctl restart myiu-api.service
sudo systemctl restart myiu-worker.service
echo "--- HOÀN TẤT KỊCH BẢN ORACLE v1.1 ---"