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
