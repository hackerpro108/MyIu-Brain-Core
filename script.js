document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const avatarImage = document.getElementById('myiu-avatar');
    const statusContent = document.getElementById('status-content');
    const statusSoma = statusContent.querySelector('p:nth-child(1) span:last-child');
    const statusMemory = statusContent.querySelector('p:nth-child(2) span:last-child');
    const statusTask = statusContent.querySelector('p:nth-child(3) span:last-child');
    const workerList = document.getElementById('worker-list');
    const consoleOutput = document.getElementById('output');
    const commandInput = document.getElementById('command-input');
    const thoughtStream = document.getElementById('thought-stream-content');
    const typingCursor = document.querySelector('.typing-cursor');

    // --- State Variables ---
    const commandHistory = []; let historyIndex = -1; let isMyIuTyping = false; const responseQueue = [];

    // --- WebSocket URL ---
    const WS_URL = ;
    
    // --- UI UPDATE FUNCTIONS ---
    function updateStatus(payload) {
        if (payload.soma) {
            let emoji = '😐'; let borderColor = 'var(--purple)';
            if (payload.soma === 'CALM' || payload.soma === 'IDLE') { emoji = '😌'; borderColor = 'var(--purple)'; }
            if (payload.soma === 'THINKING' || payload.soma === 'ANALYZING') { emoji = '🤔'; borderColor = 'var(--cyan)'; }
            if (payload.soma === 'STRESSED' || payload.soma === 'CONFUSED') { emoji = '😟'; borderColor = 'var(--magenta)'; }
            if (payload.soma === 'OFFLINE') { emoji = '🔌'; borderColor = '#6b7280';}
            statusSoma.textContent = ;
            avatarImage.style.borderColor = borderColor;
        }
        if (payload.memory_count) statusMemory.textContent = ;
        if (payload.task) statusTask.textContent = payload.task;
    }

    function updateWorkerStatus(workers) {
        workerList.innerHTML = '';
        if (!workers || workers.length === 0) {
            workerList.innerHTML = '<p class="text-gray-500">No active workers.</p>';
            return;
        }
        workers.forEach(worker => {
            let statusColor = 'var(--gray)';
            if (worker.status === 'ACTIVE' || worker.status === 'RUNNING') statusColor = 'var(--green)';
            if (worker.status === 'STALLED' || worker.status === 'ERROR') statusColor = 'var(--red)';
            
            const p = document.createElement('p');
            p.innerHTML = ;
            workerList.appendChild(p);
        });
    }

    function addThought(source, message) {
        const now = new Date().toLocaleTimeString('vi-VN');
        const p = document.createElement('p');
        const sourceSpan = document.createElement('span');
        sourceSpan.className = 'text-pink-400';
        sourceSpan.textContent = ;
        const messageSpan = document.createElement('span');
        messageSpan.className = 'text-gray-400';
        messageSpan.textContent = message;
        p.appendChild(sourceSpan); p.appendChild(messageSpan);
        thoughtStream.appendChild(p);
        thoughtStream.scrollTop = thoughtStream.scrollHeight;
    }

    function processResponseQueue() {
        if (isMyIuTyping || responseQueue.length === 0) return;
        isMyIuTyping = true;
        typingCursor.style.display = 'inline-block';
        const text = responseQueue.shift();
        const p = document.createElement('p');
        p.textContent = '> ';
        consoleOutput.insertBefore(p, typingCursor.parentElement);
        let i = 0;
        const interval = setInterval(() => {
            if (i < text.length) { p.textContent += text.charAt(i); i++; consoleOutput.scrollTop = consoleOutput.scrollHeight;
            } else { clearInterval(interval); isMyIuTyping = false; setTimeout(processResponseQueue, 200); }
        }, 30);
    }
    
    function addResponse(message) { responseQueue.push(message); if (!isMyIuTyping) { processResponseQueue(); } }

    // --- COMMAND INPUT HANDLING ---
    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const commandText = commandInput.value.trim();
            if (commandText === '') return;
            const p = document.createElement('p');
            p.innerHTML = ;
            consoleOutput.insertBefore(p, typingCursor.parentElement);
            consoleOutput.scrollTop = consoleOutput.scrollHeight;
            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: 'command', content: commandText }));
            } else { addResponse("Error: Connection to MyIu Core lost."); }
            if (commandText) commandHistory.unshift(commandText);
            historyIndex = -1; commandInput.value = '';
        } else if (e.key === 'ArrowUp') {
            e.preventDefault(); if (historyIndex < commandHistory.length - 1) { historyIndex++; commandInput.value = commandHistory[historyIndex]; }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault(); if (historyIndex > 0) { historyIndex--; commandInput.value = commandHistory[historyIndex];
            } else { historyIndex = -1; commandInput.value = ''; }
        }
    });

    // --- WEBSOCKET CONNECTION ---
    let socket;
    function connectWebSocket() {
        socket = new WebSocket(WS_URL);
        socket.onopen = () => { addThought('SYSTEM', 'Connection established. MyIu is online.'); updateStatus({ soma: 'IDLE', task: 'Awaiting Command' }); };
        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                switch (data.type) {
                    case 'thought': addThought(data.source, data.message); break;
                    case 'status': updateStatus(data.payload); break;
                    case 'response': addResponse(data.message); break;
                    case 'worker_update': updateWorkerStatus(data.payload); break;
                    default: addThought('UNKNOWN', JSON.stringify(data));
                }
            } catch (e) { addThought('RAW', event.data); }
        };
        socket.onclose = () => { addThought('SYSTEM', 'Connection lost. Reconnecting in 5s...'); updateStatus({ soma: 'OFFLINE', task: 'Connection Lost' }); setTimeout(connectWebSocket, 5000); };
        socket.onerror = (error) => { console.error("WebSocket Error:", error); addThought('SYSTEM', 'An error occurred with the connection.'); };
    }

    // --- INITIALIZE ---
    connectWebSocket();
});
