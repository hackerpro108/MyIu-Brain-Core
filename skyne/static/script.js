document.addEventListener('DOMContentLoaded', () => {
    // --- Lấy các thành phần UI ---
    const aiStatusBar = document.getElementById('ai-status-bar');
    const aiStatusText = document.getElementById('ai-status-text');
    const processingPower = document.getElementById('processing-power');
    const aiAlert = document.getElementById('ai-alert');

    const consoleOutput = document.getElementById('output');
    const commandInput = document.getElementById('command-input');
    const sendCommandBtn = document.getElementById('send-command-btn');
    const typingCursor = document.querySelector('.typing-cursor');
    const currentTypingLine = document.querySelector('.current-typing-line');
    const aiResponseIndicator = document.getElementById('ai-response-indicator');
    const micBtn = document.getElementById('mic-btn'); // Nút micro
    const commandSuggestions = document.getElementById('command-suggestions'); // Gợi ý lệnh

    const thoughtStream = document.getElementById('thoughts');
    const logOutput = document.getElementById('log-output');

    const navButtons = document.querySelectorAll('#bottom-nav .nav-btn');
    const contentPanels = document.querySelectorAll('#main-content-area .content-panel');

    const detailPanel = document.getElementById('detail-panel');
    const closeDetailPanelBtn = document.getElementById('close-detail-panel');
    const detailSoma = document.getElementById('detail-soma');
    const detailMemory = document.getElementById('detail-memory');
    const detailCpu = document.getElementById('detail-cpu');
    const detailRam = document.getElementById('detail-ram');
    const detailTemp = document.getElementById('detail-temp');
    const detailNetwork = document.getElementById('detail-network');
    const detailFps = document.getElementById('detail-fps');
    const detailEnergy = document.getElementById('detail-energy');

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

    let activeTabId = localStorage.getItem('activeTabId') || 'chat-interface';
    console.log("Trạng thái tab ban đầu từ localStorage:", activeTabId);
    
    // SFX (Audio files must be in /static_assets/audio/)
    const sfx = {
        beep: new Audio('/static_assets/audio/beep.mp3'),
        chime: new Audio('/static_assets/audio/chime.mp3'),
        typing: new Audio('/static_assets/audio/typing.mp3'),
        terminal_beep: new Audio('/static_assets/audio/terminal_beep.mp3'),
        key_press: new Audio('/static_assets/audio/key_press.mp3')
    };
    Object.values(sfx).forEach(audio => {
        audio.load();
        audio.volume = 0.3;
    });
    sfx.typing.loop = true;

    function playSFX(soundName, loop = false) {
        if (sfx[soundName]) {
            sfx[soundName].currentTime = 0;
            sfx[soundName].loop = loop;
            sfx[soundName].play().catch(e => console.warn(`Lỗi phát SFX '${soundName}':`, e));
        } else {
            console.warn(`Không tìm thấy SFX '${soundName}'.`);
        }
    }

    function stopSFX(soundName) {
        if (sfx[soundName]) {
            sfx[soundName].pause();
            sfx[soundName].currentTime = 0;
        }
    }

    // --- Cập nhật Trạng thái AI (Thanh trên cùng) ---
    function updateAIStatusBar(status, power, alertMessage = null) {
        if (!aiStatusText || !processingPower || !aiAlert || !aiStatusBar) {
            console.warn("Không tìm thấy các phần tử thanh trạng thái AI. Không thể cập nhật trạng thái.");
            return;
        }

        aiStatusText.textContent = status.toUpperCase();
        processingPower.textContent = `${power}%`;
        
        const statusIndicator = aiStatusText.previousElementSibling.querySelector('span:first-child');
        const statusDot = statusIndicator ? statusIndicator.nextElementSibling : null;

        if (statusIndicator) statusIndicator.classList.remove('bg-green-400', 'bg-yellow-400', 'bg-red-400');
        if (statusDot) statusDot.classList.remove('bg-green-500', 'bg-yellow-500', 'bg-red-500');
        aiStatusText.classList.remove('text-green-400', 'text-yellow-400', 'text-red-400');

        if (status === 'TRỰC TUYẾN') {
            if (statusIndicator) statusIndicator.classList.add('bg-green-400');
            if (statusDot) statusDot.classList.add('bg-green-500');
            aiStatusText.classList.add('text-green-400');
        } else if (status === 'ĐANG GỠ LỖI' || status === 'ĐANG TỐI ƯU') {
            if (statusIndicator) statusIndicator.classList.add('bg-yellow-400');
            if (statusDot) statusDot.classList.add('bg-yellow-500');
            aiStatusText.classList.add('text-yellow-400');
        } else if (status === 'NGOẠI TUYẾN' || status === 'LỖI') {
            if (statusIndicator) statusIndicator.classList.add('bg-red-400');
            if (statusDot) statusDot.classList.add('bg-red-500');
            aiStatusText.classList.add('text-red-400');
        }

        if (alertMessage) {
            aiAlert.textContent = `CẢNH BÁO: ${alertMessage}`;
            aiAlert.classList.remove('hidden');
            aiStatusBar.classList.add('border-red-500/50'); // Chỉ thay đổi màu border, không animation glow
        } else {
            aiAlert.classList.add('hidden');
            aiStatusBar.classList.remove('border-red-500/50');
        }
    }

    // --- Cập nhật Trạng thái chung (hiện trên Bảng Chi tiết) ---
    function updateStatusMetrics(payload) {
        if (!detailSoma) { // Basic check for detail panel elements
            console.warn("Không tìm thấy các phần tử Detail Panel. Không thể cập nhật chỉ số.");
            return;
        }
        if (detailSoma && payload.soma) detailSoma.textContent = `${getEmojiForSoma(payload.soma)} ${payload.soma}`;
        if (detailMemory && payload.memory_count) detailMemory.textContent = `${payload.memory_count} mục`;
        if (detailCpu && payload.cpu !== undefined) detailCpu.textContent = `${payload.cpu}%`;
        if (detailRam && payload.ram !== undefined) detailRam.textContent = `${payload.ram.used}GB / ${payload.ram.total}GB`;
        if (detailTemp && payload.temp) detailTemp.textContent = `${payload.temp}°C`;
        if (detailNetwork && payload.network !== undefined) detailNetwork.textContent = `${payload.network} Mbps`;
        if (detailFps && payload.fps !== undefined) detailFps.textContent = `${payload.fps}`;
        if (detailEnergy && payload.energy) detailEnergy.textContent = `${payload.energy}%`;
    }

    function getEmojiForSoma(soma) {
        switch(soma) {
            case 'CALM': case 'IDLE': return '😌';
            case 'THINKING': case 'ANALYZING': return '🤔';
            case 'CONFUSED': return '😟';
            case 'STRESSED': return '😫';
            default: return '😐';
        }
    }

    // --- Nhật ký Suy nghĩ AI ---
    const thoughtQueue = [];
    let isThinking = false;
    let currentThoughtElement = null;

    function processThoughtQueue() {
        if (isThinking || thoughtQueue.length === 0) return;
        isThinking = true;
        const { source, message } = thoughtQueue.shift();
        const now = new Date().toLocaleTimeString('vi-VN');
        const p = document.createElement('p');
        p.classList.add('thought-bubble');
        p.innerHTML = `<span class="text-pink-400">[${now} <span class="orbitron">${source}</span>]:</span> <span class="text-gray-400 roboto-mono thought-typing-line"></span>`;
        if (thoughtStream) {
            thoughtStream.appendChild(p);
            thoughtStream.scrollTop = thoughtStream.scrollHeight;
        } else {
            console.warn("Không tìm thấy phần tử thoughtStream. Không thể thêm suy nghĩ.");
            isThinking = false;
            return;
        }
        currentThoughtElement = p.querySelector('.thought-typing-line');

        let i = 0;
        playSFX('typing', true);
        const interval = setInterval(() => {
            if (currentThoughtElement && i < message.length) {
                currentThoughtElement.textContent += message.charAt(i);
                i++;
                thoughtStream.scrollTop = thoughtStream.scrollHeight;
            } else {
                clearInterval(interval);
                stopSFX('typing');
                isThinking = false;
                currentThoughtElement = null;
                playSFX('beep');
                setTimeout(processThoughtQueue, 500);
            }
        }, 20);
    }
    function addThought(source, message) {
        thoughtQueue.push({ source, message });
        if (!isThinking) processThoughtQueue();
    }

    // --- Nhật ký Hệ thống ---
    function addSystemLog(level, message) {
        const now = new Date().toLocaleString('sv-SE');
        const p = document.createElement('p');
        p.classList.add('log-entry', `log-${level.toLowerCase()}`);
        p.innerHTML = `[${now}] <span class="log-label-${level.toLowerCase()}">${level.toUpperCase()}:</span> ${message}`;
        if (logOutput) {
            logOutput.appendChild(p);
            logOutput.scrollTop = logOutput.scrollHeight;
        } else {
            console.warn("Không tìm thấy phần tử logOutput. Không thể thêm nhật ký hệ thống.");
        }
    }

    // --- Tự động cuộn ---
    function autoScrollToBottom(element) {
        if (element) element.scrollTop = element.scrollHeight;
    }

    // --- Xử lý Phản hồi AI cho Chat ---
    function processResponseQueue() {
        if (isMyIuTyping || responseQueue.length === 0) {
            if (!isMyIuTyping && responseQueue.length === 0 && document.getElementById('chat-interface').classList.contains('active')) {
                 if (typingCursor) typingCursor.style.display = 'inline-block';
                 if (aiResponseIndicator) aiResponseIndicator.classList.add('hidden');
            }
            return;
        }

        isMyIuTyping = true;
        if (typingCursor) typingCursor.style.display = 'none';
        if (aiResponseIndicator) aiResponseIndicator.classList.remove('hidden');

        const text = responseQueue.shift();
        const p = document.createElement('p');
        p.classList.add('myiu-response');
        p.textContent = '';
        
        if (consoleOutput && currentTypingLine) {
            consoleOutput.insertBefore(p, currentTypingLine);
        } else {
            console.warn("Không tìm thấy phần tử consoleOutput hoặc currentTypingLine. Không thể thêm phản hồi.");
            isMyIuTyping = false;
            return;
        }

        let i = 0;
        playSFX('typing', true);
        const interval = setInterval(() => {
            if (p.textContent && i < text.length) {
                p.textContent += text.charAt(i);
                i++;
                autoScrollToBottom(consoleOutput);
            } else {
                clearInterval(interval);
                stopSFX('typing');
                isMyIuTyping = false;
                if (aiResponseIndicator) aiResponseIndicator.classList.add('hidden');
                if (document.getElementById('chat-interface').classList.contains('active')) {
                    if (typingCursor) typingCursor.style.display = 'inline-block';
                }
                playSFX('chime');
                speakResponse(text);
                setTimeout(processResponseQueue, 200);
            }
        }, 30);
    }
    function addResponse(message) {
        responseQueue.push(message);
        if (!isMyIuTyping) processResponseQueue();
    }

    // --- Chuyển văn bản thành giọng nói ---
    function speakResponse(text) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'vi-VN'; 
            utterance.rate = 0.95; // Tốc độ hơi chậm lại để tự nhiên hơn
            utterance.pitch = 1.05; // Cao độ hơi cao hơn để dễ thương hơn

            const setVoice = () => {
                const voices = window.speechSynthesis.getVoices();
                const vietnameseVoice = voices.find(voice => voice.lang === 'vi-VN' && (voice.name.includes('Google tiếng Việt') || voice.name.includes('Female'))); 
                if (vietnameseVoice) {
                    utterance.voice = vietnameseVoice;
                    console.log("Đã chọn giọng đọc tiếng Việt:", vietnameseVoice.name);
                } else {
                    console.warn("Không tìm thấy giọng đọc tiếng Việt tùy chỉnh (hoặc giọng nữ). Sẽ dùng giọng mặc định.");
                    voices.forEach(voice => console.log(`- ${voice.name} (${voice.lang})`));
                }
                window.speechSynthesis.speak(utterance);
            };

            if (window.speechSynthesis.getVoices().length === 0) {
                window.speechSynthesis.onvoiceschanged = setVoice;
            } else {
                setVoice();
            }
            
        } else {
            console.warn("Trình tổng hợp giọng nói không được hỗ trợ trong trình duyệt này.");
        }
    }

    // --- Xử lý Lệnh Người dùng ---
    const availableCommands = [ // Danh sách lệnh có sẵn cho autocomplete và xử lý
        'chào', 'trạng thái', 'nhật ký', 'thiết bị đầu cuối', 'terminal', 'toàn màn hình', 'fullscreen', 'lỗi',
        'chủ đề cyan', 'chủ đề tím', 'chủ đề cam', 'chế độ tàng hình', 'stealth mode',
        'help', 'status', 'ls', 'ping', 'reboot', 'exit' // Lệnh tiếng Anh cho terminal
    ];

    function handleCommandSend() {
        const commandText = commandInput.value.trim();
        if (commandText === '') return;

        if (typingCursor) typingCursor.style.display = 'none';

        const p = document.createElement('p');
        p.classList.add('user-command');
        p.textContent = `$ ${commandText}`;
        if (consoleOutput && currentTypingLine) {
            consoleOutput.insertBefore(p, currentTypingLine);
            autoScrollToBottom(consoleOutput);
        } else {
            console.warn("Không tìm thấy phần tử consoleOutput hoặc currentTypingLine để hiển thị lệnh.");
            return;
        }
        playSFX('beep');
        commandInput.blur();

        setTimeout(() => {
            let responseMsg = `Lệnh '${commandText}' đã nhận. Đang xử lý... Vui lòng chờ.`;
            let isHandled = false;

            if (commandText.toLowerCase().includes("chào myiu") || commandText.toLowerCase().includes("xin chào")) {
                responseMsg = "Chào Chỉ huy! Tôi có thể giúp gì cho bạn?";
                isHandled = true;
            } else if (commandText.toLowerCase().includes("trạng thái hệ thống") || commandText.toLowerCase() === "trạng thái") {
                responseMsg = "Tất cả hệ thống cốt lõi đang hoạt động bình thường. Sức mạnh xử lý ở mức 85%.";
                openDetailPanel({ // Sử dụng dữ liệu giả lập
                    soma: 'BÌNH TĨNH', memory_count: 382, cpu: 25, ram: { used: 12, total: 32 },
                    temp: 35, network: 1.2, fps: 60, energy: 98
                });
                isHandled = true;
            } else if (commandText.toLowerCase().includes("nhật ký") || commandText.toLowerCase().includes("xem log")) {
                responseMsg = "Chuyển hướng đến Nhật ký hệ thống. Xem các mục gần đây trong tab 'Nhật ký hệ thống'.";
                addSystemLog('THÔNG TIN', 'Người dùng yêu cầu nhật ký hệ thống.');
                navButtons.forEach(btn => { if (btn.dataset.target === 'system-logs') btn.click(); });
                isHandled = true;
            } else if (commandText.toLowerCase().includes("thiết bị đầu cuối") || commandText.toLowerCase().includes("mở terminal")) {
                responseMsg = "Kích hoạt lớp phủ CLI an toàn. Gõ 'thoát' để đóng.";
                toggleFullScreenTerminal();
                isHandled = true;
            } else if (commandText.toLowerCase().includes("toàn màn hình")) { 
                responseMsg = "Đang chuyển đổi sang Chế độ Terminal toàn màn hình.";
                toggleFullScreenTerminal();
                isHandled = true;
            } else if (commandText.toLowerCase().includes("lỗi") || commandText.toLowerCase().includes("vấn đề hệ thống")) {
                responseMsg = "Đã xác nhận. Đang mô phỏng một sự cố nhỏ của hệ thống để minh họa.";
                addSystemLog('LỖI', 'Mô phỏng lỗi nghiêm trọng trong ' + (new Date()).getMilliseconds() + 'ms.');
                updateAIStatusBar('LỖI', 10, 'Lỗi nghiêm trọng mô phỏng!');
                if (navigator.vibrate) { navigator.vibrate([100, 30, 100]); } // Rung nhẹ khi cảnh báo lỗi
                isHandled = true;
            } else if (commandText.toLowerCase().includes("chủ đề cyan")) {
                setTheme('cyan');
                responseMsg = "Đã chuyển sang chủ đề Cyan.";
                isHandled = true;
            } else if (commandText.toLowerCase().includes("chủ đề tím")) {
                setTheme('purple');
                responseMsg = "Đã chuyển sang chủ đề Tím.";
                isHandled = true;
            } else if (commandText.toLowerCase().includes("chủ đề cam")) {
                setTheme('orange');
                responseMsg = "Đã chuyển sang chủ đề Cam.";
                isHandled = true;
            } else if (commandText.toLowerCase().includes("chế độ tàng hình") || commandText.toLowerCase().includes("stealth mode")) {
                setTheme('stealth');
                responseMsg = "Đã kích hoạt Chế độ Tàng hình.";
                isHandled = true;
            }

            if (!isHandled) { // Gợi ý lệnh mẫu theo thời điểm trong ngày (nếu chưa có lệnh đặc biệt nào được xử lý)
                const hour = new Date().getHours();
                if (hour >= 6 && hour < 12) { // Sáng
                    responseMsg += "\n> Gợi ý buổi sáng: Thử gõ 'trạng thái' để kiểm tra hệ thống hoặc 'nhật ký' để xem các hoạt động gần đây.";
                } else if (hour >= 18 || hour < 6) { // Tối
                    responseMsg += "\n> Gợi ý buổi tối: Thử gõ 'an ninh' để kiểm tra các giao thức bảo mật hoặc 'ngủ' để kích hoạt chế độ tiết kiệm năng lượng.";
                }
            }


            addResponse(responseMsg);
            commandInput.focus();
        }, 500);

        if (commandText) commandHistory.unshift(commandText);
        historyIndex = -1;
        commandInput.value = '';
    }

    if (commandInput) {
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
                playSFX('key_press');
            }
        });

        // Gợi ý lệnh theo từng chữ gõ (autocomplete)
        commandInput.addEventListener('input', () => {
            const currentText = commandInput.value.toLowerCase();
            if (commandSuggestions) { // Check if element exists
                commandSuggestions.innerHTML = ''; // Clear old suggestions

                if (currentText.length > 0) {
                    const filteredSuggestions = availableCommands.filter(cmd => cmd.startsWith(currentText));
                    if (filteredSuggestions.length > 0) {
                        commandSuggestions.classList.remove('hidden');
                        filteredSuggestions.slice(0, 3).forEach(suggestion => { // Show max 3 suggestions
                            const span = document.createElement('span');
                            span.textContent = suggestion;
                            span.classList.add('px-2', 'py-0', 'mr-1', 'bg-gray-700/50', 'rounded-sm', 'cursor-pointer', 'hover:bg-gray-600');
                            span.addEventListener('click', () => {
                                commandInput.value = suggestion;
                                if (commandSuggestions) commandSuggestions.classList.add('hidden');
                                commandInput.focus();
                            });
                            suggestionsDiv.appendChild(span);
                        });
                    } else {
                        commandSuggestions.classList.add('hidden');
                    }
                } else {
                    commandSuggestions.classList.add('hidden');
                }
            }
        });
        commandInput.addEventListener('blur', () => {
            // Ẩn gợi ý sau khi input mất focus, với độ trễ nhỏ để click được gợi ý
            setTimeout(() => {
                if (commandSuggestions) commandSuggestions.classList.add('hidden');
            }, 150);
        });
    }

    if (sendCommandBtn) sendCommandBtn.addEventListener('click', handleCommandSend);
    
    // --- Logic Bảng Chi tiết (cho Chỉ số Hệ thống) ---
    function openDetailPanel(metrics) {
        if (!detailPanel) {
            console.warn("Không tìm thấy phần tử Detail Panel. Không thể mở.");
            return;
        }
        detailPanel.classList.remove('hidden'); // Hiển thị nó (display: flex)
        detailPanel.classList.add('active'); // Kích hoạt animation trượt lên

        // Đổ dữ liệu vào bảng chi tiết
        updateStatusMetrics(metrics);
    }

    if (closeDetailPanelBtn) {
        closeDetailPanelBtn.addEventListener('click', () => {
            if (detailPanel) detailPanel.classList.remove('active'); // Tắt animation trượt lên
            setTimeout(() => {
                if (detailPanel) detailPanel.classList.add('hidden'); // Ẩn sau khi animation hoàn tất
            }, 300); // Khớp với thời gian transition của CSS
        });
    }

    // --- Logic Lớp phủ Terminal ---
    function openTerminalOverlay() {
        if (terminalOverlay) {
            terminalOverlay.classList.remove('hidden');
            setTimeout(() => terminalOverlay.style.opacity = '1', 10);
            if (terminalInput) terminalInput.focus();
            playSFX('terminal_beep');
            if (typingCursorTerminal) typingCursorTerminal.style.display = 'inline-block';
        } else {
            console.warn("Không tìm thấy các phần tử lớp phủ Terminal.");
        }
    }

    function closeTerminalOverlay() {
        if (terminalOverlay) {
            terminalOverlay.style.opacity = '0';
            setTimeout(() => {
                terminalOverlay.classList.add('hidden');
            }, 300);
            if (commandInput) commandInput.focus();
            stopSFX('typing');
            if (typingCursorTerminal) typingCursorTerminal.style.display = 'none';
        }
    }

    if (closeTerminalBtn) closeTerminalBtn.addEventListener('click', closeTerminalOverlay);
    function toggleFullScreenTerminal() { 
        if (terminalOverlay && terminalOverlay.classList.contains('hidden')) {
            openTerminalOverlay();
        } else {
            closeTerminalOverlay();
        }
    }


    if (terminalInput) {
        terminalInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const termCommand = terminalInput.value.trim();
                if (termCommand === '') return;

                const p = document.createElement('p');
                p.innerHTML = `<span class="text-green-400">myiu@core</span>:~ $ ${termCommand}`;
                if (terminalOutput && typingCursorTerminal) {
                    terminalOutput.insertBefore(p, typingCursorTerminal.parentElement);
                    autoScrollToBottom(terminalOutput);
                } else {
                    console.warn("Không tìm thấy các phần tử output Terminal để hiển thị lệnh.");
                    return;
                }
                playSFX('terminal_beep');

                if (termCommand.toLowerCase().includes("help")) {
                    addTerminalResponse("Các lệnh có sẵn: 'trạng thái', 'ping [ip]', 'ls', 'khởi động lại', 'thoát'");
                } else if (termCommand.toLowerCase().includes("trạng thái")) {
                    addTerminalResponse("Thời gian hoạt động hệ thống: 247 ngày, 14 giờ, 33 phút");
                    addTerminalResponse("Nhiệt độ lõi: 35.7°C");
                    addTerminalResponse("Sử dụng bộ nhớ: 38% (12GB/32GB)");
                } else if (termCommand.toLowerCase().startsWith('ping')) {
                    addTerminalResponse("Đang ping mục tiêu... (Mô phỏng)");
                    setTimeout(() => addTerminalResponse("Phản hồi từ 192.168.1.1: bytes=32 time=5ms TTL=64"), 500);
                } else if (termCommand.toLowerCase() === 'ls') {
                    addTerminalResponse("core_modules.sys  log_archive/  config.json  user_data/");
                } else if (termCommand.toLowerCase() === 'khởi động lại') {
                    addTerminalResponse("Đang khởi tạo trình tự khởi động lại... Hệ thống sẽ tạm thời ngoại tuyến.");
                    setTimeout(() => {
                        closeTerminalOverlay();
                        addResponse("MyIu Core đang khởi động lại... Vui lòng chờ.");
                        updateAIStatusBar('NGOẠI TUYẾN', 0, 'Đang khởi động lại...');
                        setTimeout(() => {
                            addResponse("MyIu Core đã khởi động lại và trực tuyến.");
                            updateAIStatusBar('TRỰC TUYẾN', 100);
                        }, 5000);
                    }, 1000);
                } else if (termCommand.toLowerCase() === 'thoát') {
                    addTerminalResponse("Thoát CLI. Phiên đã kết thúc.");
                    closeTerminalOverlay();
                } else {
                    addTerminalResponse(`Không tìm thấy lệnh: '${termCommand}'. Gõ 'help' để được hỗ trợ.`);
                }

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
                    historyIndex--;
                    terminalInput.value = terminalHistory[terminalHistoryIndex];
                } else {
                    historyIndex = -1;
                    terminalInput.value = '';
                }
                e.preventDefault();
            } else {
                playSFX('key_press');
            }
        });
    }


    function addTerminalResponse(message) {
        terminalResponseQueue.push(message);
        if (!isTerminalTyping) processTerminalResponseQueue();
    }

    function processTerminalResponseQueue() {
        if (isTerminalTyping || terminalResponseQueue.length === 0) {
            if (!isTerminalTyping && terminalResponseQueue.length === 0) {
                if (typingCursorTerminal) typingCursorTerminal.style.display = 'inline-block';
            }
            return;
        }

        isTerminalTyping = true;
        if (typingCursorTerminal) typingCursorTerminal.style.display = 'none';

        const text = terminalResponseQueue.shift();
        const p = document.createElement('p');
        p.textContent = '';
        if (terminalOutput && typingCursorTerminal) {
            terminalOutput.insertBefore(p, typingCursorTerminal.parentElement);
            autoScrollToBottom(terminalOutput);
        } else {
            console.warn("Không tìm thấy các phần tử output Terminal để hiển thị phản hồi.");
            isTerminalTyping = false;
            return;
        }

        let i = 0;
        playSFX('typing', true);
        const interval = setInterval(() => {
            if (p.textContent && i < text.length) {
                p.textContent += text.charAt(i);
                i++;
                autoScrollToBottom(terminalOutput);
            } else {
                clearInterval(interval);
                stopSFX('typing');
                isTerminalTyping = false;
                if (typingCursorTerminal) typingCursorTerminal.style.display = 'inline-block';
                setTimeout(processTerminalResponseQueue, 100);
            }
        }, 15);
    }


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
        gradient.addColorStop(0, 'rgba(0, 255, 204, 0.2)');
        gradient.addColorStop(0.5, 'rgba(128, 90, 213, 0.4)');
        gradient.addColorStop(1, 'rgba(0, 255, 204, 0.2)');

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 2;
        ctx.shadowColor = '#00ffcc';
        ctx.shadowBlur = 5;

        const dataPoints = 80;
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
    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;
            localStorage.setItem('activeTabId', targetId);

            console.log("Nút tab đã được nhấp:", targetId);

            contentPanels.forEach(panel => {
                if (panel.classList.contains('active')) {
                    console.log(`Đang ẩn panel: ${panel.id}`);
                    panel.classList.remove('active');
                    panel.style.display = 'none'; 
                    panel.style.pointerEvents = 'none';
                }
            });

            const targetPanel = document.getElementById(targetId);
            if (targetPanel) {
                console.log(`Đang hiển thị panel: ${targetId}`);
                targetPanel.classList.add('active');
                targetPanel.style.display = 'flex'; 
                targetPanel.style.pointerEvents = 'auto';

                navButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
            } else {
                console.error(`Không tìm thấy panel mục tiêu với ID ${targetId}!`);
            }

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
            if (detailPanel && detailPanel.classList.contains('active')) {
                closeDetailPanelBtn.click();
            }
        });
    });

    const initialThoughts = [
        { source: 'Cortex', message: 'Đang phân tích mẫu tương tác của người dùng để tạo phản hồi tối ưu.' },
        { source: 'Foreman', message: 'Hàng đợi tác vụ: Giám sát sức khỏe hệ thống; xử lý các lệnh mô phỏng; tạo dữ liệu nhật ký giả.' },
        { source: 'MemoryBank', message: 'Đang truy cập dữ liệu ngữ cảnh từ nhật ký tương tác trước. Đang truy xuất tùy chọn của người dùng.' },
        { source: 'NeuronNet', message: 'Đang chạy giao thức tự chẩn đoán. Tất cả các đường dẫn thần kinh đều bình thường.' },
        { source: 'DataForge', message: 'Đang tổng hợp dữ liệu môi trường thời gian thực. Xác nhận sự ổn định khí quyển.' }
    ];

    let initialThoughtIndex = 0;
    function addInitialThoughtDelayed() {
        if (initialThoughtIndex < initialThoughts.length) {
            addThought(initialThoughts[initialThoughtIndex].source, initialThoughts[initialThoughtIndex].message);
            initialThoughtIndex++;
            setTimeout(addInitialThoughtDelayed, 3000);
        }
    }

    // --- Quản lý chủ đề màu sắc ---
    function setTheme(themeName) {
        document.body.className = ''; // Xóa tất cả các class chủ đề hiện có
        document.body.classList.add(`theme-${themeName}`);
        localStorage.setItem('activeTheme', themeName); // Lưu chủ đề vào localStorage
        console.log("Đã chuyển chủ đề sang:", themeName);
    }

    // Khởi tạo chủ đề từ localStorage khi tải trang
    const savedTheme = localStorage.getItem('activeTheme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else {
        setTheme('cyan'); // Chủ đề mặc định
    }

    function connectWebSocket() {
        socket = new WebSocket(WS_URL);

        socket.onopen = () => {
            addThought('HỆ THỐNG', 'Kết nối được thiết lập. MyIu đã trực tuyến.');
            updateStatusMetrics({ soma: 'IDLE', memory_count: 382, cpu: 25, ram: { used: 12, total: 32 }, temp: 35, energy: 98, task: 'Chờ Lệnh', network: 1.2, fps: 60 });
            updateAIStatusBar('TRỰC TUYẾN', 100);
            
            const targetButton = document.querySelector(`#bottom-nav .nav-btn[data-target="${activeTabId}"]`);
            if (targetButton) {
                console.log("Kích hoạt tab ban đầu từ localStorage:", activeTabId);
                targetButton.click();
            } else {
                console.warn(`activeTabId "${activeTabId}" được lưu trữ không tìm thấy. Mặc định là giao diện trò chuyện.`);
                document.querySelector('#bottom-nav .nav-btn[data-target="chat-interface"]').click();
            }

            addInitialThoughtDelayed();
        };

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                switch (data.type) {
                    case 'thought':
                        addThought(data.source, data.message);
                        break;
                    case 'status':
                        updateStatusMetrics(data.payload); 
                        if (data.payload.soma) {
                            let aiCurrentStatus = 'TRỰC TUYẾN';
                            if (data.payload.soma === 'THINKING' || data.payload.soma === 'ANALYZING') aiCurrentStatus = 'ĐANG GỠ LỖI';
                            if (data.payload.soma === 'STRESSED' || data.payload.soma === 'CONFUSED') aiCurrentStatus = 'LỖI';
                            updateAIStatusBar(aiCurrentStatus, 80 + Math.floor(Math.random() * 20), data.payload.alert);
                        }
                        if (data.payload.task && data.payload.task !== 'IDLE') {
                            addSystemLog('THÔNG TIN', `Tác vụ MyIu đã thay đổi thành: ${data.payload.task}`);
                        }
                        break;
                    case 'response':
                        addResponse(data.message);
                        break;
                    case 'ai_system_status':
                        updateAIStatusBar(data.status, data.power, data.alert);
                        if (data.alert) addSystemLog('CẢNH BÁO', `Cảnh báo hệ thống: ${data.alert}`);
                        break;
                    case 'log':
                        addSystemLog(data.level, data.message);
                        break;
                    default:
                        addThought('KHÔNG RÕ', event.data);
                }
            } catch (e) {
                addThought('THÔ', event.data);
                console.error("Lỗi phân tích tin nhắn WebSocket:", e, event.data);
            }
        };

        socket.onclose = () => {
            addThought('HỆ THỐNG', 'Mất kết nối. Đang thử kết nối lại...');
            updateStatusMetrics({ soma: 'NGOẠI TUYẾN', memory_count: 'N/A', cpu: 'N/A', ram: { used: 'N/A', total: 'N/A' }, temp: 'N/A', energy: 'N/A' });
            updateAIStatusBar('NGOẠI TUYẾN', 0, 'Mất kết nối với Lõi!');
            addSystemLog('LỖI', 'Kết nối WebSocket đã đóng. Đang thử kết nối lại sau 5s.');
            stopSFX('typing');
            setTimeout(connectWebSocket, 5000);
        };

        socket.onerror = (error) => {
            console.error("Lỗi WebSocket:", error);
            addThought('HỆ THỐNG', 'Đã xảy ra lỗi với kết nối.');
            updateAIStatusBar('LỖI', 0, 'Lỗi WebSocket!');
            addSystemLog('LỖI', 'Lỗi WebSocket được phát hiện: ' + error.message);
            stopSFX('typing');
        };
    }

    let touchstartX = 0;
    let touchendX = 0;
    const mainContentArea = document.getElementById('main-content-area');

    function checkSwipe() {
        if (window.innerWidth >= 1024) return;

        const minSwipeDistance = 50;
        const currentActiveBtn = document.querySelector('#bottom-nav .nav-btn.active');
        if (!currentActiveBtn) return;

        const navButtonsArray = Array.from(navButtons);
        const currentIndex = navButtonsArray.indexOf(currentActiveBtn);
        if (currentIndex === -1) return;

        if (touchendX < touchstartX - minSwipeDistance) {
            const nextIndex = (currentIndex + 1) % navButtonsArray.length;
            console.log("Vuốt sang trái, đang thử nhấp tab:", navButtonsArray[nextIndex].dataset.target);
            navButtonsArray[nextIndex].click();
        }
        if (touchendX > touchstartX + minSwipeDistance) {
            const prevIndex = (currentIndex - 1 + navButtonsArray.length) % navButtonsArray.length;
            console.log("Vuốt sang phải, đang thử nhấp tab:", navButtonsArray[prevIndex].dataset.target);
            navButtonsArray[prevIndex].click();
        }
    }

    if (mainContentArea) {
        mainContentArea.addEventListener('touchstart', e => {
            touchstartX = e.changedTouches[0].screenX;
        }, false);

        mainContentArea.addEventListener('touchend', e => {
            touchendX = e.changedTouches[0].screenX;
            checkSwipe();
        }, false);
    } else {
        console.warn("Không tìm thấy phần tử mainContentArea. Cử chỉ vuốt bị tắt.");
    }


    connectWebSocket();

    if (document.getElementById('chat-interface').classList.contains('active') && commandInput) {
        commandInput.focus();
        if (typingCursor) typingCursor.style.display = 'inline-block';
    } else {
        console.warn("Giao diện trò chuyện không hoạt động hoặc không tìm thấy ô nhập lệnh khi tải ban đầu.");
    }

});
