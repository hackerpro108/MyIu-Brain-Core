#!/bin/bash

# --- Cấu hình chung ---
PROJECT_DIR="/root/myiu-brain-core"
FORTRESS_UI_DIR="${PROJECT_DIR}/fortress_ui"
SERVICE_NAME="myiu-fortress.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"
REFLECTION_SERVICE_NAME="myiu-reflection.service"
REFLECTION_SERVICE_FILE="/etc/systemd/system/${REFLECTION_SERVICE_NAME}"

LOG_FILE="${PROJECT_DIR}/deploy_log_lite_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1 # Ghi tất cả output và lỗi vào file log

echo "--- Bắt đầu triển khai MyIu Fortress (Phiên bản Gọn nhẹ & Hiệu quả, Sửa lỗi Here-Document CUỐI CÙNG) ---"
echo "Thời gian hiện tại: $(date)"
echo "Thư mục dự án: ${PROJECT_DIR}"
echo "Thư mục giao diện người dùng: ${FORTRESS_UI_DIR}"
echo "File log triển khai: ${LOG_FILE}"

# --- Hàm kiểm tra lỗi ---
check_command() {
    if [ $? -ne 0 ]; then
        echo "LỖI: Lệnh '$1' thất bại. Vui lòng kiểm tra log để biết chi tiết: ${LOG_FILE}"
        exit 1
    fi
}

# --- 1. Dừng tất cả các dịch vụ MyIu để dọn dẹp sạch sẽ ---
echo -e "\n--- 1. Dừng các dịch vụ MyIu hiện có ---"
sudo systemctl stop "${SERVICE_NAME}" &> /dev/null || true # Dừng nếu đang chạy, bỏ qua lỗi nếu không có
sudo systemctl stop "${REFLECTION_SERVICE_NAME}" &> /dev/null || true
echo "Đã gửi lệnh dừng các dịch vụ. Đang chờ 2 giây..."
sleep 2

# --- 2. Dọn dẹp thư mục giao diện người dùng cũ ---
echo -e "\n--- 2. Dọn dẹp thư mục giao diện người dùng cũ ---"
sudo rm -rf "${FORTRESS_UI_DIR}"
check_command "rm -rf ${FORTRESS_UI_DIR}"
mkdir -p "${FORTRESS_UI_DIR}"
check_command "mkdir -p ${FORTRESS_UI_DIR}"
echo "Đã xóa và tạo lại thư mục: ${FORTRESS_UI_DIR}"

# --- 3. Cập nhật các file Frontend (Nhúng trực tiếp, không tải từ ngoài) ---
echo -e "\n--- 3. Cập nhật các file Frontend ---"

# index.html (tối giản, không có Chart.js, date-fns)
echo "Đang ghi file index.html..."
sudo tee "${FORTRESS_UI_DIR}/index.html" > /dev/null << 'EOF_HTML_CONTENT'
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyIu Fortress :: Gọn nhẹ & Hiệu quả</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"/>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto Mono', monospace;
            background-color: #0D1117;
            color: #C9D1D9;
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 1.5rem;
            margin: 0;
            overflow: hidden;
            box-sizing: border-box;
        }
        .panel {
            background-color: rgba(22, 27, 34, 0.7);
            border: 1px solid rgba(139, 148, 158, 0.2);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px); /* Cho Safari */
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .panel-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: #38BDF8;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid rgba(139, 148, 158, 0.2);
            margin-bottom: 1rem;
        }
        .chat-log, .live-console {
            flex-grow: 1;
            overflow-y: auto;
            font-size: 0.875rem;
            line-height: 1.5;
            padding-right: 5px; /* Cho thanh cuộn tùy chỉnh */
        }
        .input-field {
            width: 100%;
            background-color: rgba(13, 17, 23, 0.8);
            border: 1px solid rgba(139, 148, 158, 0.2);
            color: #C9D1D9;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            font-family: 'Roboto Mono', monospace;
            font-size: 0.875rem;
            outline: none;
        }
        .input-field:focus {
            border-color: #38BDF8;
            box-shadow: 0 0 8px rgba(56, 189, 248, 0.3);
        }
        .log-entry.info { color: #63B2F5; }
        .log-entry.warn { color: #FBBF24; }
        .log-entry.error, .log-entry.alert { color: #F87171; font-weight: bold; }
        .log-entry.debug { color: #8B949E; font-style: italic; }
        .log-entry span:first-child { color: #8B949E; margin-right: 0.5rem; } /* Timestamp */
        
        /* Module styles */
        .module-card {
            background-color: rgba(30, 41, 59, 0.5);
            border: 1px solid rgba(139, 148, 158, 0.2);
            border-radius: 8px;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
        }
        .module-name {
            font-weight: bold;
            color: #38BDF8;
            display: flex;
            align-items: center;
        }
        .module-status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 0.5rem;
            display: inline-block;
        }
        .status-running { background-color: #34D399; }
        .status-stopped { background-color: #8B949E; }
        .status-failed { background-color: #F87171; }
        .status-starting { background-color: #FBBF24; animation: pulse-yellow 1s infinite alternate; }

        @keyframes pulse-yellow {
            0% { opacity: 0.7; }
            100% { opacity: 1; transform: scale(1.1); }
        }

        /* Basic layout */
        main {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            flex-grow: 1;
            min-height: 0; /* Cho phép flex-grow hoạt động */
            margin-top: 1.5rem;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 1rem;
            border-bottom: 1px solid rgba(139, 148, 158, 0.2);
        }
        h1 {
            font-size: 2rem;
            color: #38BDF8;
            letter-spacing: 0.05em;
        }
        .fas { margin-right: 0.5rem; }
        .fa-spin { animation: fa-spin 2s infinite linear; }
        @keyframes fa-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        /* Custom Scrollbar */
        .chat-log::-webkit-scrollbar, .live-console::-webkit-scrollbar, #modules-container::-webkit-scrollbar {
            width: 6px;
        }
        .chat-log::-webkit-scrollbar-track, .live-console::-webkit-scrollbar-track, #modules-container::-webkit-scrollbar-track {
            background: transparent;
        }
        .chat-log::-webkit-scrollbar-thumb, .live-console::-webkit-scrollbar-thumb, #modules-container::-webkit-scrollbar-thumb {
            background-color: rgba(139, 148, 158, 0.3);
            border-radius: 3px;
        }
        .chat-log::-webkit-scrollbar-thumb:hover, .live-console::-webkit-scrollbar-thumb:hover, #modules-container::-webkit-scrollbar-thumb:hover {
            background-color: rgba(139, 148, 158, 0.5);
        }
        .hidden { display: none !important; } /* Cho filter logs */
    </style>
</head>
<body>
    <header>
        <h1><i class="fas fa-atom fa-spin"></i> MyIu Fortress</h1>
    </header>
    <main>
        <section class="panel">
            <h2 class="panel-title"><i class="fas fa-terminal"></i>Command Stream</h2>
            <div id="chat-log" class="chat-log"></div>
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                <input type="text" id="command-input" placeholder="Nhập lệnh...">
                <button id="send-command-btn" style="background-color: #38BDF8; color: black; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer;">Gửi</button>
            </div>
        </section>

        <section class="panel">
            <h2 class="panel-title"><i class="fas fa-microchip"></i>Active Modules</h2>
            <div id="modules-container" style="flex-grow: 1; overflow-y: auto;">
                <p style="color: #8B949E; font-size: 0.875rem;">Đang tải...</p>
            </div>
        </section>

        <section class="panel">
            <h2 class="panel-title"><i class="fas fa-satellite-dish"></i>Live System Logs</h2>
            <div id="log-filter-buttons" style="display: flex; gap: 0.5rem; margin-bottom: 0.5rem; flex-wrap: wrap;">
                <button class="log-filter-btn active" data-filter="all" style="background-color: rgba(139, 148, 158, .1); color: #8B949E; border: 1px solid rgba(139, 148, 158, .2); padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 600; cursor: pointer;">Tất cả</button>
                <button class="log-filter-btn" data-filter="systemd" style="background-color: rgba(139, 148, 158, .1); color: #8B949E; border: 1px solid rgba(139, 148, 158, .2); padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 600; cursor: pointer;">Hệ thống</button>
                <button class="log-filter-btn" data-filter="app" style="background-color: rgba(139, 148, 158, .1); color: #8B949E; border: 1px solid rgba(139, 148, 158, .2); padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 600; cursor: pointer;">Ứng dụng</button>
                <button class="log-filter-btn" data-filter="alert" style="color: #F87171; font-weight: bold; background-color: rgba(139, 148, 158, .1); border: 1px solid rgba(139, 148, 158, .2); padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 600; cursor: pointer;">Cảnh báo</button>
                <button class="log-filter-btn" data-filter="warn" style="color: #FBBF24; background-color: rgba(139, 148, 158, .1); border: 1px solid rgba(139, 148, 158, .2); padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 600; cursor: pointer;">Cảnh báo (Log)</button>
                <button class="log-filter-btn" data-filter="info" style="color: #63B2F5; background-color: rgba(139, 148, 158, .1); border: 1px solid rgba(139, 148, 158, .2); padding: 0.25rem 0.75rem; border-radius: 6px; font-weight: 600; cursor: pointer;">Thông tin</button>
            </div>
            <div id="live-console" class="live-console"></div>
        </section>
    </main>

    <script>
        const API_BASE_URL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
        const WS_BASE_URL = `ws://${window.location.hostname}:${window.location.port}`;

        const commandInput = document.getElementById('command-input');
        const sendCommandBtn = document.getElementById('send-command-btn');
        const chatLog = document.getElementById('chat-log');
        const modulesContainer = document.getElementById('modules-container');
        const liveConsole = document.getElementById('live-console');
        const logFilterButtons = document.getElementById('log-filter-buttons');

        let currentLogFilter = 'all';

        // --- Core Functions ---

        async function updateSystemStatus() {
            try {
                const response = await fetch(`${API_BASE_URL}/status`);
                if (!response.ok) throw new Error('API request failed');
                const data = await response.json();
                updateModules(data.modules);
            } catch (error) {
                console.error('Failed to update system status:', error);
                addConsoleLog(`[LỖI] Không thể cập nhật trạng thái hệ thống: ${error.message}`, 'error', 'system');
            }
        }

        function connectToLogs() {
            const ws = new WebSocket(`${WS_BASE_URL}/ws/logs`);
            ws.onopen = () => {
                addConsoleLog('[THÔNG BÁO] Đã kết nối tới Live Log Stream.', 'info', 'system');
            };
            ws.onmessage = (event) => {
                const log = JSON.parse(event.data);
                addConsoleLog(log.data, log.type, log.category);
            };
            ws.onclose = () => {
                addConsoleLog('[CẢNH BÁO] WebSocket ngắt kết nối. Đang thử kết nối lại sau 5s...', 'warn', 'system');
                setTimeout(connectToLogs, 5000);
            };
            ws.onerror = (error) => {
                console.error('WebSocket Error:', error);
                addConsoleLog(`[LỖI] WebSocket: ${error.message || 'Lỗi không xác định'}`, 'error', 'system');
            };
        }

        async function sendCommand(message) {
            if (message.trim() === '') return;
            addChatMessage('Bạn', message);
            commandInput.value = ''; // Xóa nội dung input

            try {
                const response = await fetch(`${API_BASE_URL}/chat?msg=${encodeURIComponent(message)}`);
                const data = await response.json();
                if (data.status === 'success') {
                    addChatMessage('MyIu', data.message);
                } else {
                    addChatMessage('Fortress', data.message || 'Lỗi không xác định từ MyIu.', 'error');
                }
            } catch (error) {
                addChatMessage('Fortress', `Lỗi: Không thể kết nối tới MyIu: ${error.message}.`, 'error');
            }
        }

        function controlModule(serviceName, action) {
            addConsoleLog(`[HÀNH ĐỘNG] Gửi lệnh ${action} tới: ${serviceName}...`, 'info');
            fetch(`${API_BASE_URL}/module/${action}?name=${serviceName}`)
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        addChatMessage('Fortress', data.message);
                    } else {
                        addChatMessage('Fortress', data.message || 'Lỗi không xác định khi điều khiển module.', 'error');
                    }
                    setTimeout(updateSystemStatus, 2000); // Cập nhật trạng thái sau khi gửi lệnh
                })
                .catch(err => {
                    addChatMessage('Fortress', `Lỗi khi gửi lệnh tới ${serviceName}: ${err.message}.`, 'error');
                    addConsoleLog(`[LỖI] API Call Failed: ${err.message}`, 'error', 'system');
                });
        }

        // --- UI Update Functions ---

        function updateModules(modules) {
            modulesContainer.innerHTML = '';
            if (modules && modules.length > 0) {
                modules.forEach(module => {
                    const statusClass = {
                        'running': 'status-running',
                        'stopped': 'status-stopped',
                        'failed': 'status-failed',
                        'starting': 'status-starting'
                    }[module.status] || 'status-stopped'; // Mặc định là stopped

                    const moduleElement = document.createElement('div');
                    moduleElement.className = 'module-card';
                    moduleElement.innerHTML = `
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span class="module-name"><span class="module-status-dot ${statusClass}"></span>${module.name} (${module.status.toUpperCase()})</span>
                            <div style="display: flex; gap: 5px;">
                                <button onclick="controlModule('${module.service_name}', 'restart')" style="background-color: #d97706; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">Restart</button>
                                <button onclick="controlModule('${module.service_name}', 'stop')" style="background-color: #b91c1c; color: white; border: none; padding: 0.3rem 0.6rem; border-radius: 4px; cursor: pointer;">Stop</button>
                            </div>
                        </div>
                        <p style="font-size: 0.75rem; color: #8B949E; margin-top: 0.5rem;">PID: ${module.pid || 'N/A'}</p>
                    `;
                    modulesContainer.appendChild(moduleElement);
                });
            } else {
                modulesContainer.innerHTML = '<p style="color: #8B949E; font-size: 0.875rem;">Không tìm thấy module nào đang hoạt động.</p>';
            }
        }

        function addChatMessage(sender, message, type = 'normal') {
            const p = document.createElement('p');
            p.innerHTML = `<span style="font-weight: bold; color: ${sender === 'Bạn' ? '#38BDF8' : '#FBBF24'};">${sender}></span>: <span style="color: ${type === 'error' ? '#F87171' : '#C9D1D9'};">${message}</span>`;
            chatLog.appendChild(p);
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        function addConsoleLog(message, type = 'log', category = 'other') {
            const p = document.createElement('p');
            p.classList.add('log-entry', type);
            p.dataset.category = category;
            p.dataset.type = type; // Để dùng cho bộ lọc

            p.innerHTML = `<span style="color: #8B949E;">[${new Date().toLocaleTimeString()}]</span> ${message.replace(/</g, "&lt;").replace(/>/g, "&gt;")}`;
            
            liveConsole.appendChild(p);
            liveConsole.scrollTop = liveConsole.scrollHeight;

            applyLogFilter(); // Áp dụng bộ lọc sau khi thêm log
        }

        function applyLogFilter() {
            liveConsole.querySelectorAll('.log-entry').forEach(entry => {
                const category = entry.dataset.category;
                const type = entry.dataset.type;
                let isHidden = false;

                if (currentLogFilter === 'all') {
                    isHidden = false;
                } else if (currentLogFilter === 'alert') {
                    isHidden = (type !== 'alert');
                } else if (currentLogFilter === 'warn') {
                    isHidden = (type !== 'warn');
                } else if (currentLogFilter === 'info') {
                    isHidden = (type !== 'info');
                } else { // Filter by category
                    isHidden = (category !== currentLogFilter);
                }
                entry.classList.toggle('hidden', isHidden);
            });
        }


        // --- Event Listeners ---
        commandInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendCommand(commandInput.value);
            }
        });
        sendCommandBtn.addEventListener('click', () => {
            sendCommand(commandInput.value);
        });

        logFilterButtons.addEventListener('click', (event) => {
            const target = event.target.closest('button');
            if (!target || !target.dataset.filter) return;

            currentLogFilter = target.dataset.filter;
            logFilterButtons.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
            target.classList.add('active');
            applyLogFilter();
        });


        // --- Initialization ---
        document.addEventListener('DOMContentLoaded', () => {
            addChatMessage('Fortress', 'MyIu Cybernetic Core v1.0 - Đơn giản hóa. Đang khởi tạo...', 'info');
            updateSystemStatus();
            setInterval(updateSystemStatus, 10000); // Cập nhật trạng thái mỗi 10 giây
            connectToLogs();
        });
    </script>
EOF_JS
echo "Đã cập nhật fortress.js."

# --- 5. Cập nhật file fortress_api.py (Backend) ---
echo -e "\n--- 5. Cập nhật file fortress_api.py (Backend) ---"
sudo tee "${PROJECT_DIR}/fortress_api.py" > /dev/null << 'EOF_PYTHON_API'
import asyncio
import os
import subprocess
from pathlib import Path
import json

import psutil
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

app = FastAPI(title="MyIu Fortress API - Interactive Modules")

# Cấu hình CORS để cho phép frontend truy cập từ bất kỳ nguồn nào
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Middleware bảo mật (để giải quyết một số cảnh báo trình duyệt)
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["X-Frame-Options"] = "DENY" # Hoặc SAMEORIGIN, tùy nhu cầu
        return response

app.add_middleware(SecurityHeadersMiddleware)


# --- Cấu hình đường dẫn cho các file giao diện người dùng (frontend) ---
BASE_DIR = Path(__file__).resolve().parent

# Dựa trên phân tích trước, frontend của bạn nằm trong thư mục con 'fortress_ui'
UI_DIR = BASE_DIR / "fortress_ui" 

print(f"DEBUG: BASE_DIR is: {BASE_DIR}")
print(f"DEBUG: Attempting to serve UI from: {UI_DIR}")

# Kiểm tra sự tồn tại của thư mục UI và index.html
if UI_DIR.exists() and (UI_DIR / "index.html").exists():
    app.mount("/frontend", StaticFiles(directory=UI_DIR, html=True), name="fortress-ui")
    print(f"INFO: Frontend files will be SUCCESSFULLY served from: {UI_DIR} at /frontend/ path.")
else:
    print(f"ERROR: UI directory NOT FOUND or index.html missing at: {UI_DIR}")
    print(f"ERROR: Please ensure '{UI_DIR}' exists and contains 'index.html'. Frontend will NOT be served.")

# --- Quản lý trạng thái hệ thống và Module ---
# Định nghĩa các dịch vụ mà ứng dụng sẽ quản lý
SERVICE_MAP = {
    "myiu-soma.service": "MyIu Core",
    "myiu-fortress.service": "MyIu Fortress",
    "myiu-reflection.service": "MyIu Reflection",
}

@app.get("/status")
async def get_status():
    cpu_percent = psutil.cpu_percent(interval=0.1)
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    
    modules_info = []
    try:
        for service_file, module_name in SERVICE_MAP.items():
            status = "unknown"
            pid = None
            cmdline = None
            
            # Kiểm tra trạng thái bằng systemctl
            proc_status = await asyncio.create_subprocess_shell(
                f"systemctl is-active {service_file}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout_status, _ = await proc_status.communicate()
            service_active_status = stdout_status.decode().strip()

            if service_active_status == "active":
                status = "running"
                # Lấy PID và cmdline nếu dịch vụ chạy
                try:
                    proc_pid = await asyncio.create_subprocess_shell(
                        f"systemctl show --property MainPID --value {service_file}",
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                    stdout_pid, _ = await proc_pid.communicate()
                    main_pid_str = stdout_pid.decode().strip()
                    if main_pid_str and main_pid_str.isdigit():
                        pid = int(main_pid_str)
                        try:
                            p = psutil.Process(pid)
                            cmdline = ' '.join(p.cmdline())
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            cmdline = "Not accessible"
                except Exception as e:
                    print(f"WARNING: Could not get PID/cmdline for {service_file}: {e}")
                    cmdline = "Error retrieving details"
            elif service_active_status == "inactive":
                status = "stopped"
            elif service_active_status == "failed":
                status = "failed"
            elif service_active_status == "activating":
                status = "starting"
            else:
                status = "not_found"

            modules_info.append({
                "name": module_name,
                "service_name": service_file,
                "pid": pid,
                "cmdline": cmdline,
                "status": status
            })

    except Exception as e:
        print(f"ERROR: General error in get_status: {e}")

    modules_info = sorted(modules_info, key=lambda x: x['name'])
    
    return {"cpu": cpu_percent, "memory": memory_percent, "modules": modules_info}

@app.get("/module/{action}")
async def control_module(action: str, name: str):
    if action not in ["start", "stop", "restart"]:
        raise HTTPException(status_code=400, detail="Lệnh không hợp lệ.")
    
    if name not in SERVICE_MAP.keys():
        raise HTTPException(status_code=400, detail="Tên dịch vụ không hợp lệ.")

    command = ["systemctl", action, name]
    try:
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        message = f"Đã gửi yêu cầu '{action}' tới dịch vụ '{SERVICE_MAP.get(name, name)}'."
        return {"status": "success", "message": message}
    except Exception as e:
        print(f"ERROR: Failed to execute systemctl command: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi thực thi: {e}")

@app.get("/chat")
async def chat(msg: str):
    lower_msg = msg.lower()
    if "xin chào" in lower_msg:
        return {"status": "success", "message": "Chào bạn! MyIu sẵn sàng phục vụ."}
    elif "thời tiết" in lower_msg:
        return {"status": "success", "message": "MyIu chưa được trang bị khả năng dự báo thời tiết. Hãy hỏi điều gì đó liên quan đến hệ thống nhé!"}
    elif "bạn khỏe không" in lower_msg or "bạn sao rồi" in lower_msg:
        return {"status": "success", "message": "Tôi luôn trong trạng thái tốt nhất để phục vụ bạn. Cảm ơn vì đã hỏi!"}
    return {"status": "success", "message": f"MyIu: Đã nhận '{msg}'. Tôi đang xử lý..."}

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    
    # Ưu tiên journalctl
    log_command_journalctl = ["journalctl", "-f", "-o", "json"]
    # Fallback syslog
    log_file_syslog = "/var/log/syslog"
    log_command_tail = ["tail", "-F", "-n", "200", log_file_syslog]

    proc = None
    try:
        # Kiểm tra sự có sẵn của journalctl
        journalctl_available = False
        try:
            test_proc = await asyncio.create_subprocess_exec("journalctl", "--version", 
                                                             stdout=asyncio.subprocess.PIPE, 
                                                             stderr=asyncio.subprocess.PIPE)
            await asyncio.wait_for(test_proc.wait(), timeout=2) # Giảm timeout
            if test_proc.returncode == 0:
                journalctl_available = True
        except (FileNotFoundError, asyncio.TimeoutError, subprocess.CalledProcessError):
            pass # journalctl không có sẵn hoặc lỗi

        if journalctl_available:
            proc = await asyncio.create_subprocess_exec(*log_command_journalctl, 
                                                        stdout=asyncio.subprocess.PIPE, 
                                                        stderr=asyncio.subprocess.PIPE)
            print("INFO: Using journalctl for logs.")
        elif Path(log_file_syslog).exists():
            proc = await asyncio.create_subprocess_exec(*log_command_tail, 
                                                        stdout=asyncio.subprocess.PIPE, 
                                                        stderr=asyncio.subprocess.PIPE)
            print(f"INFO: Using tail -F on {log_file_syslog} for logs.")
        else:
            await websocket.send_text(json.dumps({"data": f"[ERROR] No log source found: {log_file_syslog} does not exist and journalctl is not available.", "type": "error", "category": "system"}))
            await websocket.close()
            return

        # Từ khóa phân loại log
        ALERT_KEYWORDS = ["error", "failed", "traceback", "critical", "denied", "failure", "fatal", "oom"]
        WARN_KEYWORDS = ["warn", "warning", "deprecated", "unreachable", "timeout"]
        INFO_KEYWORDS = ["info", "started", "starting", "success", "connection", "received", "completed"]
        DEBUG_KEYWORDS = ["debug", "verbose"]

        def categorize_log(line: str, systemd_unit: str = None) -> str:
            lower_line = line.lower()
            if systemd_unit:
                if "systemd" in systemd_unit: return "systemd"
                if "myiu" in systemd_unit: return "app"
                if "cron" in lower_line: return "cron"
                if "kernel" in systemd_unit: return "kernel"
                if "ssh" in systemd_unit: return "security"
                if "nginx" in systemd_unit or "apache" in systemd_unit: return "webserver"
                if "docker" in systemd_unit: return "container"
            
            if "systemd[" in lower_line: return "systemd"
            if "python[" in lower_line or "python3[" in lower_line: return "app"
            if "cron[" in lower_line: return "cron"
            if "kernel:" in lower_line: return "kernel"
            if "sshd[" in lower_line: return "security"
            return "other"
        
        def determine_log_type(line: str) -> str:
            lower_line = line.lower()
            if any(keyword in lower_line for keyword in ALERT_KEYWORDS): return "alert"
            if any(keyword in lower_line for keyword in WARN_KEYWORDS): return "warn"
            if any(keyword in lower_line for keyword in INFO_KEYWORDS): return "info"
            if any(keyword in lower_line for keyword in DEBUG_KEYWORDS): return "debug"
            return "log"

        while True:
            line = await proc.stdout.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
            
            decoded_line = line.decode(errors='ignore').strip()
            log_data = {}
            
            if journalctl_available:
                try:
                    parsed_log = json.loads(decoded_line)
                    message = parsed_log.get("MESSAGE", decoded_line)
                    systemd_unit = parsed_log.get("_SYSTEMD_UNIT")
                    
                    log_data = {
                        "data": message, 
                        "category": categorize_log(message, systemd_unit),
                        "type": determine_log_type(message)
                    }
                except json.JSONDecodeError:
                    log_data = { # Fallback nếu dòng không phải JSON hợp lệ (ví dụ: dòng khởi đầu của journalctl)
                        "data": decoded_line,
                        "category": "system", # Gán category mặc định
                        "type": determine_log_type(decoded_line)
                    }
            else: # Sử dụng tail -F
                log_data = {
                    "data": decoded_line, 
                    "category": categorize_log(decoded_line),
                    "type": determine_log_type(decoded_line)
                }
            
            await websocket.send_text(json.dumps(log_data))

    except WebSocketDisconnect:
        print("INFO: WebSocket client disconnected.")
    except Exception as e:
        print(f"ERROR: Error in websocket_logs: {e}")
    finally:
        if proc and proc.returncode is None:
            proc.terminate()
            await proc.wait()
        print("INFO: WebSocket handler closed.")
EOF_PYTHON_API
echo "Đã cập nhật fortress_api.py."

# --- Cập nhật file event_bus.py (quan trọng cho MyIu Reflection) ---
echo -e "\n--- Cập nhật file event_bus.py (cho MyIu Reflection) ---"
mkdir -p "${PROJECT_DIR}/myiu" # Tạo thư mục con 'myiu' nếu chưa có
sudo tee "${PROJECT_DIR}/myiu/event_bus.py" > /dev/null << 'EOF_EVENT_BUS'
import asyncio
import logging
from collections import defaultdict
from typing import Callable, Any, Dict, List

logger = logging.getLogger(__name__)

class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = defaultdict(list)
        logger.info("EventBus initialized.")

    async def start(self):
        logger.info("EventBus: Đang khởi động...")
        await asyncio.sleep(0.01)
        logger.info("EventBus: Đã khởi động thành công!")

    async def stop(self):
        logger.info("EventBus: Đang dừng...")
        await asyncio.sleep(0.01)
        logger.info("EventBus: Đã dừng thành công!")
        self._subscribers.clear()

    async def subscribe(self, event_name: str, callback: Callable):
        self._subscribers[event_name].append(callback)
        logger.debug(f"Subscribed callback to event: {event_name}")

    async def unsubscribe(self, event_name: str, callback: Callable):
        if callback in self._subscribers[event_name]:
            self._subscribers[event_name].remove(callback)
            logger.debug(f"Unsubscribed callback from event: {event_name}")

    async def publish(self, event_name: str, *args, **kwargs):
        logger.debug(f"Publishing event: {event_name} with args: {args}, kwargs: {kwargs}")
        for callback in self._subscribers[event_name]:
            try:
                asyncio.create_task(callback(*args, **kwargs))
            except Exception as e:
                logger.error(f"Error executing callback for event {event_name}: {e}", exc_info=True)
EOF_EVENT_BUS
echo "Đã cập nhật event_bus.py."

# --- Cập nhật file base_module.py (quan trọng cho MyIu Reflection nếu chưa có) ---
echo -e "\n--- Đảm bảo base_module.py tồn tại (cho MyIu Reflection) ---"
sudo tee "${PROJECT_DIR}/myiu/base_module.py" > /dev/null << 'EOF_BASE_MODULE'
import asyncio
import logging

class AsyncModule:
    """
    Lớp cơ sở cho các module bất đồng bộ, cung cấp logger và các phương thức start/stop.
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self._running = False
        self._tasks = []

    async def start(self):
        """Khởi động module."""
        if self._running:
            return
        self._running = True
        self.log.info(f"{self.__class__.__name__} started.")
        
    async def stop(self):
        """Dừng module và hủy các tác vụ."""
        if not self._running:
            return
        self._running = False
        self.log.info(f"{self.__class__.__name__} stopping...")
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True) # Chờ các task hủy
        self._tasks = []
        self.log.info(f"{self.__class__.__name__} stopped.")
EOF_BASE_MODULE
echo "Đã cập nhật base_module.py."


# --- Cập nhật file app_context.py (quan trọng cho MyIu Reflection nếu chưa có) ---
echo -e "\n--- Đảm bảo app_context.py tồn tại (cho MyIu Reflection) ---"
sudo tee "${PROJECT_DIR}/myiu/app_context.py" > /dev/null << 'EOF_APP_CONTEXT'
import logging

logger = logging.getLogger(__name__)

class AppContext:
    """
    Lớp AppContext cung cấp ngữ cảnh chung cho ứng dụng,
    có thể chứa các cấu hình, tài nguyên được chia sẻ.
    """
    def __init__(self):
        self.config = {} # Ví dụ: có thể chứa cấu hình
        logger.info("AppContext initialized.")

    async def start(self):
        """Khởi động ngữ cảnh ứng dụng (nếu cần)."""
        logger.info("AppContext started.")
        pass

    async def stop(self):
        """Dừng ngữ cảnh ứng dụng (nếu cần)."""
        logger.info("AppContext stopped.")
        pass
EOF_APP_CONTEXT
echo "Đã cập nhật app_context.py."

# --- Cập nhật file memory.py (quan trọng cho MyIu Reflection nếu chưa có) ---
echo -e "\n--- Đảm bảo memory.py tồn tại (cho MyIu Reflection) ---"
sudo tee "${PROJECT_DIR}/myiu/memory.py" > /dev/null << 'EOF_MEMORY'
import logging
from myiu.app_context import AppContext
from myiu.base_module import AsyncModule

logger = logging.getLogger(__name__)

class MemorySystem(AsyncModule):
    """
    Hệ thống bộ nhớ giả lập cho MyIu.
    """
    def __init__(self, app_context: AppContext):
        super().__init__()
        self.app_context = app_context
        self._data = {} # Bộ nhớ đơn giản
        self.log.info("MemorySystem initialized.")

    async def start(self):
        await super().start()
        self.log.info("MemorySystem: Đang tải dữ liệu...")
        await asyncio.sleep(0.02) # Giả lập tải dữ liệu
        self._data['status'] = 'ready'
        self.log.info("MemorySystem: Đã sẵn sàng.")

    async def stop(self):
        await super().stop()
        self.log.info("MemorySystem: Đang lưu dữ liệu...")
        await asyncio.sleep(0.01) # Giả lập lưu dữ liệu
        self.log.info("MemorySystem: Đã dừng.")

    def store(self, key: str, value: Any):
        self._data[key] = value
        self.log.debug(f"Stored {key}: {value}")

    def retrieve(self, key: str) -> Any:
        return self._data.get(key)
EOF_MEMORY
echo "Đã cập nhật memory.py."

# --- Cập nhật file reflection_engine.py (đảm bảo hàm main() đúng) ---
echo -e "\n--- Cập nhật file reflection_engine.py ---"
sudo tee "${PROJECT_DIR}/myiu/reflection_engine.py" > /dev/null << 'EOF_REFLECTION_ENGINE'
import asyncio
import logging
import signal
from typing import Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from myiu.base_module import AsyncModule
from myiu.event_bus import EventBus
from myiu.memory import MemorySystem
from myiu.app_context import AppContext

logger = logging.getLogger(__name__)


class ReflectionEngine(AsyncModule):
    """
    Module này cho phép MyIu thực hiện quá trình phản tư về các tương tác
    và trạng thái nội bộ của mình. Nó lắng nghe các sự kiện trên EventBus,
    phân tích chúng và tạo ra những suy ngẫm mới.
    """

    def __init__(self, event_bus: EventBus, memory_system: MemorySystem):
        super().__init__()
        self.event_bus = event_bus
        self.memory_system = memory_system
        self.reflection_queue = asyncio.Queue()
        self._is_running = False
        self._loop_task = None
        self.log.info("ReflectionEngine initialized.")

    async def _reflection_loop(self):
        self.log.info("Reflection loop started.")
        while self._is_running:
            try:
                event_data = await self.reflection_queue.get()
                self.log.info(f"Reflecting on event: {event_data}")
                self.reflection_queue.task_done()
            except asyncio.CancelledError:
                self.log.info("Reflection loop was cancelled.")
                break
            except Exception as e:
                self.log.error(f"Error during reflection process: {e}", exc_info=True)
        self.log.info("Reflection loop stopped.")

    async def on_new_thought(self, thought_data: Dict[str, Any]):
        await self.reflection_queue.put(thought_data)
        self.log.debug(f"Queued new thought for reflection: {thought_data.get('id')}")

    async def start(self):
        if self._is_running:
            return
        self._is_running = True
        await super().start()
        await self.event_bus.subscribe("new_thought", self.on_new_thought)
        self._loop_task = asyncio.create_task(self._reflection_loop())
        self.log.info("ReflectionEngine started and subscribed to events.")

    async def stop(self):
        if not self._is_running:
            return
        self._is_running = False
        await self.event_bus.unsubscribe("new_thought", self.on_new_thought)
        if self._loop_task:
            self._loop_task.cancel()
            await asyncio.sleep(0)
        await self.reflection_queue.join()
        await super().stop()
        self.log.info("ReflectionEngine unsubscribed and shutting down.")

async def main():
    """Hàm chính để thiết lập và chạy engine."""
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    app_context = AppContext()
    event_bus = EventBus()
    memory_system = MemorySystem(app_context=app_context)
    engine = ReflectionEngine(event_bus=event_bus, memory_system=memory_system)

    try:
        if isinstance(app_context, AsyncModule):
            await app_context.start()

        await event_bus.start()
        await memory_system.start()
        await engine.start()
        logger.info("Reflection service is now running. Press Ctrl+C to stop.")
        await stop_event.wait()
    except Exception as e:
        logger.error(f"An error occurred during startup or runtime: {e}", exc_info=True)
    finally:
        logger.info("Shutting down services...")
        await engine.stop()
        await memory_system.stop()
        await event_bus.stop()
        if isinstance(app_context, AsyncModule):
            await app_context.stop()
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Service stopped by user.")
EOF_REFLECTION_ENGINE
echo "Đã cập nhật reflection_engine.py."


# --- 8. Cập nhật cấu hình dịch vụ systemd (myiu-fortress.service) ---
echo -e "\n--- 8. Cập nhật cấu hình dịch vụ systemd ---"
sudo tee "${SERVICE_FILE}" > /dev/null << 'EOF_SERVICE'
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
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF_SERVICE
echo "Đã cập nhật file dịch vụ systemd."

# --- 9. Cấu hình dịch vụ systemd cho MyIu Reflection ---
echo -e "\n--- 9. Cấu hình dịch vụ systemd cho MyIu Reflection ---"
REFLECTION_SERVICE_NAME="myiu-reflection.service"
REFLECTION_SERVICE_FILE="/etc/systemd/system/${REFLECTION_SERVICE_NAME}"

sudo tee "${REFLECTION_SERVICE_FILE}" > /dev/null << 'EOF_REFLECTION_SERVICE'
[Unit]
Description=MyIu Reflection Engine - Subconscious Process
After=network.target myiu-fortress.service # Đảm bảo chạy sau Fortress

[Service]
User=root
Group=root
WorkingDirectory=/root/myiu-brain-core
ExecStart=/root/myiu-brain-core/myiu_env/bin/python /root/myiu-brain-core/myiu/reflection_engine.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF_REFLECTION_SERVICE
echo "Đã cập nhật file dịch vụ MyIu Reflection systemd."

# --- 10. Tải lại cấu hình systemd và Khởi động/Bật dịch vụ ---
echo -e "\n--- 10. Tải lại cấu hình systemd và Khởi động/Bật dịch vụ ---"
sudo systemctl daemon-reload
check_command "systemctl daemon-reload"
echo "Đã tải lại daemon systemd."

echo "Bật và khởi động dịch vụ MyIu Fortress..."
sudo systemctl enable "${SERVICE_NAME}"
check_command "systemctl enable ${SERVICE_NAME}"
sudo systemctl start "${SERVICE_NAME}"
check_command "systemctl start ${SERVICE_NAME}"
echo "Dịch vụ MyIu Fortress đã được gửi lệnh khởi động."

echo "Bật và khởi động dịch vụ MyIu Reflection..."
sudo systemctl enable "${REFLECTION_SERVICE_NAME}"
check_command "systemctl enable ${REFLECTION_SERVICE_NAME}"
sudo systemctl start "${REFLECTION_SERVICE_NAME}"
check_command "systemctl start ${REFLECTION_SERVICE_NAME}"
echo "Dịch vụ MyIu Reflection đã được gửi lệnh khởi động."

# --- 11. Kiểm tra trạng thái cuối cùng ---
echo -e "\n--- 11. Kiểm tra trạng thái dịch vụ MyIu Fortress (sau 5 giây) ---"
sleep 5 # Chờ dịch vụ khởi động
sudo systemctl status "${SERVICE_NAME}" --no-pager
echo -e "\n--- Kiểm tra 50 dòng log cuối của MyIu Fortress ---"
sudo journalctl -u "${SERVICE_NAME}" -n 50 --no-pager

echo -e "\n--- Kiểm tra trạng thái dịch vụ MyIu Reflection (sau 5 giây) ---"
sleep 5
sudo systemctl status "${REFLECTION_SERVICE_NAME}" --no-pager
echo -e "\n--- Kiểm tra 50 dòng log cuối của MyIu Reflection ---"
sudo journalctl -u "${REFLECTION_SERVICE_NAME}" -n 50 --no-pager

echo -e "\n--- Kịch bản triển khai hoàn tất ---"
echo "Vui lòng kiểm tra giao diện người dùng bằng cách xoá cache trình duyệt và truy cập: http://103.78.2.25:12440/frontend/"
echo "Nếu vẫn có lỗi, hãy kiểm tra log chi tiết hơn bằng: journalctl -u ${SERVICE_NAME} -f"
echo "Và journalctl -u ${REFLECTION_SERVICE_NAME} -f"

# Đặt quyền sở hữu cho các file frontend (quan trọng nếu chạy user không phải root)
sudo chown -R root:root "${FORTRESS_UI_DIR}" # Hoặc user:group mà dịch vụ FastAPI chạy
sudo chmod -R 755 "${FORTRESS_UI_DIR}"
sudo chmod 644 "${FORTRESS_UI_DIR}"/*.html "${FORTRESS_UI_DIR}"/*.css "${FORTRESS_UI_DIR}"/*.js
EOF_SCRIPT
