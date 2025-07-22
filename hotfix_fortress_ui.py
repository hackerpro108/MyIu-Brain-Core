import os
import shutil

PROJECT_ROOT = "/root/myiu-brain-core"
UI_DIR = os.path.join(PROJECT_ROOT, "fortress_ui")

files = {
    "index.html": """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Pháo Đài MyIu - Mobile React</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <link rel="manifest" href="manifest.json">
  <link rel="stylesheet" href="tailwind.css">
</head>
<body class="bg-gray-900 text-white m-0 p-0">
  <div id="root"></div>
  <script type="module" src="main.js"></script>
</body>
</html>
""",

    "main.js": """
import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.js";
const root = createRoot(document.getElementById("root"));
root.render(<App />);
""",

    "App.js": '''
import React, { useState } from "react";
import TabBar from "./TabBar.js";
import ChatBox from "./ChatBox.js";
import LogViewer from "./LogViewer.js";

export default function App() {
  const [tab, setTab] = useState("chat");
  return (
    <div className="bg-[#18181b] min-h-screen text-white font-inter flex flex-col items-center pb-14">
      <header className="mt-6 mb-2 text-center">
        <span className="text-4xl mr-2">🧠</span>
        <span className="text-3xl font-bold text-cyan-400">Pháo Đài MyIu</span>
        <div className="mt-2 text-lg font-medium">Mobile-first React App đã sẵn sàng!</div>
        <div className="text-base text-gray-300">Chào xếp! Hãy thổi hồn vào pháo đài này nhé.</div>
      </header>
      <main className="w-full max-w-md px-2 flex-1">
        {tab === "chat" && <ChatBox />}
        {tab === "log" && <LogViewer />}
      </main>
      <TabBar tab={tab} setTab={setTab} />
      <footer className="fixed bottom-2 left-0 right-0 text-center text-sm text-gray-400">
        🔥 Mobile-first UI • Powered by React
      </footer>
    </div>
  );
}
''',

    "TabBar.js": '''
import React from "react";
const tabs = [
  { key: "chat", label: "💬 Chat" },
  { key: "log", label: "📜 Log" }
];
export default function TabBar({ tab, setTab }) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#18181b] border-t border-gray-700 flex justify-center gap-6 py-2 z-10">
      {tabs.map(t => (
        <button
          key={t.key}
          onClick={() => setTab(t.key)}
          className={`px-6 py-2 rounded-full text-lg font-semibold transition 
            ${tab === t.key ? "bg-cyan-400 text-[#18181b] shadow-lg" : "bg-gray-800 text-white"}`}
        >
          {t.label}
        </button>
      ))}
    </nav>
  );
}
''',

    "ChatBox.js": '''
import React, { useState } from "react";
import { sendCommand } from "./api.js";
export default function ChatBox() {
  const [messages, setMessages] = useState([
    { from: "MyIu", text: "Xin chào xếp! Bạn cần gì hôm nay?", avatar: "🧠" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { from: "Bạn", text: input, avatar: "🧑‍💻" }]);
    setLoading(true);
    try {
      const res = await sendCommand(input);
      setMessages(msgs => [...msgs, { from: "MyIu", text: res.response || "...", avatar: "🧠" }]);
    } catch {
      setMessages(msgs => [...msgs, { from: "MyIu", text: "Không kết nối được AI.", avatar: "🧠" }]);
    }
    setLoading(false);
    setInput("");
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto bg-gray-800 rounded-lg p-2 mb-2">
        {messages.map((m, i) => (
          <div key={i}
            className={`flex mb-2 ${m.from === "Bạn" ? "justify-end" : "justify-start"}`}>
            <span className="mr-2">{m.avatar}</span>
            <span className={`px-4 py-2 rounded-2xl 
              ${m.from === "Bạn" ? "bg-cyan-400 text-[#18181b]" : "bg-yellow-300 text-[#18181b]"}`}>
              <b>{m.from}:</b> {m.text}
            </span>
          </div>
        ))}
        {loading && <div className="text-cyan-400">Đang gửi...</div>}
      </div>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          className="flex-1 px-3 py-2 rounded-lg bg-gray-700 text-white border-none"
          placeholder="Nhập lệnh hoặc tin nhắn..."
          onKeyDown={e => { if (e.key === "Enter") send(); }}
        />
        <button
          onClick={send}
          className="px-5 py-2 bg-cyan-400 text-[#18181b] font-bold rounded-lg"
          disabled={loading}
        >Gửi 🚀</button>
      </div>
    </div>
  );
}
''',

    "LogViewer.js": '''
import React, { useEffect, useState } from "react";
import { getLog } from "./api.js";
export default function LogViewer() {
  const [log, setLog] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    const fetchLog = async () => {
      try {
        const data = await getLog();
        if (mounted) setLog(data.log || []);
      } finally {
        if (mounted) setLoading(false);
      }
    };
    fetchLog();
    const interval = setInterval(fetchLog, 5000);
    return () => { mounted = false; clearInterval(interval); };
  }, []);

  return (
    <div className="bg-gray-800 p-3 rounded-lg h-full overflow-y-auto font-mono text-sm">
      {loading && <div className="text-cyan-400">Đang tải log...</div>}
      {log.map((entry, i) =>
        <div key={i}>
          <span className={entry.level === "ERROR"
            ? "text-red-400"
            : entry.level === "WARN"
              ? "text-yellow-400"
              : "text-green-300"
          }>
            [{entry.time}] <b>{entry.level}</b>:
          </span> {entry.msg}
        </div>
      )}
    </div>
  );
}
''',

    "api.js": '''
export async function sendCommand(cmd) {
  const r = await fetch("http://103.78.2.25:12440/send_command", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command: cmd })
  });
  return await r.json();
}
export async function getLog() {
  const r = await fetch("http://103.78.2.25:12440/log");
  return await r.json();
}
''',

    "manifest.json": """
{
  "name": "Pháo Đài MyIu",
  "short_name": "MyIuFortress",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#18181b",
  "theme_color": "#18181b",
  "description": "Mobile-first PWA Fortress UI for MyIu"
}
""",

    "tailwind.css": """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
body { font-family: 'Inter',sans-serif; background: #18181b; color: #fff; }
"""
}

def recreate_ui_dir():
    if os.path.exists(UI_DIR):
        shutil.rmtree(UI_DIR)
    os.makedirs(UI_DIR, exist_ok=True)
    print(f"📦 Đã làm sạch và tạo lại thư mục: {UI_DIR}")

def write_files():
    for fname, content in files.items():
        with open(os.path.join(UI_DIR, fname), "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        print(f"✅ Đã tạo file: {fname}")

if __name__ == "__main__":
    recreate_ui_dir()
    write_files()
    print("🎉 Build fortress_ui hoàn chỉnh xong! Sẵn sàng cho phát triển sản phẩm thực tế.")