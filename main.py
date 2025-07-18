import uvicorn
import asyncio
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from myiu.logging_config import setup_logging, get_logger
from soma import Soma
from myiu.websocket_manager import manager as websocket_manager
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

setup_logging()
log = get_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Bắt đầu vòng đời ứng dụng...")
    soma_instance = Soma()
    app.state.soma = soma_instance
    await soma_instance.start()
    log.info("Soma đã khởi động xong.")
    yield
    log.info("Bắt đầu tắt ứng dụng...")
    await app.state.soma.stop()
    log.info("Đã tắt ứng dụng xong.")

app = FastAPI(lifespan=lifespan, title="MyIu Core Brain API")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.post("/ipc/message")
async def post_ipc_message(request: Request):
    log.info("--- API: Đã nhận được một yêu cầu ---")
    try:
        event_data = await request.json()
        soma_instance = request.app.state.soma
        
        # --- NÂNG CẤP: Gọi trực tiếp Cortex ---
        cortex = soma_instance.app_context.get_service("cortex") if soma_instance else None
        
        if cortex:
            # Tạo một task để Cortex xử lý yêu cầu trong nền
            asyncio.create_task(cortex._handle_user_message(event_data.get('message')))
            log.info("API: Đã gửi lệnh trực tiếp đến Cortex thành công.")
            return {"status": "command_delegated_to_cortex"}
        
        log.error("API: Không tìm thấy Cortex để xử lý.")
        return {"status": "error", "message": "Cortex not ready"}, 503

    except Exception as e:
        log.error(f"API Error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}, 500

# Các hàm còn lại giữ nguyên
@app.websocket("/ws/live_stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

app.mount("/static", StaticFiles(directory="skyne"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('skyne/index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
