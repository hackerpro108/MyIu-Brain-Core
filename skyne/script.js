document.addEventListener('DOMContentLoaded', () => {
    // --- Lấy các thành phần UI ---
    const myiuTopLogo = document.getElementById('myiu-top-logo');
    const myiuTopLogoImg = myiuTopLogo ? myiuTopLogo.querySelector('img') : null;
    const aiResponseIndicator = document.getElementById('ai-response-indicator');

    const myiuAvatarLarge = document.getElementById('myiu-avatar-large');
    const avatarImage = myiuAvatarLarge ? myiuAvatarLarge.querySelector('img') : null; // Large avatar in status panel
    const statusSoma = document.getElementById('status-soma');
    const statusMemory = document.getElementById('status-memory');
    const statusTask = document.getElementById('status-task');
    const statusTemp = document.getElementById('status-temp');
    const statusEnergy = document.getElementById('status-energy');

    // New game-like status bar elements
    const gameStatusCpu = document.getElementById('game-status-cpu');
    const gameStatusNetwork = document.getElementById('game-status-network');
    // New detailed status metrics
    const statusCpu = document.getElementById('status-cpu');
    const statusRam = document.getElementById('status-ram');
    const statusNetwork = document.getElementById('status-network');
    const statusFps = document.getElementById('status-fps');


    const aiStatusText = document.getElementById('ai-status-text');
    const processingPower = document.getElementById('processing-power');
    const aiAlert = document.getElementById('ai-alert');
    const aiStatusPanel = document.getElementById('ai-status-panel'); // For warning pulse


    const consoleOutput = document.getElementById('output');
    const commandInput = document.getElementById('command-input');
    const sendCommandBtn = document.getElementById('send-command-btn'); // Send button
    const thoughtStream = document.getElementById('thoughts'); // Thought Log content div
    const typingCursor = document.querySelector('.typing-cursor');
    const currentTypingLine = document.querySelector('.current-typing-line'); // The P tag holding the cursor

    const navTabButtons = document.querySelectorAll('.nav-tab-btn');
    const contentSections = document.querySelectorAll('.content-section');
    const logOutput = document.getElementById('log-output'); // System Logs content div

    // Terminal Overlay Elements
    const terminalOverlay = document.getElementById('terminal-overlay');
    const closeTerminalBtn = document.getElementById('close-terminal-btn');
    const terminalOutput = document.getElementById('terminal-output');
    const terminalInput = document.getElementById('terminal-input');
    const typingCursorTerminal = document.querySelector('.typing-cursor-terminal');


    // --- Biến trạng thái ---
    const commandHistory = [];
    let historyIndex = -1;
    let isMyIuTyping = false;
    const responseQueue = [];

    const terminalHistory = [];
    let terminalHistoryIndex = -1;
    let isTerminalTyping = false;
    const terminalResponseQueue = [];

    // Store active tab to persist across reloads
    let activeTabId = localStorage.getItem('activeTabId') || 'chat-interface';
    
    // Check for Dark Mode preference
    const isDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (isDarkMode) {
        // Potentially add a 'dark-mode' class to body or adjust theme variables here
        // For this project, our default theme is already dark-mode friendly.
    }


    // --- WebSocket URL ---
    const WS_URL = `ws://${window.location.host}/ws/live_stream`; 
    let socket = null;

    // --- Sound Effects ---
    const sfx = {
        beep: new Audio('/static/audio/beep.mp3'), // You need to provide this file (short, subtle)
        chime: new Audio('/static/audio/chime.mp3'), // You need to provide this file (positive, clear)
        typing: new Audio('/static/audio/typing.mp3'), // Small clicky sound, loopable
        terminal_beep: new Audio('/static/audio/terminal_beep.mp3'), // For terminal interaction
        key_press: new Audio('/static/audio/key_press.mp3') // Subtle key press sound
    };
    // Ensure all audio objects are loaded, handle potential errors
    Object.values(sfx).forEach(audio => {
        audio.load();
        audio.volume = 0.3; // Adjust volume for all SFX
    });
    sfx.typing.loop = true; // Make typing sound loop

    function playSFX(soundName, loop = false) {
        if (sfx[soundName]) {
            sfx[soundName].currentTime = 0; // Rewind to start
            sfx[soundName].loop = loop;
            sfx[soundName].play().catch(e => console.warn(`SFX '${soundName}' playback failed:`, e));
        }
    }

    function stopSFX(soundName) {
        if (sfx[soundName]) {
            sfx[soundName].pause();
            sfx[soundName].currentTime = 0;
        }
    }


    // --- CÁC HÀM CẬP NHẬT GIAO DIỆN ---

    function updateAIStatus(status, power, alertMessage = null) {
        aiStatusText.textContent = status.toUpperCase();
        processingPower.textContent = `${power}%`;
        
        const statusIndicator = aiStatusText.previousElementSibling.querySelector('span:first-child');
        const statusDot = aiStatusText.previousElementSibling.querySelector('span:last-child');

        // Reset classes
        statusIndicator.classList.remove('bg-green-400', 'bg-yellow-400', 'bg-red-400');
        statusDot.classList.remove('bg-green-500', 'bg-yellow-500', 'bg-red-500');
        aiStatusText.classList.remove('text-green-400', 'text-yellow-400', 'text-red-400');

        if (status === 'online') {
            statusIndicator.classList.add('bg-green-400');
            statusDot.classList.add('bg-green-500');
            aiStatusText.classList.add('text-green-400');
        } else if (status === 'debugging' || status === 'optimizing') {
            statusIndicator.classList.add('bg-yellow-400');
            statusDot.classList.add('bg-yellow-500');
            aiStatusText.classList.add('text-yellow-400');
        } else if (status === 'offline' || status === 'error') {
            statusIndicator.classList.add('bg-red-400');
            statusDot.classList.add('bg-red-500');
            aiStatusText.classList.add('text-red-400');
        }

        if (alertMessage) {
            aiAlert.textContent = `ALERT: ${alertMessage}`;
            aiAlert.classList.remove('hidden');
            aiStatusPanel.classList.add('border-red-500/50', 'panel-glow-red-pulse'); // Custom class for warning
        } else {
            aiAlert.classList.add('hidden');
            aiStatusPanel.classList.remove('border-red-500/50', 'panel-glow-red-pulse');
        }
    }

    // Function to simulate AI avatar "nodding" or "blinking"
    function aiAvatarResponse(type) {
        if (!avatarImage) return;

        if (type === 'nod') {
            // Simulate a subtle nod (e.g., scale Y slightly or translateY)
            avatarImage.style.transition = 'transform 0.1s ease-in-out';
            avatarImage.style.transform = 'scaleY(0.95)';
            setTimeout(() => {
                avatarImage.style.transform = 'scaleY(1)';
            }, 100);
        } else if (type === 'blink') {
            // Simulate a blink (e.g., quick change in opacity or filter)
            avatarImage.style.transition = 'opacity 0.05s';
            avatarImage.style.opacity = '0.8';
            setTimeout(() => {
                avatarImage.style.opacity = '1';
            }, 50);
        }
        // General visual feedback for response
        avatarImage.classList.add('pulsing-avatar');
        setTimeout(() => {
            avatarImage.classList.remove('pulsing-avatar');
        }, 500); // Short pulse
    }


    function updateStatus(payload) {
        if (payload.soma) {
            let emoji = '😐';
            if (payload.soma === 'CALM' || payload.soma === 'IDLE') emoji = '😌';
            if (payload.soma === 'THINKING' || payload.soma === 'ANALYZING') emoji = '🤔';
            if (payload.soma === 'CONFUSED') emoji = '😟';
            if (payload.soma === 'STRESSED') emoji = '😫';
            statusSoma.textContent = `${emoji} ${payload.soma}`;
        }
        if (payload.memory_count) statusMemory.textContent = `${payload.memory_count} entries`;
        if (payload.task) statusTask.textContent = payload.task;
        if (payload.temp) statusTemp.textContent = `${payload.temp}°C`;
        if (payload.energy) statusEnergy.textContent = `${payload.energy}%`;

        // Update new detailed metrics
        if (payload.cpu !== undefined) {
            statusCpu.textContent = `${payload.cpu}%`;
            if (gameStatusCpu) gameStatusCpu.textContent = `${payload.cpu}%`;
        }
        if (payload.ram !== undefined) statusRam.textContent = `${payload.ram.used}GB / ${payload.ram.total}GB`;
        if (payload.network !== undefined) {
            statusNetwork.textContent = `${payload.network} Mbps`;
            if (gameStatusNetwork) gameStatusNetwork.textContent = `${payload.network}Mbps`;
        }
        if (payload.fps !== undefined) statusFps.textContent = `${payload.fps}`;
    }

    // New: Type out thoughts in Thought Log
    const thoughtQueue = [];
    let isThinking = false;
    let currentThoughtElement = null;

    function processThoughtQueue() {
        if (isThinking || thoughtQueue.length === 0) {
            return;
        }
        isThinking = true;
        const { source, message } = thoughtQueue.shift();
        const now = new Date().toLocaleTimeString('vi-VN');
        const p = document.createElement('p');
        p.classList.add('thought-bubble');
        p.innerHTML = `<span class="text-pink-400">[${now} <span class="orbitron">${source}</span>]:</span> <span class="text-gray-400 thought-typing-line"></span>`;
        thoughtStream.appendChild(p);
        thoughtStream.scrollTop = thoughtStream.scrollHeight;
        currentThoughtElement = p.querySelector('.thought-typing-line');

        let i = 0;
        playSFX('typing', true); // Play typing SFX for thoughts
        const interval = setInterval(() => {
            if (i < message.length) {
                currentThoughtElement.textContent += message.charAt(i);
                i++;
                thoughtStream.scrollTop = thoughtStream.scrollHeight;
            } else {
                clearInterval(interval);
                stopSFX('typing');
                isThinking = false;
                currentThoughtElement = null;
                playSFX('beep'); // Beep after thought complete
                setTimeout(processThoughtQueue, 500); // Process next thought after a slight delay
            }
        }, 20); // Faster typing for thoughts
    }

    function addThought(source, message) {
        thoughtQueue.push({ source, message });
        if (!isThinking) {
            processThoughtQueue();
        }
    }

    // New: Add log entry to System Logs
    function addSystemLog(level, message) {
        const now = new Date().toLocaleString('sv-SE'); // ISO format for logs
        const p = document.createElement('p');
        p.classList.add('log-entry', `log-${level.toLowerCase()}`);
        p.innerHTML = `[${now}] <span class="log-label-${level.toLowerCase()}">${level.toUpperCase()}:</span> ${message}`;
        logOutput.appendChild(p);
        logOutput.scrollTop = logOutput.scrollHeight;
    }

    // Auto-scroll function
    function autoScrollToBottom(element) {
        element.scrollTop = element.scrollHeight;
    }


    function processResponseQueue() {
        if (isMyIuTyping || responseQueue.length === 0) {
            if (!isMyIuTyping && responseQueue.length === 0 && document.getElementById('chat-interface').classList.contains('active')) {
                 typingCursor.style.display = 'inline-block';
                 if (myiuTopLogoImg) myiuTopLogoImg.classList.remove('pulsing-avatar'); // Stop pulse if idle
                 aiResponseIndicator.classList.add('hidden');
            }
            return;
        }

        isMyIuTyping = true;
        typingCursor.style.display = 'none';
        aiResponseIndicator.classList.remove('hidden'); // Show AI response indicator
        if (myiuTopLogoImg) myiuTopLogoImg.classList.add('pulsing-avatar'); // Start pulse when MyIu is typing
        if (avatarImage) aiAvatarResponse('nod'); // AI avatar nods/blinks

        const text = responseQueue.shift();
        const p = document.createElement('p');
        p.classList.add('myiu-response');
        p.textContent = ''; // Start empty for typing effect
        
        // Insert new response BEFORE the line with the typing cursor
        consoleOutput.insertBefore(p, currentTypingLine);

        let i = 0;
        playSFX('typing', true); // Play typing SFX for responses
        const interval = setInterval(() => {
            if (i < text.length) {
                p.textContent += text.charAt(i);
                i++;
                autoScrollToBottom(consoleOutput); // Auto-scroll
            } else {
                clearInterval(interval);
                stopSFX('typing');
                isMyIuTyping = false;
                aiResponseIndicator.classList.add('hidden'); // Hide AI response indicator
                if (document.getElementById('chat-interface').classList.contains('active')) {
                    typingCursor.style.display = 'inline-block';
                }
                if (myiuTopLogoImg) myiuTopLogoImg.classList.remove('pulsing-avatar'); // Stop pulse when done
                playSFX('chime'); // Play sound when response is complete
                speakResponse(text); // Speak the response
                setTimeout(processResponseQueue, 200);
            }
        }, 30); // Typing speed
    }
    
    function addResponse(message) {
        responseQueue.push(message);
        if (!isMyIuTyping) {
            processResponseQueue();
        }
    }

    // --- Speech Synthesis (Text-to-Speech) ---
    function speakResponse(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'en-US'; // Or 'vi-VN' for Vietnamese, if available and desired
            // You can choose a specific voice here if desired
            // const voices = window.speechSynthesis.getVoices();
            // utterance.voice = voices.find(voice => voice.name === 'Google US English'); // Example
            window.speechSynthesis.speak(utterance);
        } else {
            console.warn("Speech Synthesis not supported in this browser.");
        }
    }


    // --- XỬ LÝ LỆNH TỪ NGƯỜI DÙNG ---
    function handleCommandSend() {
        const commandText = commandInput.value.trim();
        if (commandText === '') return;

        typingCursor.style.display = 'none';
        if (myiuTopLogoImg) myiuTopLogoImg.classList.add('pulsing-avatar'); // Start pulse when user sends command

        const p = document.createElement('p');
        p.classList.add('user-command');
        p.textContent = `$ ${commandText}`;
        consoleOutput.insertBefore(p, currentTypingLine); // Insert user command before the current typing line
        autoScrollToBottom(consoleOutput); // Auto-scroll
        playSFX('beep'); // Play sound on command entry
        commandInput.blur(); // Auto blur input after sending

        // Dummy response for now
        setTimeout(() => {
            if (commandText.toLowerCase().includes("hello")) {
                addResponse("Greetings, Commander. How can I assist you further?");
            } else if (commandText.toLowerCase().includes("status")) {
                addResponse("All core systems are nominal. Processing power at 85%.");
            } else if (commandText.toLowerCase().includes("logs")) {
                addResponse("Redirecting to System Logs. See recent entries in the 'System Logs' tab.");
                addSystemLog('INFO', 'User requested system logs.');
                // Switch tab if possible
                navTabButtons.forEach(btn => {
                    if (btn.dataset.target === 'system-logs') btn.click();
                });
            } else if (commandText.toLowerCase().includes("terminal")) {
                addResponse("Activating secure CLI overlay. Type 'exit' to close.");
                openTerminalOverlay();
            } else if (commandText.toLowerCase().includes("fullscreen")) {
                toggleFullScreenChatMode();
                addResponse("Toggling Full-screen Chat Mode.");
            } else if (commandText.toLowerCase().includes("error")) {
                addResponse("Acknowledged. Simulating a minor system anomaly for demonstration.");
                addSystemLog('ERROR', 'Simulated critical error in ' + (new Date()).getMilliseconds() + 'ms.');
                updateAIStatus('error', 10, 'Simulated Critical Failure!');
            }
            else {
                addResponse(`Command '${commandText}' received. Processing... Stand by.`);
            }
            commandInput.focus(); // Auto-focus back to input after AI response
        }, 500);

        if (commandText) commandHistory.unshift(commandText);
        historyIndex = -1;
        commandInput.value = '';
    }

    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            handleCommandSend();
            e.preventDefault();
        } else if (e.key === 'ArrowUp') {
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                commandInput.value = commandHistory[historyIndex];
                e.preventDefault();
            }
        } else if (e.key === 'ArrowDown') {
            if (historyIndex > 0) {
                historyIndex--;
                commandInput.value = commandHistory[historyIndex];
            } else {
                historyIndex = -1;
                commandInput.value = '';
            }
            e.preventDefault();
        } else {
            playSFX('key_press'); // Play key press sound for typing
        }
    });

    // Send button click for desktop
    if (sendCommandBtn) {
        sendCommandBtn.addEventListener('click', handleCommandSend);
    }
    
    // Toggle Full-screen Chat Mode
    function toggleFullScreenChatMode() {
        document.body.classList.toggle('fullscreen-chat');
        // Re-focus input after mode change
        setTimeout(() => commandInput.focus(), 100);
    }

    // --- Terminal Overlay Logic ---
    function openTerminalOverlay() {
        terminalOverlay.classList.remove('hidden');
        setTimeout(() => terminalOverlay.style.opacity = '1', 10); // Fade in
        terminalInput.focus();
        playSFX('terminal_beep');
        typingCursorTerminal.style.display = 'inline-block'; // Ensure cursor is visible
    }

    closeTerminalBtn.addEventListener('click', () => {
        terminalOverlay.style.opacity = '0'; // Fade out
        setTimeout(() => terminalOverlay.classList.add('hidden'), 300);
        commandInput.focus(); // Return focus to main input
        stopSFX('typing'); // Ensure typing sound stops if active in terminal
        typingCursorTerminal.style.display = 'none'; // Hide terminal cursor
    });

    terminalInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const termCommand = terminalInput.value.trim();
            if (termCommand === '') return;

            // Display command
            const p = document.createElement('p');
            p.innerHTML = `<span class="text-green-400">myiu@core</span>:~ $ ${termCommand}`;
            terminalOutput.insertBefore(p, typingCursorTerminal.parentElement);
            autoScrollToBottom(terminalOutput); // Auto-scroll
            playSFX('terminal_beep');

            // Dummy terminal responses
            if (termCommand.toLowerCase() === 'help') {
                addTerminalResponse("Available commands: 'status', 'ping [ip]', 'ls', 'reboot', 'exit'");
            } else if (termCommand.toLowerCase() === 'status') {
                addTerminalResponse("System Uptime: 247 days, 14 hours, 33 minutes");
                addTerminalResponse("Core Temperature: 35.7°C");
                addTerminalResponse("Memory Usage: 38% (12GB/32GB)");
            } else if (termCommand.toLowerCase().startsWith('ping')) {
                addTerminalResponse("Pinging target... (Simulated)");
                setTimeout(() => addTerminalResponse("Response from 192.168.1.1: bytes=32 time=5ms TTL=64"), 500);
            } else if (termCommand.toLowerCase() === 'ls') {
                addTerminalResponse("core_modules.sys  log_archive/  config.json  user_data/");
            } else if (termCommand.toLowerCase() === 'reboot') {
                addTerminalResponse("Initiating reboot sequence... System will be offline momentarily.");
                setTimeout(() => {
                    closeTerminalBtn.click();
                    addResponse("MyIu Core is rebooting... Please wait.");
                    updateAIStatus('offline', 0, 'Rebooting...');
                    // Simulate reconnect after reboot
                    setTimeout(() => {
                        addResponse("MyIu Core has rebooted and is back online.");
                        updateAIStatus('online', 100);
                    }, 5000);
                }, 1000);
            } else if (termCommand.toLowerCase() === 'exit') {
                addTerminalResponse("Exiting CLI. Session terminated.");
                closeTerminalBtn.click();
            } else {
                addTerminalResponse(`Command not found: '${termCommand}'. Type 'help' for assistance.`);
            }

            // Save and reset
            terminalHistory.unshift(termCommand);
            terminalHistoryIndex = -1;
            terminalInput.value = '';
        } else if (e.key === 'ArrowUp') {
            if (terminalHistoryIndex < terminalHistory.length - 1) {
                terminalHistoryIndex++;
                terminalInput.value = terminalHistory[terminalHistoryIndex];
                e.preventDefault();
            }
        } else if (e.key === 'ArrowDown') {
            if (terminalHistoryIndex > 0) {
                terminalHistoryIndex--;
                terminalInput.value = terminalHistory[terminalHistoryIndex];
            } else {
                terminalHistoryIndex = -1;
                terminalInput.value = '';
            }
            e.preventDefault();
        } else {
            playSFX('key_press'); // Play key press sound for typing
        }
    });

    function addTerminalResponse(message) {
        terminalResponseQueue.push(message);
        if (!isTerminalTyping) {
            processTerminalResponseQueue();
        }
    }

    function processTerminalResponseQueue() {
        if (isTerminalTyping || terminalResponseQueue.length === 0) {
            if (!isTerminalTyping && terminalResponseQueue.length === 0) {
                typingCursorTerminal.style.display = 'inline-block';
            }
            return;
        }

        isTerminalTyping = true;
        typingCursorTerminal.style.display = 'none';

        const text = terminalResponseQueue.shift();
        const p = document.createElement('p');
        p.textContent = '';
        terminalOutput.insertBefore(p, typingCursorTerminal.parentElement);
        autoScrollToBottom(terminalOutput); // Auto-scroll

        let i = 0;
        playSFX('typing', true); // Play typing SFX for terminal
        const interval = setInterval(() => {
            if (i < text.length) {
                p.textContent += text.charAt(i);
                i++;
                autoScrollToBottom(terminalOutput); // Auto-scroll
            } else {
                clearInterval(interval);
                stopSFX('typing');
                isTerminalTyping = false;
                typingCursorTerminal.style.display = 'inline-block';
                setTimeout(processTerminalResponseQueue, 100);
            }
        }, 15); // Faster typing for terminal for snappier feel
    }


    // --- Placeholder for simple canvas graph in Data Visuals ---
    function drawSystemGraph() {
        const canvas = document.getElementById('system-graph-placeholder');
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        const parentDiv = canvas.parentElement;
        
        if (canvas.width !== parentDiv.offsetWidth || canvas.height !== parentDiv.offsetHeight) {
            canvas.width = parentDiv.offsetWidth;
            canvas.height = parentDiv.offsetHeight;
        }

        const gradient = ctx.createLinearGradient(0, 0, canvas.width, 0);
        gradient.addColorStop(0, 'rgba(0, 255, 204, 0.2)'); // Cyan
        gradient.addColorStop(0.5, 'rgba(128, 90, 213, 0.4)'); // Purple
        gradient.addColorStop(1, 'rgba(0, 255, 204, 0.2)');

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 2;
        ctx.shadowColor = '#00ffcc';
        ctx.shadowBlur = 5;

        const dataPoints = 80; // More data points for smoother graph
        const baseHeight = canvas.height / 2;
        const amplitude = canvas.height / 4;

        ctx.beginPath();
        ctx.moveTo(0, baseHeight + Math.sin(0) * amplitude);

        for (let i = 0; i < dataPoints; i++) {
            const x = (i / (dataPoints - 1)) * canvas.width;
            const y = baseHeight + Math.sin(i * 0.3 + Date.now() * 0.002) * amplitude * (0.8 + Math.random() * 0.4);
            ctx.lineTo(x, y);
        }
        ctx.stroke();
        ctx.shadowBlur = 0;
    }
    
    let graphInterval;
    navTabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;
            if (targetId === 'data-visuals') {
                if (!graphInterval) {
                    graphInterval = setInterval(drawSystemGraph, 50);
                }
            } else {
                if (graphInterval) {
                    clearInterval(graphInterval);
                    graphInterval = null;
                }
            }
            // Close mobile sidebar/status panel on tab change
            if (window.innerWidth < 1024) { // Only on mobile
                 // Assuming navigation-panel and status-panel are directly hidden/shown
                 // or have classes toggled. This part requires specific CSS/HTML setup if not done already.
                 // For now, if these panels cover the screen, we'd add logic here.
                 // Example: document.getElementById('navigation-panel').classList.add('hidden-on-mobile-tab-change');
            }
        });
    });

    // --- INITIAL DUMMY THOUGHTS FOR DEMO ---
    const initialThoughts = [
        { source: 'Cortex', message: 'Analyzing current user input patterns for optimal response generation.' },
        { source: 'Foreman', message: 'Task queue: Monitor system health; process simulated commands; generate dummy log data.' },
        { source: 'MemoryBank', message: 'Accessing contextual data from previous interaction logs. Retrieving user preferences.' },
        { source: 'NeuronNet', message: 'Running self-diagnostic protocols. All neural pathways are nominal.' },
        { source: 'DataForge', message: 'Synthesizing real-time environment data. Confirming atmospheric stability.' }
    ];

    let initialThoughtIndex = 0;
    function addInitialThoughtDelayed() {
        if (initialThoughtIndex < initialThoughts.length) {
            addThought(initialThoughts[initialThoughtIndex].source, initialThoughts[initialThoughtIndex].message);
            initialThoughtIndex++;
            setTimeout(addInitialThoughtDelayed, 3000); // Add next thought every 3 seconds
        }
    }


    // --- KẾT NỐI WEBSOCKET ---
    function connectWebSocket() {
        socket = new WebSocket(WS_URL);

        socket.onopen = () => {
            addThought('SYSTEM', 'Connection established. MyIu is online.');
            // Initial dummy status updates for new metrics
            updateStatus({ soma: 'IDLE', task: 'Awaiting Command', temp: 35, energy: 98, cpu: 25, ram: { used: 12, total: 32 }, network: 1.2, fps: 60 });
            updateAIStatus('online', 100);
            
            // Activate the correct tab based on localStorage
            const targetButton = document.querySelector(`.nav-tab-btn[data-target="${activeTabId}"]`);
            if (targetButton) {
                targetButton.click(); // This will also auto-focus the input if it's chat-interface
            } else {
                // Fallback to chat-interface if activeTabId is not found or invalid
                document.querySelector('.nav-tab-btn[data-target="chat-interface"]').click();
            }

            addInitialThoughtDelayed(); // Start adding initial thoughts
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
                        if (data.payload.soma) {
                            let aiCurrentStatus = 'online';
                            if (data.payload.soma === 'THINKING' || data.payload.soma === 'ANALYZING') aiCurrentStatus = 'debugging';
                            if (data.payload.soma === 'STRESSED' || data.payload.soma === 'CONFUSED') aiCurrentStatus = 'error';
                            updateAIStatus(aiCurrentStatus, 80 + Math.floor(Math.random() * 20));
                        }
                        // Add dummy system logs based on status changes (for demo)
                        if (data.payload.task && data.payload.task !== 'IDLE') {
                            addSystemLog('INFO', `MyIu task changed to: ${data.payload.task}`);
                        }
                        break;
                    case 'response':
                        addResponse(data.message);
                        break;
                    case 'ai_system_status':
                        updateAIStatus(data.status, data.power, data.alert);
                        if (data.alert) addSystemLog('WARN', data.alert); // Log alerts to system logs
                        break;
                    case 'log': // New: Handle backend logs explicitly
                        addSystemLog(data.level, data.message);
                        break;
                    default:
                        addThought('UNKNOWN', event.data);
                }
            } catch (e) {
                addThought('RAW', event.data);
                console.error("Error parsing WebSocket message:", e, event.data);
            }
        };

        socket.onclose = () => {
            addThought('SYSTEM', 'Connection lost. Attempting to reconnect...');
            updateStatus({ soma: 'OFFLINE', task: 'Connection Lost', temp: 'N/A', energy: 'N/A', cpu: 'N/A', ram: { used: 'N/A', total: 'N/A' }, network: 'N/A', fps: 'N/A' });
            updateAIStatus('offline', 0, 'Connection to Core Lost!');
            if (myiuTopLogoImg) myiuTopLogoImg.classList.remove('pulsing-avatar');
            addSystemLog('ERROR', 'WebSocket connection closed. Attempting reconnect in 5s.');
            stopSFX('typing'); // Ensure typing sound stops if offline
            setTimeout(connectWebSocket, 5000);
        };

        socket.onerror = (error) => {
            console.error("WebSocket Error:", error);
            addThought('SYSTEM', 'An error occurred with the connection.');
            updateAIStatus('error', 0, 'WebSocket Error!');
            if (myiuTopLogoImg) myiuTopLogoImg.classList.remove('pulsing-avatar');
            addSystemLog('ERROR', 'WebSocket error detected: ' + error.message);
            stopSFX('typing'); // Ensure typing sound stops if error
        };
    }

    // --- EVENT LISTENERS FOR MOBILE SWIPE ---
    let touchstartX = 0;
    let touchendX = 0;
    const mainContentArea = document.getElementById('main-content-area');

    function checkSwipe() {
        const minSwipeDistance = 50; // pixels
        const currentIndex = Array.from(navTabButtons).findIndex(btn => btn.classList.contains('active'));
        if (currentIndex === -1) return;

        if (touchendX < touchstartX - minSwipeDistance) { // Swiped left
            const nextIndex = (currentIndex + 1) % navTabButtons.length;
            navTabButtons[nextIndex].click();
        }
        if (touchendX > touchstartX + minSwipeDistance) { // Swiped right
            const prevIndex = (currentIndex - 1 + navTabButtons.length) % navTabButtons.length;
            navTabButtons[prevIndex].click();
        }
    }

    mainContentArea.addEventListener('touchstart', e => {
        touchstartX = e.changedTouches[0].screenX;
    }, false);

    mainContentArea.addEventListener('touchend', e => {
        touchendX = e.changedTouches[0].screenX;
        checkSwipe();
    }, false);


    // --- KHỞI ĐỘNG ---
    connectWebSocket();

    // Initial check for typing cursor when page loads
    if (document.getElementById('chat-interface').classList.contains('active')) {
        typingCursor.style.display = 'inline-block';
        commandInput.focus(); // Auto-focus on load for chat interface
    }
});
