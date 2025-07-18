#!/bin/bash

# ==============================================================================
# DEPLOYMENT SCRIPT TỰ CHỨA CHO MYIU FORTRESS
# Phiên bản: Cuối cùng
# Mô tả: Script này sẽ tạo lại toàn bộ ứng dụng từ mã nguồn được nhúng sẵn,
# loại bỏ mọi phụ thuộc vào kết nối mạng bên ngoài để tải code.
# ==============================================================================

# Biến màu để output đẹp hơn
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}--- BẮT ĐẦU QUÁ TRÌNH DỌN DẸP VÀ TÁI THIẾT MYIU FORTRESS ---${NC}"

# --- 1. DỌN DẸP ---
echo -e "\n${YELLOW}[1/7] Dừng và vô hiệu hóa các dịch vụ cũ...${NC}"
sudo systemctl stop myiu-fortress.service &> /dev/null
sudo systemctl disable myiu-fortress.service &> /dev/null
sudo systemctl stop nginx &> /dev/null
sudo systemctl disable nginx &> /dev/null
echo -e "${GREEN}==> Đã dừng các dịch vụ cũ.${NC}"

# --- 2. TẠO LẠI CẤU TRÚC THƯ MỤC ---
echo -e "\n${YELLOW}[2/7] Tạo lại cấu trúc thư mục sạch...${NC}"
cd /root/myiu-brain-core
rm -rf fortress_ui
mkdir -p fortress_ui
echo -e "${GREEN}==> Đã tạo thư mục 'fortress_ui'.${NC}"

# --- 3. GHI FILE fortress_api.py ---
echo -e "\n${YELLOW}[3/7] Ghi file backend 'fortress_api.py'...${NC}"
cat > fortress_api.py << 'EOF'
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

app = FastAPI(title="MyIu Fortress API - Final Version")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
UI_DIR = BASE_DIR / "fortress_ui"

if UI_DIR.exists() and (UI_DIR / "index.html").exists():
    app.mount("/frontend", StaticFiles(directory=UI_DIR, html=True), name="fortress-ui")
    print(f"✅ [INFO] Giao diện Fortress UI đã được mount tại /frontend")
else:
    print(f"❌ [LỖI] Không tìm thấy thư mục 'fortress_ui' hoặc file 'index.html' bên trong.")

@app.get("/status")
async def get_status():
    cpu = psutil.cpu_percent(interval=0.1)
    modules = []
    try:
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            cmdline = ' '.join(p.info.get('cmdline') or [])
            if 'myiu-soma.service' in cmdline:
                if 'MyIu Core' not in modules: modules.append('MyIu Core')
            elif 'myiu-fortress.service' in cmdline:
                 if 'MyIu Fortress' not in modules: modules.append('MyIu Fortress')
    except (psutil.NoSuchProcess, psutil.AccessDenied): pass
    return {"cpu": cpu, "modules": sorted(modules)}

@app.get("/module/{action}")
async def control_module(action: str, name: str):
    service_map = {"MyIu Core": "myiu-soma.service", "MyIu Fortress": "myiu-fortress.service"}
    service_name = service_map.get(name)
    if not service_name or action not in ["start", "stop", "restart"]:
        return {"status": "error", "message": "Lệnh hoặc tên module không hợp lệ."}
    command = ["systemctl", action, service_name]
    try:
        subprocess.Popen(command)
        message = f"Đã gửi yêu cầu '{action}' tới module '{name}'."
        print(f"✅ [ACTION] {message}")
        return {"status": "success", "message": message}
    except Exception as e:
        message = f"Lỗi khi thực thi lệnh '{' '.join(command)}': {e}"
        print(f"❌ [ERROR] {message}")
        return {"status": "error", "message": message}

@app.get("/chat")
async def chat(msg: str):
    return {"status": "success", "message": f"MyIu (từ cổng 80): Đã nhận '{msg}'."}

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    log_file = "/var/log/syslog"
    proc = None
    ALERT_KEYWORDS = ["error", "failed", "traceback", "critical", "denied"]
    try:
        print(f"✅ [LOGS] Client connected. Bắt đầu stream từ {log_file}")
        proc = await asyncio.create_subprocess_exec(
            "tail", "-F", "-n", "20", log_file,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        while True:
            line = await proc.stdout.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            
            decoded_line = line.decode(errors='ignore').strip()
            log_data = {"data": decoded_line}
            if any(keyword in decoded_line.lower() for keyword in ALERT_KEYWORDS):
                log_data["type"] = "alert"
            else:
                log_data["type"] = "log"
            await websocket.send_text(json.dumps(log_data))
    except WebSocketDisconnect: print("ℹ️ [LOGS] Client disconnected.")
    except Exception as e: print(f"❌ [LOGS] WebSocket Error: {e}")
    finally:
        if proc and proc.returncode is None:
            proc.terminate()
            await proc.wait()
            print("ℹ️ [LOGS] Đã dừng tiến trình theo dõi log.")
EOF
echo -e "${GREEN}==> Đã ghi file 'fortress_api.py'.${NC}"

# --- 4. GHI CÁC FILE GIAO DIỆN ---
echo -e "\n${YELLOW}[4/7] Ghi các file giao diện (HTML, CSS, JS)...${NC}"
cat > fortress_ui/index.html << 'EOF'
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>MyIu Fortress :: Cybernetic Core</title><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"/><link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gradient-to-br from-gray-900 to-black text-gray-300 h-screen flex flex-col p-4 sm:p-6 space-y-4 sm:space-y-6">
    <header class="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0"><h1 class="text-2xl sm:text-3xl font-bold text-cyan-400 tracking-wider uppercase"><i class="fas fa-atom fa-spin" style="--fa-animation-duration: 5s;"></i> MyIu Fortress</h1><div class="flex items-center space-x-4"><span class="text-sm font-semibold text-green-400 tracking-widest">HARMONY</span><div class="relative w-40 h-6 bg-black bg-opacity-50 rounded-full shadow-md overflow-hidden border border-gray-700"><div id="harmony-bar" class="absolute top-0 left-0 h-full rounded-full bg-gradient-to-r from-green-400 to-cyan-400 shadow-inner flex items-center justify-center text-xs font-bold text-black transition-all duration-500" style="width: 100%;"><span id="harmony-score-text">100%</span></div></div></div></header>
    <main class="grid grid-cols-1 md:grid-cols-3 gap-6 flex-grow min-h-0">
        <section class="panel flex flex-col"><h2 class="panel-title"><i class="fas fa-terminal mr-2"></i>Command Stream</h2><div id="chat-log" class="flex-grow overflow-y-auto mt-4 mb-4 font-mono text-sm leading-relaxed custom-scrollbar"></div><div class="flex items-center space-x-2 border-t border-gray-800 pt-4"><input type="text" id="command-input" class="input-field" placeholder="> Enter Command..."><button id="voice-command-btn" class="control-btn"><i class="fas fa-microphone-alt"></i></button></div></section>
        <section class="panel flex flex-col"><h2 class="panel-title text-yellow-400"><i class="fas fa-brain mr-2"></i>AI Core Status</h2><div class="flex-grow flex flex-col justify-around mt-4"><div class="mb-4"><label class="block text-sm font-semibold text-gray-400 mb-2">CPU LOAD</label><div class="gauge-container"><div class="gauge-fill"></div><div id="cpu-gauge-bar" class="gauge-bar"></div><div class="gauge-text" id="cpu-percent-text">0%</div></div></div><div><h3 class="text-md text-yellow-400 font-semibold mt-4 mb-2 border-b border-gray-800 pb-2">Active Modules</h3><div id="modules-container" class="space-y-2 pt-2"></div></div></div></section>
        <section class="panel flex flex-col font-mono text-sm"><h2 class="panel-title text-red-500 flex items-center"><span id="log-status-indicator" class="mr-3 w-3 h-3 rounded-full bg-gray-500"></span><i class="fas fa-satellite-dish mr-2"></i>Live System Logs</h2><div id="live-console" class="flex-grow overflow-y-auto mt-4 leading-relaxed custom-scrollbar"></div></section>
    </main>
    <script src="fortress.js"></script>
</body>
</html>
EOF
cat > fortress_ui/styles.css << 'EOF'
:root{--bg-primary:#0D1117;--panel-bg:rgba(22, 27, 34, 0.7);--border-color:rgba(139, 148, 158, 0.2);--text-primary:#C9D1D9;--text-secondary:#8B949E;--accent-cyan:#38BDF8;--accent-green:#34D399;--accent-yellow:#FBBF24;--accent-red:#F87171;--font-primary:'Roboto Mono',monospace}body{font-family:var(--font-primary);background-color:var(--bg-primary);color:var(--text-primary);-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}.panel{background-color:var(--panel-bg);border:1px solid var(--border-color);backdrop-filter:blur(10px);border-radius:12px;padding:1.5rem;box-shadow:0 8px 32px 0 rgba(0,0,0,.37);transition:transform .3s ease,box-shadow .3s ease}.panel:hover{transform:translateY(-5px);box-shadow:0 12px 40px 0 rgba(0,0,0,.45)}.panel-title{letter-spacing:.05em;font-weight:700;padding-bottom:.75rem;border-bottom:1px solid var(--border-color)}.input-field{width:100%;background-color:rgba(13,17,23,.8);border:1px solid var(--border-color);color:var(--text-primary);padding:.75rem 1rem;border-radius:8px;font-family:var(--font-primary);font-size:.9rem;outline:none;transition:all .2s ease-in-out}.input-field:focus{border-color:var(--accent-cyan);box-shadow:0 0 10px 0 rgba(56,189,248,.3)}.control-btn{padding:.75rem;border-radius:8px;background-color:rgba(13,17,23,.8);border:1px solid var(--border-color);color:var(--accent-cyan);font-size:1rem;transition:all .2s ease-in-out}.control-btn:hover{background-color:var(--accent-cyan);color:var(--bg-primary);transform:scale(1.1)}.custom-scrollbar::-webkit-scrollbar{width:6px}.custom-scrollbar::-webkit-scrollbar-track{background:transparent}.custom-scrollbar::-webkit-scrollbar-thumb{background-color:rgba(139,148,158,.3);border-radius:3px}.custom-scrollbar::-webkit-scrollbar-thumb:hover{background-color:rgba(139,148,158,.5)}#log-status-indicator{transition:all .5s ease}#log-status-indicator.bg-green-500{background-color:var(--accent-green);box-shadow:0 0 8px var(--accent-green)}#log-status-indicator.bg-red-500{background-color:var(--accent-red);box-shadow:0 0 8px var(--accent-red)}.gauge-container{width:120px;height:120px;margin:1rem auto;position:relative;display:flex;align-items:center;justify-content:center}.gauge-fill{width:100%;height:100%;border-radius:50%;background-color:rgba(13,17,23,.5);border:3px solid var(--border-color);position:absolute}.gauge-bar{position:absolute;top:0;left:0;width:100%;height:100%;border-radius:50%;clip:rect(0,120px,120px,60px);transform:rotate(0deg);transition:transform .5s ease-in-out;background-image:conic-gradient(from 0deg,var(--accent-cyan),var(--accent-yellow),var(--accent-red),var(--accent-red))}.gauge-text{font-size:1.5rem;font-weight:700;z-index:1;color:var(--text-primary)}
EOF
cat > fortress_ui/fortress.js << 'EOF'
const commandInput=document.getElementById("command-input"),chatLog=document.getElementById("chat-log"),liveConsole=document.getElementById("live-console"),cpuGaugeBar=document.getElementById("cpu-gauge-bar"),cpuPercentText=document.getElementById("cpu-percent-text"),modulesContainer=document.getElementById("modules-container"),harmonyBar=document.getElementById("harmony-bar"),harmonyScoreText=document.getElementById("harmony-score-text"),voiceCommandBtn=document.getElementById("voice-command-btn"),logStatusIndicator=document.getElementById("log-status-indicator"),API_BASE_URL=`http://${window.location.hostname}:80`,WS_BASE_URL=`ws://${window.location.hostname}:80`;let harmonyScore=100;async function updateSystemStatus(){try{const e=await fetch(`${API_BASE_URL}/status`);if(!e.ok)throw new Error("API request failed");const o=await e.json();updateCpuGauge(o.cpu),updateModules(o.modules)}catch(e){console.error("Failed to update system status:",e),updateHarmony(-5)}}function connectToLogs(){const e=new WebSocket(`${WS_BASE_URL}/ws/logs`);e.onopen=()=>{logStatusIndicator.classList.remove("bg-gray-500","bg-red-500"),logStatusIndicator.classList.add("bg-green-500")},e.onmessage=e=>{const o=JSON.parse(e.data),t="alert"===o.type?"alert":"log";addConsoleLog(o.data,t),"alert"===t&&updateHarmony(-1)},e.onclose=()=>{logStatusIndicator.classList.remove("bg-green-500"),logStatusIndicator.classList.add("bg-red-500"),setTimeout(connectToLogs,5e3)},e.onerror=e=>{logStatusIndicator.classList.remove("bg-green-500"),logStatusIndicator.classList.add("bg-red-500")}}async function sendCommand(e,o="text"){"text"===o&&addChatMessage("Bạn",e),""!==e.trim()&&fetch(`${API_BASE_URL}/chat?msg=${encodeURIComponent(e)}`).then(e=>e.json()).then(e=>{"success"===e.status?(addChatMessage("MyIu",e.message,"success"),updateHarmony(1)):addChatMessage("Fortress",e.message,"error")}).catch(e=>{addChatMessage("Fortress","Lỗi: Không thể kết nối tới MyIu.","error"),updateHarmony(-2)})}function updateHarmony(e){harmonyScore=Math.max(0,Math.min(100,harmonyScore+change)),harmonyBar.style.width=`${harmonyScore}%`,harmonyScoreText.textContent=`${Math.round(harmonyScore)}%`;const o=1.2*harmonyScore;harmonyBar.style.backgroundImage=`linear-gradient(to right, hsl(${o}, 100%, 35%), hsl(${o}, 100%, 50%))`}function updateCpuGauge(e){const o=Math.round(e),t=o/100*180;cpuGaugeBar.style.transform=`rotate(${t}deg)`,cpuPercentText.textContent=`${o}%`}function updateModules(e){modulesContainer.innerHTML="",e.length>0?e.forEach(e=>{const o=document.createElement("div");o.innerHTML=`<p class="text-sm"><i class="fas fa-check-circle text-green-500 mr-2"></i>${e}</p>`,modulesContainer.appendChild(o)}):modulesContainer.innerHTML='<p class="text-sm text-gray-500">No active modules detected.</p>'}function addChatMessage(e,o,t="normal"){const n="Bạn"===e?"text-cyan-400":"text-yellow-300",s="error"===t?"text-red-400":"text-gray-300";chatLog.innerHTML+=`<p><span class="${n}">${e}></span> <span class="${s}">${o}</span></p>`,chatLog.scrollTop=chatLog.scrollHeight}function addConsoleLog(e,o="log"){let t="alert"===o?"text-red-400 font-bold":"text-gray-400";liveConsole.innerHTML+=`<p><span class="text-gray-600">[${(new Date).toLocaleTimeString()}]</span> <span class="${t}">${e}</span></p>`,liveConsole.scrollTop=liveConsole.scrollHeight}commandInput.addEventListener("keydown",e=>{"Enter"===e.key&&(sendCommand(commandInput.value.trim(),"text"),commandInput.value="")});const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;SpeechRecognition?(recognition=new SpeechRecognition,recognition.lang="vi-VN",voiceCommandBtn.addEventListener("click",()=>recognition.start()),recognition.onstart=()=>voiceCommandBtn.classList.add("text-red-500"),recognition.onend=()=>voiceCommandBtn.classList.remove("text-red-500"),recognition.onresult=e=>{const o=e.results[0][0].transcript;addChatMessage("Bạn (Giọng nói)",o),sendCommand(o,"voice")}):voiceCommandBtn.style.display="none",document.addEventListener("DOMContentLoaded",()=>{addChatMessage("Fortress","Cybernetic Core Interface v3.0 Initialized.","success"),updateSystemStatus(),setInterval(updateSystemStatus,1e4),connectToLogs()});
EOF
echo -e "${GREEN}==> Đã ghi 3 file giao diện.${NC}"

# --- 5. GHI FILE REQUIREMENTS.TXT VÀ CÀI ĐẶT ---
echo -e "\n${YELLOW}[5/7] Ghi file 'requirements.txt' và cài đặt thư viện...${NC}"
cat > requirements.txt << EOF
fastapi
uvicorn[standard]
psutil
EOF
source myiu_env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate
echo -e "${GREEN}==> Đã cài đặt các thư viện.${NC}"

# --- 6. GHI FILE DỊCH VỤ VÀ CẤU HÌNH SYSTEMD ---
echo -e "\n${YELLOW}[6/7] Ghi file dịch vụ 'myiu-fortress.service' và cấu hình hệ thống...${NC}"
cat > myiu-fortress.service << 'EOF'
[Unit]
Description=MyIu Fortress - Chay tren cong 80
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/root/myiu-brain-core
ExecStart=/root/myiu-brain-core/myiu_env/bin/python -m uvicorn fortress_api:app --host 0.0.0.0 --port 80
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
sudo cp myiu-fortress.service /etc/systemd/system/myiu-fortress.service
sudo systemctl daemon-reload
sudo systemctl enable myiu-fortress.service
echo -e "${GREEN}==> Đã cấu hình dịch vụ hệ thống.${NC}"

# --- 7. KHỞI ĐỘNG LẠI DỊCH VỤ ---
echo -e "\n${YELLOW}[7/7] Khởi động lại dịch vụ myiu-fortress...${NC}"
sudo systemctl restart myiu-fortress.service

echo -e "\n${GREEN}--- HOÀN TẤT! ---${NC}"
echo -e "Quá trình tái thiết đã xong. Vui lòng kiểm tra trạng thái dịch vụ bên dưới."
echo -e "Sau đó, truy cập ${YELLOW}http://103.78.2.25:12440/frontend/${NC} trên trình duyệt (dùng Hard Refresh Ctrl+Shift+R)."
echo -e "----------------------------------------------------------------"
sudo systemctl status myiu-fortress.service --no-pager
