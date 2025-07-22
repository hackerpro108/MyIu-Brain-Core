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
