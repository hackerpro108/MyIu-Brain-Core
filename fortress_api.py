import asyncio
import os
import subprocess
from pathlib import Path
import json

import psutil
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="MyIu Fortress API - Interactive Modules")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "fortress_ui"

if UI_DIR.exists() and (UI_DIR / "index.html").exists():
    app.mount("/frontend", StaticFiles(directory=UI_DIR, html=True), name="fortress-ui")

@app.get("/status")
async def get_status():
    cpu = psutil.cpu_percent(interval=0.1)
    modules = []
    try:
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            cmdline_list = p.info.get('cmdline') or []
            cmdline = ' '.join(cmdline_list)
            
            module_info = None
            if 'myiu-soma.service' in cmdline or ('python' in p.info['name'] and 'myiu_soma' in cmdline):
                module_info = {"name": "MyIu Core", "service_name": "myiu-soma.service"}
            elif 'myiu-fortress.service' in cmdline or ('python' in p.info['name'] and 'fortress_api' in cmdline):
                module_info = {"name": "MyIu Fortress", "service_name": "myiu-fortress.service"}
            elif 'myiu-reflection.service' in cmdline or ('python' in p.info['name'] and 'reflection_engine' in cmdline):
                module_info = {"name": "MyIu Reflection", "service_name": "myiu-reflection.service"}
            
            if module_info and not any(m['name'] == module_info['name'] for m in modules):
                module_info['pid'] = p.info['pid']
                module_info['cmdline'] = cmdline
                modules.append(module_info)
                
    except (psutil.NoSuchProcess, psutil.AccessDenied): pass
    return {"cpu": cpu, "modules": sorted(modules, key=lambda x: x['name'])}

@app.get("/module/{action}")
async def control_module(action: str, name: str):
    if action not in ["start", "stop", "restart"]:
        return {"status": "error", "message": "Lệnh không hợp lệ."}
    command = ["systemctl", action, name]
    try:
        subprocess.Popen(command)
        message = f"Đã gửi yêu cầu '{action}' tới dịch vụ '{name}'."
        return {"status": "success", "message": message}
    except Exception as e:
        return {"status": "error", "message": f"Lỗi khi thực thi: {e}"}

# ... Các hàm chat và websocket giữ nguyên như cũ ...
@app.get("/chat")
async def chat(msg: str):
    return {"status": "success", "message": f"MyIu: Đã nhận '{msg}'."}

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    log_file = "/var/log/syslog"
    proc = None
    ALERT_KEYWORDS = ["error", "failed", "traceback", "critical", "denied", "failure"]
    def categorize_log(line: str) -> str:
        lower_line = line.lower()
        if "systemd[1]:" in lower_line: return "systemd"
        if "python[" in lower_line or "python3[" in lower_line: return "app"
        if "cron[" in lower_line: return "cron"
        return "other"
    try:
        proc = await asyncio.create_subprocess_exec("tail", "-F", "-n", "100", log_file, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        while True:
            line = await proc.stdout.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            decoded_line = line.decode(errors='ignore').strip()
            log_data = {"data": decoded_line, "category": categorize_log(decoded_line)}
            if any(keyword in decoded_line.lower() for keyword in ALERT_KEYWORDS):
                log_data["type"] = "alert"
            else:
                log_data["type"] = "log"
            await websocket.send_text(json.dumps(log_data))
    except WebSocketDisconnect: pass
    finally:
        if proc and proc.returncode is None:
            proc.terminate()
            await proc.wait()
