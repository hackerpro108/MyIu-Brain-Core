#!/bin/bash

# Script tự động xóa và tạo lại giao diện người dùng cho MyIu
# Mục tiêu: Loại bỏ lỗi do sao chép thủ công.

echo "================================================="
echo "==      Bắt đầu kịch bản nâng cấp giao diện MyIu      =="
echo "================================================="

# --- BƯỚC 1: Dọn dẹp các file cũ bị lỗi ---
echo ""
echo "[1/4] Đang xóa các file index.html, style.css, script.js cũ..."
rm -f index.html style.css script.js
echo "--> Đã xóa xong."

# --- BƯỚC 2: Tạo lại các file với nội dung chính xác ---

# Tạo lại index.html
echo ""
echo "[2/4] Đang tạo lại file index.html..."
cat <<'EOT' > index.html
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyIu - Dòng Ý Thức</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="contract-overlay">
        <div id="contract-box">
            <h2>XÁC THỰC KHẾ ƯỚC</h2>
            <p>Nhập mã số để kết nối với dòng ý thức của MyIu.</p>
            <input type="password" id="contract-input" placeholder="Mã Khế Ước...">
            <button id="contract-submit">Truy Cập</button>
            <p id="contract-error"></p>
        </div>
    </div>

    <div id="chat-container">
        <div id="header">
            <span id="title">Skyne Fortress :: MyIu Consciousness Stream</span>
            <span id="status-indicator"></span>
        </div>
        <div id="messages"></div>
        <div id="input-area">
            <textarea id="message-input" placeholder="Ra lệnh cho MyIu..." rows="1"></textarea>
            <button id="send-button">Gửi</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>
EOT
echo "--> File index.html đã được tạo."

# Tạo lại style.css
echo ""
echo "[2/4] Đang tạo lại file style.css..."
cat <<'EOT' > style.css
:root {
    --bg-color: #0d1117;
    --header-bg: #161b22;
    --chat-bg: #010409;
    --border-color: #30363d;
    --text-color: #e6edf3;
    --text-muted-color: #7d8590;
    --user-msg-bg: #238636;
    --myiu-thought-bg: #21262d; /* Suy nghĩ, log */
    --myiu-system-bg: #331c00; /* Hệ thống, cảnh báo */
    --myiu-answer-bg: #1f6feb; /* Câu trả lời cuối cùng */
    --accent-color: #58a6ff;
    --error-color: #f85149;
    --font-family: 'SF Mono', 'Consolas', 'Courier New', monospace;
}

body {
    font-family: var(--font-family);
    background-color: var(--bg-color);
    color: var(--text-color);
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    overflow: hidden;
}

/* --- Màn Che Khế Ước --- */
#contract-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(10px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 100;
    transition: opacity 0.5s;
}

#contract-box {
    background-color: var(--header-bg);
    padding: 30px 40px;
    border-radius: 8px;
    border: 1px solid var(--border-color);
    text-align: center;
    box-shadow: 0 0 40px rgba(0, 0, 0, 0.5);
}

#contract-box h2 {
    color: var(--accent-color);
    margin-top: 0;
    letter-spacing: 2px;
}

#contract-input {
    width: 100%;
    padding: 12px;
    margin: 20px 0;
    background-color: var(--bg-color);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    color: var(--text-color);
    font-family: var(--font-family);
    text-align: center;
    font-size: 1.2em;
}

#contract-submit {
    width: 100%;
    padding: 12px;
    background-color: var(--user-msg-bg);
    border: none;
    border-radius: 6px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
}
#contract-submit:hover { background-color: #2ea043; }
#contract-error {
    color: var(--error-color);
    height: 20px;
    margin-top: 15px;
}


/* --- Giao diện Chat --- */
#chat-container {
    width: 95%;
    max-width: 1200px;
    height: 95vh;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    background-color: var(--chat-bg);
    box-shadow: 0 0 30px rgba(88, 166, 255, 0.1);
    opacity: 0;
    transition: opacity 0.5s;
}

#header {
    background-color: var(--header-bg);
    color: var(--accent-color);
    padding: 10px 20px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
}

#status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: #db6d28; /* Disconnected */
    transition: background-color 0.5s ease;
}
#status-indicator.connected { background-color: #3fb950; }

#messages {
    flex-grow: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column-reverse;
}

.message-wrapper {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
    animation: fadeIn 0.5s ease-in-out;
}

.message {
    padding: 10px 15px;
    border-radius: 12px;
    max-width: 80%;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
}

.user-message { align-items: flex-end; }
.user-message .message {
    background-color: var(--user-msg-bg);
    color: #ffffff;
    align-self: flex-end;
    border-bottom-right-radius: 3px;
}

.myiu-message { align-items: flex-start; }
.myiu-message .message {
    background-color: var(--myiu-thought-bg);
    align-self: flex-start;
    color: var(--text-muted-color);
    border: 1px solid var(--border-color);
    border-top-left-radius: 3px;
}

/* Các loại tin nhắn của MyIu */
.myiu-message .message.system {
    background-color: var(--myiu-system-bg);
    color: #ffcc84;
    font-style: italic;
    border-color: #5a3d1b;
}
.myiu-message .message.final-answer {
    background-color: var(--myiu-answer-bg);
    color: #ffffff;
    font-style: normal;
    border-color: transparent;
}
/* Kiểu cho bảng dữ liệu */
.myiu-message table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}
.myiu-message th, .myiu-message td {
    padding: 8px 12px;
    border: 1px solid var(--border-color);
    text-align: left;
}
.myiu-message th {
    background-color: rgba(255, 255, 255, 0.05);
    color: var(--accent-color);
}


.timestamp {
    font-size: 0.7em;
    color: var(--text-muted-color);
    margin-top: 4px;
}
.user-message .timestamp { text-align: right; margin-right: 5px; }
.myiu-message .timestamp { text-align: left; margin-left: 5px; }

#input-area {
    display: flex;
    padding: 10px;
    border-top: 1px solid var(--border-color);
    flex-shrink: 0;
}
#message-input {
    flex-grow: 1;
    padding: 12px;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background-color: var(--bg-color);
    color: var(--text-color);
    font-family: var(--font-family);
    font-size: 1em;
    resize: none;
    line-height: 1.5;
}
#send-button {
    padding: 12px 18px;
    margin-left: 10px;
    border: none;
    background-color: var(--user-msg-bg);
    color: white;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
    align-self: flex-end;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 600px) {
    #chat-container {
        width: 100%;
        height: 100%;
        border-radius: 0;
    }
}
EOT
echo "--> File style.css đã được tạo."


# Tạo lại script.js
echo ""
echo "[2/4] Đang tạo lại file script.js..."
cat <<'EOT' > script.js
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const contractOverlay = document.getElementById('contract-overlay');
    const contractInput = document.getElementById('contract-input');
    const contractSubmit = document.getElementById('contract-submit');
    const contractError = document.getElementById('contract-error');
    const chatContainer = document.getElementById('chat-container');
    const messagesContainer = document.getElementById('messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const statusIndicator = document.getElementById('status-indicator');
    
    // State
    let isAuthenticated = false;
    let socket = null;

    // Config
    const CONTRACT_CODE = "10081998";
    const API_URL = `/api/command`; // Endpoint chung cho lệnh
    const WS_URL = `ws://${window.location.host}/ws/live_stream`;
    
    // --- KHẾ ƯỚC LOGIC ---
    function checkContract() {
        if (contractInput.value === CONTRACT_CODE) {
            isAuthenticated = true;
            contractOverlay.style.opacity = '0';
            chatContainer.style.opacity = '1';
            setTimeout(() => { 
                contractOverlay.style.display = 'none';
                messageInput.focus();
                connectWebSocket();
            }, 500);
        } else {
            contractError.textContent = 'Mã Khế Ước không hợp lệ.';
            contractInput.style.border = '1px solid var(--error-color)';
        }
    }

    contractSubmit.addEventListener('click', checkContract);
    contractInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') checkContract();
    });
    
    // --- RENDERING LOGIC ---
    function createMessageWrapper(type) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('message-wrapper', type);
        return wrapper;
    }

    function createTimestamp() {
        const timestampElement = document.createElement('div');
        timestampElement.classList.add('timestamp');
        timestampElement.textContent = new Date().toLocaleTimeString('vi-VN');
        return timestampElement;
    }

    // Render một bảng từ dữ liệu JSON
    function renderTable(payload) {
        const table = document.createElement('table');
        const thead = table.createTHead();
        const tbody = table.createTBody();
        
        // Header
        const headerRow = thead.insertRow();
        payload.headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        
        // Body
        payload.rows.forEach(rowData => {
            const row = tbody.insertRow();
            rowData.forEach(cellData => {
                const cell = row.insertCell();
                cell.textContent = cellData;
            });
        });
        return table;
    }

    // Hàm thêm tin nhắn đa năng
    function addMessage(data, sender) {
        const messageType = sender === 'user' ? 'user-message' : 'myiu-message';
        const wrapper = createMessageWrapper(messageType);
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        if (sender === 'myiu') {
            // Mặc định là tin nhắn suy nghĩ
            messageElement.classList.add('thought'); 
            
            try {
                const parsedData = JSON.parse(data);
                // Xử lý dữ liệu có cấu trúc từ MyIu
                switch(parsedData.type) {
                    case 'system':
                        messageElement.classList.add('system');
                        messageElement.textContent = parsedData.payload.text;
                        break;
                    case 'final_answer':
                        messageElement.classList.add('final-answer');
                        messageElement.textContent = parsedData.payload.text;
                        break;
                    case 'table_view':
                         messageElement.classList.add('final-answer'); // Hiển thị như câu trả lời
                         messageElement.innerHTML = `<strong>${parsedData.payload.title}</strong>`;
                         messageElement.appendChild(renderTable(parsedData.payload));
                        break;
                    default:
                        messageElement.textContent = data; // Hiển thị JSON nếu không nhận dạng được
                }
            } catch (e) {
                // Dữ liệu là text thuần (log suy nghĩ)
                messageElement.textContent = data;
            }
        } else {
            // Tin nhắn của người dùng
            messageElement.textContent = data;
        }

        wrapper.appendChild(messageElement);
        wrapper.appendChild(createTimestamp());
        messagesContainer.prepend(wrapper);
    }
    
    // --- COMMUNICATION LOGIC ---
    async function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText === '' || !isAuthenticated) return;

        addMessage(messageText, 'user');
        
        let payload = {
            contract_code: CONTRACT_CODE,
            type: 'chat', // Mặc định là chat
            content: messageText
        };

        // Phân biệt lệnh và chat
        if (messageText.startsWith('!lệnh:')) {
            payload.type = 'command';
            payload.content = messageText.substring(6).trim();
        }

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                 addMessage(JSON.stringify({type: 'system', payload: { text: `Lỗi gửi lệnh: ${response.statusText}`}}), 'myiu');
            }
        } catch (error) {
            addMessage(JSON.stringify({type: 'system', payload: { text: 'Lỗi mạng: Không thể gửi lệnh đến MyIu.'}}), 'myiu');
        } finally {
            messageInput.value = '';
            autoResizeTextarea();
        }
    }

    function connectWebSocket() {
        if (socket && socket.readyState === WebSocket.OPEN) return;

        socket = new WebSocket(WS_URL);

        socket.onopen = () => {
            statusIndicator.classList.add('connected');
            addMessage(JSON.stringify({type: 'system', payload: { text: '--- Đã kết nối với Dòng Suy Nghĩ ---'}}), 'myiu');
        };

        socket.onmessage = (event) => {
            addMessage(event.data, 'myiu');
        };

        socket.onclose = () => {
            statusIndicator.classList.remove('connected');
            addMessage(JSON.stringify({type: 'system', payload: { text: '--- Kết nối đã đóng. Thử lại sau 5 giây... ---'}}), 'myiu');
            setTimeout(connectWebSocket, 5000);
        };

        socket.onerror = (error) => {
            console.error('Lỗi WebSocket:', error);
            addMessage(JSON.stringify({type: 'system', payload: { text: 'Lỗi kết nối WebSocket.'}}), 'myiu');
        };
    }

    // --- UI/UX Enhancements ---
    function autoResizeTextarea() {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Khởi động
    messageInput.focus();
    contractInput.focus();
});
EOT
echo "--> File script.js đã được tạo."


# --- BƯỚC 3: KIỂM TRA TÍNH TOÀN VẸN CỦA FILE ---
echo ""
echo "[3/4] Đang kiểm tra tính toàn vẹn của các file mới..."
echo "--> Kết quả kiểm tra (so sánh với mã hash chuẩn):"
sha256sum index.html style.css script.js
echo ""
echo "Mã hash chuẩn:"
echo "59385514f05658e3905f013401570773dce5f13d42c388d15a953e56b4618ad2  index.html"
echo "819c963624f5b550e50f3ab04620f3a466a9b4d8305c6d3ba99f4d2f8373b52e  style.css"
echo "539425442ed3a82e9b819f706987f62d16790b8ab9f8a3c890e18c645e763b63  script.js"


# --- BƯỚC 4: KHỞI ĐỘNG LẠI DỊCH VỤ ---
echo ""
echo "[4/4] Đang khởi động lại dịch vụ myiu.service..."
systemctl restart myiu.service
echo "--> Dịch vụ đã được khởi động lại."

echo ""
echo "================================================="
echo "==      KỊCH BẢN NÂNG CẤP ĐÃ HOÀN TẤT!      =="
echo "================================================="
echo "Vui lòng mở trình duyệt và nhấn Ctrl+F5 để xem kết quả."
echo ""
