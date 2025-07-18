#!/bin/bash

# --- Bắt đầu kịch bản triển khai MyIu Fortress ---
echo "--- Bắt đầu triển khai MyIu Fortress (Phiên bản Sửa lỗi Cuối cùng - Dùng Luxon) ---"
echo "Thời gian hiện tại: $(date)"

# --- Cấu hình đường dẫn chính ---
PROJECT_DIR="/root/myiu-brain-core"
FORTRESS_UI_DIR="${PROJECT_DIR}/fortress_ui"
JS_DIR="${FORTRESS_UI_DIR}/js"
SERVICE_NAME="myiu-fortress.service"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}"

echo "Thư mục dự án: ${PROJECT_DIR}"
echo "Thư mục giao diện người dùng: ${FORTRESS_UI_DIR}"
echo "Thư mục JS cục bộ: ${JS_DIR}"

# --- 1. Dừng dịch vụ MyIu Fortress hiện tại để tránh xung đột ---
echo -e "\n--- 1. Dừng dịch vụ ${SERVICE_NAME} hiện tại (nếu đang chạy) ---"
sudo systemctl stop "${SERVICE_NAME}"
echo "Đã gửi lệnh dừng."
sleep 2 # Chờ 2 giây để dịch vụ dừng hẳn

# --- 2. Dọn dẹp và Tạo lại thư mục JS cục bộ cho thư viện Frontend ---
echo -e "\n--- 2. Dọn dẹp và Tạo lại thư mục JS cục bộ ---"
sudo rm -rf "${JS_DIR}"
mkdir -p "${JS_DIR}"
echo "Đã xóa và tạo lại thư mục: ${JS_DIR}"

# --- 3. Tải các thư viện JavaScript cần thiết xuống máy chủ cục bộ (Chỉ tải Chart.js và Luxon) ---
echo -e "\n--- 3. Tải các thư viện JavaScript từ CDN về cục bộ (SỬ DỤNG LUXON) ---"

# Tải Chart.js (đường dẫn này đã ổn định)
echo "Đang tải chart.min.js..."
sudo wget -O "${JS_DIR}/chart.min.js" https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js
if [ $? -eq 0 ]; then echo "  chart.min.js: Tải thành công."; else echo "  chart.min.js: LỖI TẢI. Vui lòng kiểm tra kết nối mạng hoặc CDN. Thoát."; exit 1; fi

# Tải Luxon (đường dẫn này đã tải thành công trước đó)
echo "Đang tải luxon.min.js..."
sudo wget -O "${JS_DIR}/luxon.min.js" https://cdn.jsdelivr.net/npm/luxon@3.4.4/build/global/luxon.min.js
if [ $? -eq 0 ]; then echo "  luxon.min.js: Tải thành công."; else echo "  luxon.min.js: LỖI TẢI. Thoát."; exit 1; fi

# Tải chartjs-adapter-luxon (đường dẫn này đã tải thành công trước đó)
echo "Đang tải chartjs-adapter-luxon.min.js..."
sudo wget -O "${JS_DIR}/chartjs-adapter-luxon.min.js" https://cdn.jsdelivr.net/npm/chartjs-adapter-luxon@1.1.0/dist/chartjs-adapter-luxon.min.js
if [ $? -eq 0 ]; then echo "  chartjs-adapter-luxon.min.js: Tải thành công."; else echo "  chartjs-adapter-luxon.min.js: LỖI TẢI. Thoát."; exit 1; fi

echo "Đã hoàn tất tải thư viện JS (Luxon)."

# --- 4. Cập nhật các file Frontend (index.html, styles.css, fortress.js) ---
echo -e "\n--- 4. Cập nhật các file Frontend (index.html, styles.css, fortress.js) ---"

# index.html (đã thay đổi để dùng Luxon)
echo "Đang cập nhật index.html..."
sudo tee "${FORTRESS_UI_DIR}/index.html" > /dev/null << 'EOF_HTML'
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyIu Fortress :: Interactive Core</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css"/>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet"> 
    
    <script src="js/chart.min.js"></script>
    
    <script src="js/luxon.min.js"></script>
    <script src="js/chartjs-adapter-luxon.min.js"></script>
    
</head>
<body class="bg-gradient-to-br from-gray-900 to-black text-gray-300 h-screen flex flex-col p-4 sm:p-6 space-y-4 sm:space-y-6 theme-dark">
    <header class="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
        <h1 class="text-2xl sm:text-3xl font-bold text-cyan-400 tracking-wider uppercase">
            <i class="fas fa-atom fa-spin" style="--fa-animation-duration: 5s;"></i> MyIu Fortress
        </h1>
        <div class="flex items-center space-x-4">
            <span class="text-sm font-semibold text-green-400 tracking-widest">HARMONY</span>
            <div class="relative w-40 h-6 bg-black bg-opacity-50 rounded-full shadow-md overflow-hidden border border-gray-700">
                <div id="harmony-bar" class="absolute top-0 left-0 h-full rounded-full bg-gradient-to-r from-green-400 to-cyan-400 shadow-inner flex items-center justify-center text-xs font-bold text-black transition-all duration-500" style="width: 100%;">
                    <span id="harmony-score-text">100%</span>
                </div>
            </div>
            <label for="theme-selector" class="sr-only">Chọn chủ đề:</label>
            <select id="theme-selector" class="theme-selector">
                <option value="dark">Dark Theme</option>
                <option value="light">Light Theme</option>
                <option value="retro-green">Retro Green</option>
            </select>
        </div>
    </header>
    <main class="grid grid-cols-1 md:grid-cols-3 gap-6 flex-grow min-h-0">
        <section class="panel flex flex-col">
            <h2 class="panel-title"><i class="fas fa-terminal"></i>Command Stream</h2>
            <div id="chat-log" class="flex-grow overflow-y-auto mt-4 mb-4 font-mono text-sm leading-relaxed custom-scrollbar"></div>
            <div class="flex items-center space-x-2 border-t border-gray-800 pt-4">
                <label for="command-input" class="sr-only">Nhập lệnh:</label>
                <input type="text" id="command-input" class="input-field" placeholder="> Enter Command...">
                <button id="voice-command-btn" class="control-btn" title="Lệnh giọng nói (Tiếng Việt)"><i class="fas fa-microphone-alt"></i></button>
            </div>
        </section>

        <section class="panel flex flex-col">
            <h2 class="panel-title text-yellow-400"><i class="fas fa-brain"></i>AI Core Status</h2>
            <div class="flex-grow flex flex-col justify-around mt-4">
                <div class="mb-4">
                    <label class="block text-sm font-semibold text-gray-400 mb-2">CPU LOAD</label>
                    <div class="gauge-container">
                        <div class="gauge-fill"></div>
                        <div id="cpu-gauge-bar" class="gauge-bar"></div>
                        <div class="gauge-text" id="cpu-percent-text">0%</div>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="system-metrics-chart"></canvas>
                </div>
                <div class="flex-grow mt-4">
                    <h3 class="text-md text-yellow-400 font-semibold mb-2 border-b border-gray-800 pb-2 flex items-center"><i class="fas fa-microchip mr-2"></i>Active Modules</h3>
                    <div id="modules-container" class="space-y-3 pt-2 overflow-y-auto custom-scrollbar"></div>
                </div>
            </div>
        </section>

        <section class="panel flex flex-col font-mono text-sm">
            <div class="flex justify-between items-center">
                <h2 class="panel-title text-red-500 flex items-center">
                    <span id="log-status-indicator" class="mr-3 w-3 h-3 rounded-full bg-gray-50"></span>
                    <i class="fas fa-satellite-dish"></i>Live System Logs
                </h2>
            </div>
            <div id="log-filter-buttons" class="flex items-center space-x-2 py-2 border-b border-t border-gray-800 my-2 flex-wrap">
                <button class="log-filter-btn active" data-filter="all">Tất cả</button>
                <button class="log-filter-btn" data-filter="systemd">Hệ thống</button>
                <button class="log-filter-btn" data-filter="app">Ứng dụng</button>
                <button class="log-filter-btn" data-filter="cron">CRON</button>
                <button class="log-filter-btn" data-filter="kernel">Kernel</button>
                <button class="log-filter-btn" data-filter="security">Bảo mật</button>
                <button class="log-filter-btn alert-btn" data-filter="alert">Cảnh báo</button>
                <button class="log-filter-btn warn-btn" data-filter="warn">Cảnh báo (Log)</button>
                <button class="log-filter-btn info-btn" data-filter="info">Thông tin</button>
                <button class="log-filter-btn debug-btn" data-filter="debug">Debug</button>
            </div>
            <div id="live-console" class="flex-grow overflow-y-auto leading-relaxed custom-scrollbar"></div>
        </section>
    </main>
    <script src="fortress.js"></script>
</body>
</html>
EOF_HTML
echo "Đã cập nhật index.html."

# styles.css
echo "Đang cập nhật styles.css..."
sudo tee "${FORTRESS_UI_DIR}/styles.css" > /dev/null << 'EOF_CSS'
:root {
    /* Base Variables (Default Dark Theme) */
    --bg-primary: #0D1117;
    --panel-bg: rgba(22, 27, 34, 0.7);
    --border-color: rgba(139, 148, 158, 0.2);
    --text-primary: #C9D1D9;
    --text-secondary: #8B949E;
    --accent-cyan: #38BDF8;
    --accent-green: #34D399;
    --accent-yellow: #FBBF24;
    --accent-red: #F87171;
    --font-primary: 'Roboto Mono', monospace;

    /* Dynamic Theme Variables - Default to Dark */
    --theme-bg-gradient-from: #0D1117;
    --theme-bg-gradient-to: #000000;
    --theme-header-color: #38BDF8;
    --theme-harmony-from: #34D399;
    --theme-harmony-to: #38BDF8;
    --theme-panel-border: rgba(139, 148, 158, 0.2);
    --theme-input-border-focus: var(--accent-cyan);
    --theme-log-text-normal: #C9D1D9;
    --theme-log-text-info: #63B2F5; /* Lighter blue for info */
    --theme-log-text-warn: #FBBF24;
    --theme-log-text-error: #F87171;
    --theme-log-text-alert: #E53E3E; /* More intense red for alert */
    --theme-log-text-debug: #8B949E; /* New debug color */
}

/* Dark Theme (Default) */
.theme-dark {
    --theme-bg-gradient-from: #0D1117;
    --theme-bg-gradient-to: #000000;
    --theme-header-color: #38BDF8;
    --theme-harmony-from: #34D399;
    --theme-harmony-to: #38BDF8;
    --theme-panel-border: rgba(139, 148, 158, 0.2);
    --theme-input-border-focus: var(--accent-cyan);
    --theme-log-text-normal: #C9D1D9;
    --theme-log-text-info: #63B2F5;
    --theme-log-text-warn: #FBBF24;
    --theme-log-text-error: #F87171;
    --theme-log-text-alert: #E53E3E;
    --theme-log-text-debug: #8B949E;
}

/* Light Theme */
.theme-light {
    --bg-primary: #F0F2F5;
    --panel-bg: rgba(255, 255, 255, 0.9);
    --border-color: rgba(0, 0, 0, 0.1);
    --text-primary: #333;
    --text-secondary: #666;
    --theme-bg-gradient-from: #E0E2E5;
    --theme-bg-gradient-to: #FFFFFF;
    --theme-header-color: #007BFF;
    --theme-harmony-from: #28A745;
    --theme-harmony-to: #17A2B8;
    --theme-panel-border: rgba(0, 0, 0, 0.1);
    --theme-input-border-focus: #007BFF;
    --theme-log-text-normal: #333;
    --theme-log-text-info: #007BFF;
    --theme-log-text-warn: #FFC107;
    --theme-log-text-error: #DC3545;
    --theme-log-text-alert: #C82333;
    --theme-log-text-debug: #888;
}

/* Retro Green Theme (New) */
.theme-retro-green {
    --bg-primary: #000000;
    --panel-bg: rgba(0, 50, 0, 0.8);
    --border-color: rgba(0, 255, 0, 0.3);
    --text-primary: #00FF00;
    --text-secondary: #00AA00;
    --accent-cyan: #00FFFF;
    --accent-green: #00FF00;
    --accent-yellow: #FFFF00;
    --accent-red: #FF0000;
    --font-primary: 'VT323', monospace; 

    --theme-bg-gradient-from: #000000;
    --theme-bg-gradient-to: #001100;
    --theme-header-color: #00FF00;
    --theme-harmony-from: #00AA00;
    --theme-harmony-to: #00FF00;
    --theme-panel-border: rgba(0, 255, 0, 0.3);
    --theme-input-border-focus: #00FFFF;
    --theme-log-text-normal: #00FF00;
    --theme-log-text-info: #00FFFF;
    --theme-log-text-warn: #FFFF00;
    --theme-log-text-error: #FF0000;
    --theme-log-text-alert: #FF0000;
    --theme-log-text-debug: #008800;

    /* Add scanline effect for retro theme */
    background-image: 
        linear-gradient(rgba(0, 255, 0, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 255, 0, 0.05) 1px, transparent 1px);
    background-size: 3px 3px;
}


body {
    font-family: var(--font-primary);
    background: linear-gradient(to bottom right, var(--theme-bg-gradient-from), var(--theme-bg-gradient-to)); /* Dynamic gradient */
    color: var(--text-primary);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    transition: background-color .5s ease, color .5s ease, background-image .5s ease; /* Smooth theme transition */
}

.panel {
    background-color: var(--panel-bg);
    border: 1px solid var(--border-color);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px); /* THÊM DÒNG NÀY CHO TƯƠNG THÍCH SAFARI */
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, .37);
    transition: transform .3s ease, box-shadow .3s ease, border-color .3s ease, background-color .3s ease; /* Added background-color transition */
    position: relative;
    overflow: hidden;
}

.panel:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, .45);
    border-color: var(--accent-cyan);
}

.panel-title {
    letter-spacing: .05em;
    font-weight: 700;
    padding-bottom:.75rem;
    border-bottom:1px solid var(--border-color);
    color:var(--theme-header-color);
    display:flex;
    align-items:center;
    text-shadow:0 0 5px rgba(var(--theme-header-color-rgb,56,189,248),.5)
}

.panel-title i {
    margin-right:.5rem;
    color:var(--text-secondary)
}

.input-field {
    width:100%;
    background-color:rgba(13,17,23,.8);
    border:1px solid var(--border-color);
    color:var(--text-primary);
    padding:.75rem 1rem;
    border-radius:8px;
    font-family:var(--font-primary);
    font-size:.9rem;
    outline:none;
    transition:all .2s ease-in-out
}

.input-field:focus {
    border-color:var(--theme-input-border-focus);
    box-shadow:0 0 10px 0 rgba(56,189,248,.3)
}

.control-btn {
    padding:.75rem;
    border-radius:8px;
    background-color:rgba(13,17,23,.8);
    border:1px solid var(--border-color);
    color:var(--accent-cyan);
    font-size:1rem;
    transition:all .2s ease-in-out;
    cursor:pointer;
    display:flex;
    align-items:center;
    justify-content:center
}

.control-btn:hover {
    background-color:var(--accent-cyan);
    color:var(--bg-primary);
    transform:scale(1.05);
    box-shadow:0 0 12px rgba(56,189,248,.5);
    text-shadow:none
}

#harmony-bar {
    background-image:linear-gradient(to right,var(--theme-harmony-from),var(--theme-harmony-to))
}

.custom-scrollbar::-webkit-scrollbar {
    width:6px
}

.custom-scrollbar::-webkit-scrollbar-track {
    background:transparent
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color:rgba(139,148,158,.3);
    border-radius:3px
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color:rgba(139,148,158,.5)
}

#log-status-indicator {
    transition:all .5s ease;
    animation:pulse 1.5s infinite alternate
}

#log-status-indicator.bg-green-500 {
    background-color:var(--accent-green);
    box-shadow:0 0 8px var(--accent-green)
}

#log-status-indicator.bg-red-500 {
    background-color:var(--accent-red);
    box-shadow:0 0 8px var(--accent-red)
}

@keyframes pulse {
    0%,100% {
        opacity:1
    }

    50% {
        opacity:1
    }
}

.gauge-container {
    width:120px;
    height:120px;
    margin:1rem auto;
    position:relative;
    display:flex;
    align-items:center;
    justify-content:center
}

.gauge-fill {
    width:100%;
    height:100%;
    border-radius:50%;
    background-color:rgba(13,17,23,.5);
    border:3px solid var(--border-color);
    position:absolute
}

.gauge-bar {
    position:absolute;
    top:0;
    left:0;
    width:100%;
    height:100%;
    border-radius:50%;
    clip:rect(0,120px,120px,60px);
    transform:rotate(0deg);
    transition:transform .5s ease-in-out;
    background-image:conic-gradient(from 0deg,var(--accent-cyan),var(--accent-yellow),var(--accent-red),var(--accent-red))
}

.gauge-text {
    font-size:1.5rem;
    font-weight:700;
    z-index:1;
    color:var(--text-primary)
}

.log-filter-btn {
    padding:.25rem .75rem;
    border-radius:6px;
    font-size:.75rem;
    font-weight:600;
    font-family:var(--font-primary);
    background-color:rgba(139,148,158,.1);
    color:var(--text-secondary);
    border:1px solid var(--border-color);
    transition:all .2s ease;
    cursor:pointer
}

.log-filter-btn:hover {
    background-color:rgba(139,148,158,.2);
    color:var(--text-primary)
}

.log-filter-btn.active {
    background-color:var(--accent-cyan);
    color:var(--bg-primary);
    border-color:var(--accent-cyan);
    box-shadow:0 0 8px rgba(56,189,248,.3)
}

.log-filter-btn.alert-btn.active {
    background-color:var(--accent-red);
    border-color:var(--accent-red);
    box-shadow:0 0 8px rgba(248,113,113,.3)
}

.log-filter-btn.warn-btn.active {
    background-color:var(--accent-yellow);
    border-color:var(--accent-yellow);
    color:var(--bg-primary);
    box-shadow:0 0 8px rgba(251,191,36,.3)
}

.log-filter-btn.info-btn.active {
    background-color:var(--accent-cyan);
    border-color:var(--accent-cyan);
    color:var(--bg-primary);
    box-shadow:0 0 8px rgba(56,189,248,.3)
}

.log-filter-btn.debug-btn.active {
    background-color:#6B7280;
    border-color:#6B7280;
    color:var(--bg-primary);
    box-shadow:0 0 8px rgba(107,114,122,.3)
}

.log-entry {
    transition:all .3s ease,opacity .3s ease;
    padding:.1rem 0
}

.log-entry.hidden {
    opacity:0;
    height:0;
    padding:0;
    margin:0;
    overflow:hidden;
    border:none
}

.log-entry[data-type=log] span:last-child {
    color:var(--theme-log-text-normal)
}

.log-entry[data-type=info] span:last-child {
    color:var(--theme-log-text-info)
}

.log-entry[data-type=warn] span:last-child {
    color:var(--theme-log-text-warn)
}

.log-entry[data-type=error] span:last-child {
    color:var(--theme-log-text-error);
    font-weight:700
}

.log-entry[data-type=alert] span:last-child {
    color:var(--theme-log-text-alert);
    font-weight:700
}

.log-entry[data-type=debug] span:last-child {
    color:var(--theme-log-text-debug);
    font-style:italic
}

.module-card {
    background-color:rgba(30,41,59,.5);
    border:1px solid var(--border-color);
    border-radius:8px;
    padding:1rem;
    transition:all .3s ease,border-color .3s ease,box-shadow .3s ease,background-color .3s ease;
    position:relative
}

.module-card:hover {
    border-color:var(--accent-cyan);
    box-shadow:0 4px 16px rgba(56,189,248,.2)
}

.module-card .status-indicator {
    display:inline-block;
    width:8px;
    height:8px;
    border-radius:50%;
    margin-right:.5rem;
    animation:fadePulse 2s infinite ease-in-out
}

.module-card .status-indicator.running {
    background-color:var(--accent-green);
    box-shadow:0 0 5px var(--accent-green)
}

.module-card .status-indicator.stopped {
    background-color:var(--text-secondary)
}

.module-card .status-indicator.failed {
    background-color:var(--accent-red);
    animation:severePulse 1s infinite alternate
}

.module-card .status-indicator.starting {
    background-color:var(--accent-yellow);
    animation:spinPulse 1s infinite linear
}

.module-card .status-indicator.not_found {
    background-color:var(--text-secondary);
    opacity:.5
}

@keyframes fadePulse {
    0%,100% {
        opacity:1
    }

    50% {
        opacity:1
    }
}

@keyframes severePulse {
    0%,100% {
        transform:scale(1);
        opacity:1
    }

    50% {
        transform:scale(1.1);
        opacity:.8
    }
}

@keyframes spinPulse {
    0% {
        transform:rotate(0deg) scale(1)
    }

    50% {
        transform:rotate(180deg) scale(1.1)
    }

    100% {
        transform:rotate(360deg) scale(1)
    }
}

.module-detail {
    margin-top:.75rem;
    padding-top:.75rem;
    border-top:1px solid var(--border-color);
    font-size:.8rem;
    color:var(--text-secondary);
    word-break:break-all;
    transition:max-height .4s ease-out,opacity .4s ease-out;
    max-height:0;
    overflow:hidden;
    opacity:0
}

.module-detail.active {
    max-height:200px;
    opacity:1
}

.module-controls {
    display:flex;
    gap:.5rem;
    margin-top:1rem
}

.module-btn {
    flex-grow:1;
    padding:.5rem;
    border-radius:6px;
    font-size:.8rem;
    font-weight:600;
    border:none;
    cursor:pointer;
    transition:all .2s ease;
    display:flex;
    align-items:center;
    justify-content:center
}

.module-btn i {
    margin-right:.25rem
}

.restart-btn {
    background-color:#d97706;
    color:white
}

.restart-btn:hover {
    background-color:#f59e0b;
    transform:translateY(-2px);
    box-shadow:0 2px 8px rgba(245,158,11,.4)
}

.stop-btn {
    background-color:#b91c1c;
    color:white
}

.stop-btn:hover {
    background-color:#ef4444;
    transform:translateY(-2px);
    box-shadow:0 2px 8px rgba(239,68,68,.4)
}

.log-btn {
    background-color:#4b5563;
    color:white
}

.log-btn:hover {
    background-color:#6b7280;
    transform:translateY(-2px);
    box-shadow:0 2px 8px rgba(107,114,122,.4)
}

.chart-container {
    width:100%;
    height:150px;
    margin-top:1rem;
    background-color:rgba(13,17,23,.5);
    border-radius:8px;
    padding:10px;
    display:flex;
    justify-content:center;
    align-items:center
}

.theme-selector {
    margin-left:1rem;
    padding:.25rem .5rem;
    border-radius:6px;
    background-color:rgba(139,148,158,.1);
    color:var(--text-secondary);
    border:1px solid var(--border-color);
    cursor:pointer;
    font-family:var(--font-primary);
    font-size:.8rem;
    transition:all .2s ease,background-color .2s ease,color .2s ease
}

.theme-selector:hover {
    background-color:rgba(139,148,158,.2);
    color:var(--text-primary)
}

body.theme-light {
    background:var(--bg-primary)
}

body.theme-dark {
    background:var(--bg-primary)
}

.sr-only {
    position:absolute;
    width:1px;
    height:1px;
    padding:0;
    margin:-1px;
    overflow:hidden;
    clip:rect(0,0,0,0);
    white-space:nowrap;
    border-width:0
}
EOF_CSS
echo "Đã cập nhật styles.css."

# fortress.js
echo "Đang cập nhật fortress.js..."
sudo tee "${FORTRESS_UI_DIR}/fortress.js" > /dev/null << 'EOF_JS'
const commandInput = document.getElementById('command-input');
const chatLog = document.getElementById('chat-log');
const liveConsole = document.getElementById('live-console');
const cpuGaugeBar = document.getElementById('cpu-gauge-bar');
const cpuPercentText = document.getElementById('cpu-percent-text');
const modulesContainer = document.getElementById('modules-container');
const harmonyBar = document.getElementById('harmony-bar');
const harmonyScoreText = document.getElementById('harmony-score-text');
const voiceCommandBtn = document.getElementById('voice-command-btn');
const logStatusIndicator = document.getElementById('log-status-indicator');
const logFilterButtons = document.getElementById('log-filter-buttons');
const themeSelector = document.getElementById('theme-selector');

const API_BASE_URL = `${window.location.protocol}//${window.location.hostname}:${window.location.port}`;
const WS_BASE_URL = `ws://${window.location.hostname}:${window.location.port}`;

let harmonyScore = 100;
let currentLogFilter = 'all';

let systemMetricsChart;
const cpuData = [];
const memData = [];
const chartMaxPoints = 30;

// --- CORE LOGIC ---

async function updateSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        if (!response.ok) throw new Error('API request failed');
        const data = await response.json();
        
        updateCpuGauge(data.cpu);
        updateModules(data.modules);
        
        if (systemMetricsChart) {
            const now = new Date();
            cpuData.push({ x: now, y: data.cpu });
            memData.push({ x: now, y: data.memory });

            if (cpuData.length > chartMaxPoints) cpuData.shift();
            if (memData.length > chartMaxPoints) memData.shift();

            systemMetricsChart.update();
        }
    } catch (error) {
        console.error('Failed to update system status:', error);
        addConsoleLog('[ERROR] Failed to fetch system status. Check API connection.', 'error', 'system');
        updateHarmony(-5);
    }
}

function connectToLogs() {
    const ws = new WebSocket(`${WS_BASE_URL}/ws/logs`);
    ws.onopen = () => {
        logStatusIndicator.className = 'mr-3 w-3 h-3 rounded-full bg-green-500';
        logStatusIndicator.style.animationPlayState = 'paused';
        addConsoleLog('[INFO] Connected to Live Log Stream.', 'info', 'system');
    };
    ws.onmessage = (event) => {
        try {
            const log = JSON.parse(event.data);
            addConsoleLog(log.data, log.type, log.category);
            if (log.type === 'alert') {
                updateHarmony(-1);
            } else if (log.type === 'warn') {
                updateHarmony(-0.5);
            }
        } catch (e) {
            console.error('Error parsing log message:', e, event.data);
            addConsoleLog(`[ERROR] Malformed log entry: ${event.data.substring(0, 100)}...`, 'error', 'system');
        }
    };
    ws.onclose = (event) => {
        logStatusIndicator.className = 'mr-3 w-3 h-3 rounded-full bg-red-500';
        logStatusIndicator.style.animationPlayState = 'running';
        let reason = "unknown reason";
        if (event.code === 1000) reason = "Normal closure";
        else if (event.code === 1006) reason = "Abnormal closure (no close frame)";
        else if (event.reason) reason = event.reason;
        
        addConsoleLog(`[WARN] WebSocket disconnected (Code: ${event.code}, Reason: ${reason}). Reconnecting in 5s...`, 'warn', 'system');
        setTimeout(connectToLogs, 5000);
    };
    ws.onerror = (error) => {
        logStatusIndicator.className = 'mr-3 w-3 h-3 rounded-full bg-red-500';
        logStatusIndicator.style.animationPlayState = 'running';
        console.error('WebSocket Error:', error);
        addConsoleLog(`[ERROR] WebSocket connection error: ${error.message || "Unknown error"}`, 'error', 'system');
    };
}

async function sendCommand(message, source = 'text') {
    if (source === 'text') addChatMessage('Bạn', message);
    if (message.trim() === '') return;

    try {
        const response = await fetch(`${API_BASE_URL}/chat?msg=${encodeURIComponent(message)}`);
        const data = await response.json();
        if (data.status === 'success') {
            addChatMessage('MyIu', data.message, 'success');
            updateHarmony(1);
        } else {
            addChatMessage('Fortress', data.message || 'Unknown error from API.', 'error');
            updateHarmony(-1);
        }
    } catch (error) {
        addChatMessage('Fortress', 'Lỗi: Không thể kết nối tới MyIu.', 'error');
        updateHarmony(-2);
    }
}

function controlModule(serviceName, action) {
    addConsoleLog(`[ACTION] Gửi lệnh ${action} tới: ${serviceName}...`, 'info');
    fetch(`${API_BASE_URL}/module/${action}?name=${serviceName}`)
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                addChatMessage('Fortress', data.message, 'success');
                updateHarmony(2);
            } else {
                addChatMessage('Fortress', data.message, 'error');
                updateHarmony(-2);
            }
            setTimeout(updateSystemStatus, 3000); 
        })
        .catch(err => {
            addChatMessage('Fortress', `Lỗi khi gửi lệnh tới ${serviceName}: ${err.message}.`, 'error');
            addConsoleLog(`[ERROR] API Call Failed: ${err.message}`, 'error', 'system');
            updateHarmony(-5);
        });
}

window.toggleModuleDetails = function(pid) {
    const detailElement = document.getElementById(`detail-${pid}`);
    const iconElement = document.getElementById(`icon-${pid}`);
    if (detailElement) {
        detailElement.classList.toggle('active');
        iconElement.classList.toggle('fa-chevron-down');
        iconElement.classList.toggle('fa-chevron-up');
    }
};

window.filterLogsForModule = function(serviceName) {
    document.querySelectorAll('.log-filter-btn').forEach(btn => btn.classList.remove('active'));

    const moduleLogKeyword = serviceName.replace('.service', '').toLowerCase().split('-').pop();

    liveConsole.querySelectorAll('.log-entry').forEach(entry => {
        const logText = entry.textContent.toLowerCase();
        const isHidden = !logText.includes(serviceName.toLowerCase()) && !logText.includes(moduleLogKeyword);
        entry.classList.toggle('hidden', isHidden);
    });
    currentLogFilter = `module-${serviceName}`;
};


// --- UI UPDATE FUNCTIONS ---

function updateHarmony(change) {
    harmonyScore = Math.max(0, Math.min(100, harmonyScore + change));
    harmonyBar.style.width = `${harmonyScore}%`;
    harmonyScoreText.textContent = `${Math.round(harmonyScore)}%`;

    let startHue = (harmonyScore / 100) * 120;
    let endHue = startHue + 60;
    harmonyBar.style.backgroundImage = `linear-gradient(to right, hsl(${startHue}, 100%, 35%), hsl(${endHue}, 100%, 50%))`;

    if (Math.abs(change) > 1 && navigator.vibrate) {
        navigator.vibrate(50);
    }
}

function updateCpuGauge(cpu) {
    const cpuValue = Math.round(cpu);
    const rotation = (cpuValue / 100) * 180;
    cpuGaugeBar.style.transform = `rotate(${rotation}deg)`;
    cpuPercentText.textContent = `${cpuValue}%`;
}

function updateModules(modules) {
    modulesContainer.innerHTML = '';
    if (modules && modules.length > 0) {
        modules.forEach(module => {
            const statusClass = {
                'running': 'text-green-500',
                'stopped': 'text-gray-500',
                'failed': 'text-red-500',
                'starting': 'text-yellow-500',
                'not_found': 'text-blue-500',
                'error': 'text-red-700'
            }[module.status] || 'text-gray-400';

            const statusIcon = {
                'running': 'fa-check-circle',
                'stopped': 'fa-circle-stop',
                'failed': 'fa-triangle-exclamation',
                'starting': 'fa-spinner fa-spin',
                'not_found': 'fa-question-circle',
                'error': 'fa-times-circle'
            }[module.status] || 'fa-circle-info';

            const statusDotClass = {
                'running': 'status-indicator running',
                'stopped': 'status-indicator stopped',
                'failed': 'status-indicator failed',
                'starting': 'status-indicator starting',
                'not_found': 'status-indicator not_found',
                'error': 'status-indicator failed'
            }[module.status] || 'status-indicator';


            const moduleElement = document.createElement('div');
            moduleElement.className = 'module-card';
            moduleElement.innerHTML = `
                <div class="flex items-center justify-between cursor-pointer" onclick="toggleModuleDetails('${module.pid || module.service_name}')">
                    <span class="font-bold ${statusClass}">
                        <span class="${statusDotClass}"></span>
                        ${module.name}
                        <span class="text-xs text-gray-400 ml-2">(${module.status.toUpperCase()})</span>
                    </span>
                    <i id="icon-${module.pid || module.service_name}" class="fas fa-chevron-down text-gray-500 transition-transform"></i>
                </div>
                <div id="detail-${module.pid || module.service_name}" class="module-detail">
                    <p><strong>PID:</strong> ${module.pid || 'N/A'}</p>
                    <p><strong>Service:</strong> ${module.service_name}</p>
                    <p><strong>Command:</strong> <span class="text-xs text-gray-500">${module.cmdline || 'N/A'}</span></p>
                </div>
                <div class="module-controls">
                    <button onclick="controlModule('${module.service_name}', 'restart')" class="module-btn restart-btn"><i class="fas fa-arrows-rotate"></i>Restart</button>
                    <button onclick="controlModule('${module.service_name}', 'stop')" class="module-btn stop-btn"><i class="fas fa-stop"></i>Stop</button>
                    <button onclick="filterLogsForModule('${module.service_name}')" class="module-btn log-btn"><i class="fas fa-file-lines"></i>Logs</button>
                </div>
            `;
            modulesContainer.appendChild(moduleElement);
        });
    } else {
        modulesContainer.innerHTML = '<p class="text-sm text-gray-500">Không tìm thấy module nào đang hoạt động.</p>';
    }
}

function addChatMessage(sender, message, type = 'normal') {
    const senderClass = sender === 'Bạn' ? 'text-cyan-400' : 'text-yellow-300';
    let msgClass = 'text-gray-300';
    if (type === 'error') msgClass = 'text-red-400';
    else if (type === 'success') msgClass = 'text-green-400';
    
    chatLog.innerHTML += `<p><span class="font-bold">${sender}></span>: <span class="${msgClass}">${message}</span></p>`;
    chatLog.scrollTop = chatLog.scrollHeight;
}

function addConsoleLog(message, type = 'log', category = 'other') {
    const p = document.createElement('p');
    p.classList.add('log-entry');
    p.dataset.type = type;
    p.dataset.category = category;
    
    let typeColorVar = '--theme-log-text-normal';
    switch (type) {
        case 'info': typeColorVar = '--theme-log-text-info'; break;
        case 'warn': typeColorVar = '--theme-log-text-warn'; break;
        case 'error': typeColorVar = '--theme-log-text-error'; break;
        case 'alert': typeColorVar = '--theme-log-text-alert'; break;
        case 'debug': typeColorVar = '--theme-log-text-debug'; break;
    }
    p.style.color = `var(${typeColorVar})`;

    if ((type === 'alert' || type === 'error') && !document.hidden) {
        // new Audio('/path/to/alert.mp3').play();
    }

    p.innerHTML = `<span class="text-gray-600">[${new Date().toLocaleTimeString()}]</span> <span style="color: var(${typeColorVar});">${message.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</span>`;
    
    if (currentLogFilter !== 'all') {
        let isHidden = true;
        if (currentLogFilter.startsWith('module-')) {
            const serviceName = currentLogFilter.substring('module-'.length);
            const moduleLogKeyword = serviceName.replace('.service', '').toLowerCase().split('-').pop();
            const logText = message.toLowerCase();
            if (logText.includes(serviceName.toLowerCase()) || logText.includes(moduleLogKeyword)) {
                isHidden = false;
            }
        } else {
            if (currentLogFilter === type || currentLogFilter === category) {
                 isHidden = false;
            }
        }
        p.classList.toggle('hidden', isHidden);
    }
    
    liveConsole.appendChild(p);
    liveConsole.scrollTop = liveConsole.scrollHeight;
}

// --- INITIALIZATION ---

function initializeChartWithRetry(attempt = 0) {
    const MAX_RETRIES = 200; // Tăng số lần thử lại để chắc chắn hơn (20 giây)
    const RETRY_DELAY = 100; // 100ms

    // Kiểm tra tất cả các đối tượng toàn cục cần thiết
    // Đảm bảo window.Chart và window.dateFns (HOẶC window.luxon) tồn tại
    // Và các thành phần đăng ký của Chart.js sẵn sàng
    if (typeof window.Chart === 'undefined' || 
        (typeof window.dateFns === 'undefined' && typeof window.luxon === 'undefined') || // Kiểm tra CẢ dateFns và Luxon
        typeof Chart.registry === 'undefined' || 
        typeof Chart.scales === 'undefined' || 
        typeof Chart.scales.TimeScale === 'undefined' || // Kiểm tra TimeScale component
        typeof Chart.adapters === 'undefined' || 
        (typeof Chart.adapters.date === 'undefined' && typeof Chart.adapters.luxon === 'undefined') // Kiểm tra CẢ date adapter và luxon adapter
        ) {
        
        if (attempt < MAX_RETRIES) {
            console.warn(`[Biểu đồ] Chưa tải đủ thư viện (lần ${attempt + 1}/${MAX_RETRIES}). Thử lại sau ${RETRY_DELAY}ms...`);
            setTimeout(() => initializeChartWithRetry(attempt + 1), RETRY_DELAY);
        } else {
            console.error('[Biểu đồ] LỖI: Đã đạt số lần thử tối đa. Thư viện biểu đồ không tải được. Biểu đồ sẽ không được khởi tạo.');
            const chartContainer = document.getElementById('system-metrics-chart').parentNode;
            chartContainer.innerHTML = '<p class="text-red-500 text-center">Lỗi tải biểu đồ: Thư viện chưa sẵn sàng.</p>';
        }
        return;
    }

    // Nếu đã đến đây, các thư viện đã sẵn sàng.
    try {
        // Đăng ký các thành phần cần thiết của Chart.js v3+
        if (!Chart.registry.getScale('time')) { 
             Chart.register(Chart.scales.TimeScale);
             console.info('Chart.js TimeScale registered.');
        }
        if (!Chart.registry.getScale('linear')) { 
            Chart.register(Chart.scales.LinearScale);
            console.info('Chart.js LinearScale registered.');
        }
        if (!Chart.registry.getController('line')) { 
            Chart.register(Chart.controllers.LineController);
            console.info('Chart.js LineController registered.');
        }
        if (!Chart.registry.getElement('point')) {
            Chart.register(Chart.elements.PointElement);
            console.info('Chart.js PointElement registered.');
        }
        if (!Chart.registry.getElement('line')) {
            Chart.register(Chart.elements.LineElement);
            console.info('Chart.js LineElement registered.');
        }

        // Đăng ký bộ chuyển đổi ngày tháng (date-fns hoặc luxon)
        if (typeof window.Chart.adapters.date.dateFns !== 'undefined') {
            console.info('Sử dụng date-fns adapter.');
            // Adapter này thường tự đăng ký, không cần gọi Chart.register() lại
        } else if (typeof window.Chart.adapters.luxon !== 'undefined') {
            console.info('Sử dụng Luxon adapter.');
            // Luxon adapter cũng thường tự đăng ký, không cần gọi Chart.register() lại
        } else {
            console.error('LỖI: Không tìm thấy adapter date-fns hay Luxon nào sau khi tải thư viện.');
            const chartContainer = document.getElementById('system-metrics-chart').parentNode;
            chartContainer.innerHTML = '<p class="text-red-500 text-center">Lỗi: Không có adapter ngày tháng.</p>';
            return;
        }

    } catch (e) {
        console.error('LỖI: Ngoại lệ trong quá trình đăng ký thành phần Chart.js:', e);
        const chartContainer = document.getElementById('system-metrics-chart').parentNode;
        chartContainer.innerHTML = '<p class="text-red-500 text-center">Lỗi khởi tạo biểu đồ: Lỗi đăng ký thành phần.</p>';
        return;
    }

    const ctx = document.getElementById('system-metrics-chart').getContext('2d');
    systemMetricsChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'CPU (%)',
                data: cpuData,
                borderColor: 'var(--accent-cyan)',
                backgroundColor: 'rgba(56, 189, 248, 0.1)',
                borderWidth: 1,
                fill: true,
                tension: 0.3,
                pointRadius: 2,
                pointBackgroundColor: 'var(--accent-cyan)'
            }, {
                label: 'Memory (%)',
                data: memData,
                borderColor: 'var(--accent-red)',
                backgroundColor: 'rgba(248, 113, 113, 0.1)',
                borderWidth: 1,
                fill: true,
                tension: 0.3,
                pointRadius: 2,
                pointBackgroundColor: 'var(--accent-red)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second',
                        tooltipFormat: 'HH:mm:ss',
                        displayFormats: {
                            second: 'HH:mm:ss'
                        }
                    },
                    title: {
                        display: false,
                    },
                    grid: {
                        color: 'rgba(139, 148, 158, 0.1)'
                    },
                    ticks: {
                        color: 'var(--text-secondary)'
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Usage %',
                        color: 'var(--text-secondary)'
                    },
                    grid: {
                        color: 'rgba(139, 148, 158, 0.1)'
                    },
                    ticks: {
                        color: 'var(--text-secondary)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        color: 'var(--text-primary)'
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    backgroundColor: 'var(--panel-bg)',
                    borderColor: 'var(--border-color)',
                    borderWidth: 1,
                    titleColor: 'var(--text-primary)',
                    bodyColor: 'var(--text-primary)'
                }
            },
            animation: {
                duration: 0
            }
        }
    });
    console.info('Biểu đồ đã khởi tạo thành công!');
}


logFilterButtons.addEventListener('click', (event) => {
    const target = event.target.closest('.log-filter-btn');
    if (!target) return;

    currentLogFilter = target.dataset.filter;
    document.querySelectorAll('.log-filter-btn').forEach(btn => btn.classList.remove('active'));
    target.classList.add('active');

    liveConsole.querySelectorAll('.log-entry').forEach(entry => {
        const category = entry.dataset.category;
        const type = entry.dataset.type;

        let isHidden = true;
        if (currentLogFilter === 'all') {
            isHidden = false;
        } else if (currentLogFilter === 'alert') {
            isHidden = (type !== 'alert');
        } else if (currentLogFilter === 'warn') {
            isHidden = (type !== 'warn');
        } else if (currentLogFilter === 'info') {
            isHidden = (type !== 'info');
        } else if (currentLogFilter === 'debug') {
            isHidden = (type !== 'debug');
        } else {
            isHidden = (category !== currentLogFilter);
        }
        entry.classList.toggle('hidden', isHidden);
    });
});

commandInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendCommand(commandInput.value.trim(), 'text');
        commandInput.value = '';
    }
});

themeSelector.addEventListener('change', (event) => {
    document.body.className = '';
    document.body.classList.add('bg-gradient-to-br', 'from-gray-900', 'to-black', 'text-gray-300', 'h-screen', 'flex', 'flex-col', 'p-4', 'sm:p-6', 'space-y-4', 'sm:space-y-6');
    document.body.classList.add(`theme-${event.target.value}`);
    localStorage.setItem('myiu-fortress-theme', event.target.value);
});

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = 'vi-VN';
    recognition.continuous = false;
    recognition.interimResults = false;
    
    voiceCommandBtn.addEventListener('click', () => {
        try {
            recognition.start();
            voiceCommandBtn.classList.add('text-red-500', 'animate-pulse');
            voiceCommandBtn.title = "Listening...";
        } catch (e) {
            addConsoleLog('Voice recognition is busy or not supported.', 'warn');
        }
    });
    
    recognition.onend = () => {
        voiceCommandBtn.classList.remove('text-red-500', 'animate-pulse');
        voiceCommandBtn.title = "Voice Command (Vietnamese)";
    };
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        addChatMessage('Bạn (Giọng nói)', transcript);
        sendCommand(transcript, 'voice');
    };
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        addConsoleLog(`[ERROR] Lỗi nhận dạng giọng nói: ${event.error}`, 'error');
        voiceCommandBtn.classList.remove('text-red-500', 'animate-pulse');
        voiceCommandBtn.title = "Voice Command (Vietnamese)";
    };
} else {
    voiceCommandBtn.style.display = 'none';
    addConsoleLog('[INFO] Trình duyệt không hỗ trợ nhận dạng giọng nói.', 'info');
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('myiu-fortress-theme') || 'dark';
    document.body.classList.add(`theme-${savedTheme}`);
    themeSelector.value = savedTheme;

    initializeChartWithRetry();
    
    addChatMessage('Fortress', 'Cybernetic Core Interface v4.13 Initialized. All systems nominal.', 'success'); // Cập nhật phiên bản
    updateSystemStatus();
    setInterval(updateSystemStatus, 15000);
    connectToLogs();
});
EOF_JS
echo "Đã cập nhật fortress.js."

# --- 6. Cập nhật file event_bus.py (quan trọng cho MyIu Reflection) ---
echo -e "\n--- 6. Cập nhật file event_bus.py (cho MyIu Reflection) ---"
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

# --- 7. Cập nhật file reflection_engine.py (đảm bảo hàm main() đúng) ---
echo -e "\n--- 7. Cập nhật file reflection_engine.py ---"
sudo tee "${PROJECT_DIR}/myiu/reflection_engine.py" > /dev/null << 'EOF_REFLECTION'
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
EOF_REFLECTION
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

# --- 9. Tải lại cấu hình systemd và Khởi động dịch vụ ---
echo -e "\n--- 9. Tải lại cấu hình systemd và Khởi động dịch vụ ---"
sudo systemctl daemon-reload
echo "Đã tải lại daemon systemd."

sudo systemctl enable "${SERVICE_NAME}"
echo "Đã bật dịch vụ ${SERVICE_NAME} để tự động khởi động."

sudo systemctl start "${SERVICE_NAME}"
echo "Đã gửi lệnh khởi động dịch vụ ${SERVICE_NAME}."

# --- 10. Kiểm tra trạng thái dịch vụ ---
echo -e "\n--- 10. Kiểm tra trạng thái dịch vụ ---"
sleep 5
sudo systemctl status "${SERVICE_NAME}" --no-pager
echo -e "\n--- Kiểm tra log dịch vụ MyIu Fortress (50 dòng cuối) ---"
sudo journalctl -u "${SERVICE_NAME}" -n 50 --no-pager

echo -e "\n--- Kịch bản triển khai hoàn tất ---"
echo "Hãy kiểm tra lại giao diện người dùng bằng cách xoá cache trình duyệt và truy cập: http://103.78.2.25:12440/frontend/"
echo "Nếu vẫn có lỗi, hãy kiểm tra log chi tiết hơn bằng: journalctl -u ${SERVICE_NAME} -f"
echo "Và kiểm tra trạng thái của các dịch vụ MyIu khác nếu chúng không xuất hiện trên UI: myiu-soma.service, myiu-reflection.service"
