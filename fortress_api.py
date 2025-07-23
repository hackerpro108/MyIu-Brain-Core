# Tên file: fortress_api.py (đã dọn dẹp)
import uuid
from datetime import datetime
from fastapi import APIRouter, Request, Depends
from myiu.logging_config import get_logger
from soma import Soma # <-- Quay trở lại import ở đầu file

router = APIRouter()
log = get_logger("fortress_api")

def get_soma_instance(request: Request) -> Soma:
    return request.app.state.soma

@router.post("/ipc/message")
async def handle_fortress_message(request: Request, soma_instance: Soma = Depends(get_soma_instance)):
  
    # === DÒNG SỬA LỖI QUAN TRỌNG NHẤT ===
    # Import Soma ngay tại thời điểm cần dùng để phá vỡ vòng lặp
    from soma import Soma
    # ====================================

    log.info("--- API Fortress: Đã nhận được yêu cầu từ Pháo đài ---")
    try:
        event_data = await request.json()
        soma_instance = request.app.state.soma

        cortex = soma_instance.app_context.get_service("cortex")

        if not cortex:
            log.error("API Fortress: Không tìm thấy Cortex.")
            error_response = { "id": f"err-{uuid.uuid4()}", "text": "Lỗi Hệ thống: Cortex chưa sẵn sàng.", "type": "system", "timestamp": datetime.now().isoformat() }
            return {"message": error_response}

        user_message_text = event_data.get('message')
        response_message = await cortex.process_user_message(user_message_text)
        return {"message": response_message}

    except Exception as e:
        log.error(f"API Fortress Error: {e}", exc_info=True)
        error_response = { "id": f"err-{uuid.uuid4()}", "text": f"Lỗi nghiêm trọng từ Não bộ: {e}", "type": "system", "timestamp": datetime.now().isoformat() }
        return {"message": error_response}