document.addEventListener('DOMContentLoaded', () => {
    // --- Lấy các thành phần UI ---
    const avatarImage = document.getElementById('myiu-avatar'); // Sẽ dùng sau
    const statusSoma = document.querySelector('#status-panel p:nth-child(1) span:last-child');
    const statusMemory = document.querySelector('#status-panel p:nth-child(2) span:last-child');
    const statusTask = document.querySelector('#status-panel p:nth-child(3) span:last-child');

    const consoleOutput = document.getElementById('output');
    const commandInput = document.getElementById('command-input');
    const thoughtStream = document.getElementById('thoughts');
    const typingCursor = document.querySelector('.typing-cursor');

    // --- Biến trạng thái ---
    const commandHistory = [];
    let historyIndex = -1;
    let isMyIuTyping = false;
    const responseQueue = [];

    // --- WebSocket URL ---
    const WS_URL = `ws://${window.location.host}/ws/live_stream`; // Cần backend hỗ trợ endpoint này
    
    // --- CÁC HÀM CẬP NHẬT GIAO DIỆN ---

    function updateStatus(payload) {
        if (payload.soma) {
            let emoji = '😐';
            if (payload.soma === 'CALM' || payload.soma === 'IDLE') emoji = '😌';
            if (payload.soma === 'THINKING' || payload.soma === 'ANALYZING') emoji = '🤔';
            if (payload.soma === 'CONFUSED') emoji = '😟';
            if (payload.soma === 'STRESSED') emoji = '😫';
            statusSoma.textContent = `${emoji} ${payload.soma}`;
            // Trong tương lai, ta có thể thay đổi src của avatarImage tại đây
        }
        if (payload.memory_count) statusMemory.textContent = `${payload.memory_count} entries`;
        if (payload.task) statusTask.textContent = payload.task;
    }

    function addThought(source, message) {
        const now = new Date().toLocaleTimeString('vi-VN');
        const p = document.createElement('p');
        p.innerHTML = `<span class="text-pink-400">[${now} ${source}]:</span> <span class="text-gray-400">${message}</span>`;
        thoughtStream.appendChild(p);
        thoughtStream.scrollTop = thoughtStream.scrollHeight;
    }

    function processResponseQueue() {
        if (isMyIuTyping || responseQueue.length === 0) {
            return;
        }
        isMyIuTyping = true;
        typingCursor.style.display = 'inline-block';
        
        const text = responseQueue.shift();
        const p = document.createElement('p');
        p.textContent = '> ';
        consoleOutput.insertBefore(p, typingCursor.parentElement);

        let i = 0;
        const interval = setInterval(() => {
            if (i < text.length) {
                p.textContent += text.charAt(i);
                i++;
                consoleOutput.scrollTop = consoleOutput.scrollHeight;
            } else {
                clearInterval(interval);
                isMyIuTyping = false;
                // Check xem còn phản hồi nào trong hàng đợi không
                setTimeout(processResponseQueue, 200);
            }
        }, 30);
    }
    
    function addResponse(message) {
        responseQueue.push(message);
        if (!isMyIuTyping) {
            processResponseQueue();
        }
    }

    // --- XỬ LÝ LỆNH TỪ NGƯỜI DÙNG ---
    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const commandText = commandInput.value.trim();
            if (commandText === '') return;

            // Hiển thị lệnh đã gõ trong console
            const p = document.createElement('p');
            p.textContent = `$ ${commandText}`;
            consoleOutput.insertBefore(p, typingCursor.parentElement);
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
            
            // Gửi lệnh tới backend qua WebSocket
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: 'command', content: commandText }));
            } else {
                addResponse("Lỗi: Mất kết nối tới MyIu Core.");
            }

            // Lưu và reset
            if (commandText) commandHistory.unshift(commandText);
            historyIndex = -1;
            commandInput.value = '';
        } else if (e.key === 'ArrowUp') {
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                commandInput.value = commandHistory[historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            if (historyIndex > 0) {
                historyIndex--;
                commandInput.value = commandHistory[historyIndex];
            } else {
                historyIndex = -1;
                commandInput.value = '';
            }
        }
    });

    // --- KẾT NỐI WEBSOCKET ---
    function connectWebSocket() {
        const socket = new WebSocket(WS_URL);

        socket.onopen = () => {
            addThought('SYSTEM', 'Connection established. MyIu is online.');
            updateStatus({ soma: 'IDLE', task: 'Awaiting Command' });
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                switch (data.type) {
                    case 'thought':
                        addThought(data.source, data.message);
                        break;
                    case 'status':
                        updateStatus(data.payload);
                        break;
                    case 'response':
                        addResponse(data.message);
                        break;
                    default:
                        addThought('UNKNOWN', event.data);
                }
            } catch (e) {
                addThought('RAW', event.data);
            }
        };

        socket.onclose = () => {
            addThought('SYSTEM', 'Connection lost. Attempting to reconnect...');
            updateStatus({ soma: 'OFFLINE', task: 'Connection Lost' });
            setTimeout(connectWebSocket, 5000);
        };

        socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
            addThought('SYSTEM', 'An error occurred with the connection.');
        };
        
        return socket;
    }

    // --- KHỞI ĐỘNG ---
    const socket = connectWebSocket();
});
