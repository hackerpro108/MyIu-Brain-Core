document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const statusIndicator = document.getElementById('status-indicator');

    const hostname = window.location.hostname;
    const port = window.location.port || (window.location.protocol === 'https' ? '443' : '80');
    const API_URL = `http://${hostname}:${port}/ipc/message`;
    const WS_URL = `ws://${hostname}:${port}/ws/live_stream`;

    function addMessage(text, type) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('message-wrapper', type);

        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        
        // Phân loại tin nhắn của MyIu
        if (type === 'myiu-message') {
            if (text.startsWith('PHẢN HỒI CUỐI CÙNG:') || text.startsWith('PHẢN HỒI HOÀN CHỈNH:')) {
                messageElement.classList.add('final-answer');
            }
        }
        
        messageElement.textContent = text;
        wrapper.appendChild(messageElement);
        
        const timestampElement = document.createElement('div');
        timestampElement.classList.add('timestamp');
        timestampElement.textContent = new Date().toLocaleTimeString();
        wrapper.appendChild(timestampElement);

        messagesContainer.prepend(wrapper);
    }

    async function sendMessage() {
        const messageText = messageInput.value.trim();
        if (messageText === '') return;

        addMessage(messageText, 'user-message');
        messageInput.value = '';

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    topic: 'user_message',
                    message: { user: 'SkyNewBie', text: messageText }
                })
            });
            if (!response.ok) {
                 addMessage(`Lỗi gửi lệnh: ${response.statusText}`, 'myiu-message');
            }
        } catch (error) {
            addMessage('Lỗi mạng: Không thể gửi lệnh đến MyIu.', 'myiu-message');
        }
    }

    function connectWebSocket() {
        const socket = new WebSocket(WS_URL);

        socket.onopen = () => {
            statusIndicator.classList.add('connected');
            addMessage('--- Đã kết nối với Dòng Suy Nghĩ ---', 'myiu-message');
        };

        socket.onmessage = (event) => {
            addMessage(event.data, 'myiu-message');
        };

        socket.onclose = () => {
            statusIndicator.classList.remove('connected');
            addMessage('--- Kết nối đã đóng. Thử lại sau 5 giây... ---', 'myiu-message');
            setTimeout(connectWebSocket, 5000);
        };

        socket.onerror = (error) => {
            console.error('Lỗi WebSocket:', error);
            addMessage('Lỗi kết nối WebSocket.', 'myiu-message');
        };
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    connectWebSocket();
});
