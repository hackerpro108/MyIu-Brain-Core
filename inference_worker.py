# Tên file: inference_worker.py (Phiên bản Đồng bộ)
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
        
        # Gọi trực tiếp hàm đồng bộ
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
    log.info("✅ Worker (Synchronized) đã sẵn sàng.")
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
