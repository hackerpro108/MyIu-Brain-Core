#!/bin/bash
set -e

echo -e "\n\033[1;36m[🔧 FIX_UI] Đang cấu hình lại giao diện khách hàng và pháo đài...\033[0m"

cd /root/myiu-brain-core

# --- BƯỚC 1: Di chuyển giao diện Vue (nếu cần) ---
if [ -d "frontend" ]; then
    echo -e "[→] Di chuyển 'frontend/' thành 'frontend_customer/'..."
    mv -f frontend frontend_customer
fi

# --- BƯỚC 2: Tạo lại giao diện pháo đài ---
echo -e "[→] Tạo giao diện Pháo đài đơn giản tại 'fortress_ui/'..."
mkdir -p fortress_ui
cat <<EOF > fortress_ui/index.html
<!DOCTYPE html>
<html>
<head><title>MyIu Fortress</title></head>
<body style="font-family:sans-serif; text-align:center; margin-top:10%">
    <h1>🛡️ Giao diện Pháo Đài đã mount thành công!</h1>
    <p>Chào mừng bạn đến với hệ thống giám sát nội bộ MyIu.</p>
</body>
</html>
EOF

# --- BƯỚC 3: Vá fortress_api.py ---
echo -e "[→] Vá fortress_api.py..."
cat << 'EOF' > fortress_api.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import json, psutil

app = FastAPI()

# Mount thư mục giao diện pháo đài
static_path = Path(__file__).parent / "fortress_ui"
if static_path.is_dir():
    app.mount("/frontend", StaticFiles(directory=static_path, html=True), name="frontend")

@app.get("/status")
def get_status():
    processes = []
    for p in psutil.process_iter(['name', 'cmdline']):
        cmd = ' '.join(p.info.get('cmdline') or [])
        if 'main:app' in cmd: processes.append('MyIu Core (Soma)')
        elif 'foreman.py' in cmd: processes.append('Autobot Foreman')
    return {"active_modules": processes}
EOF

# --- BƯỚC 4: Vá main.py ---
echo -e "[→] Vá main.py để phục vụ Vue (frontend_customer)..."
cat << 'EOF' > main.py
import uvicorn
import asyncio
import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from bot_worker.utils import log
from soma import Soma

app = FastAPI()
soma_instance = None

@app.on_event("startup")
async def startup_event():
    global soma_instance
    log.info("Khởi tạo Lõi AI Soma...")
    soma_instance = Soma()
    asyncio.create_task(soma_instance.start())

# Mount frontend_customer (Vue)
app.mount("/assets", StaticFiles(directory="frontend_customer/assets"), name="assets")

@app.get("/{full_path:path}")
async def serve_vue_app(full_path: str):
    path = os.path.join("frontend_customer", full_path)
    if os.path.isfile(path):
        return FileResponse(path)
    return FileResponse("frontend_customer/index.html")
EOF

# --- BƯỚC 5: Khởi động lại dịch vụ ---
echo -e "[⟳] Khởi động lại dịch vụ..."
systemctl restart myiu-soma.service
systemctl restart myiu-fortress.service
sleep 3

echo -e "\n\033[1;32m✅ HOÀN TẤT! Giao diện đã được cấu hình chuẩn.\033[0m"
echo -e "🔗 Pháo Đài:  http://103.78.2.25:12440/frontend/"
echo -e "🔗 Khách Hàng: http://myiu.lohi.io.vn"
