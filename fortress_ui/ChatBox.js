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
