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
