// src/App.tsx
import { useState } from 'react';
import { ChatWindow } from './components/ChatWindow';
import { Sidebar } from './components/Sidebar';
import { MessageInput } from './components/MessageInput';

export default function App() {
  const [messages, setMessages] = useState<string[]>([]);
  const [panel, setPanel] = useState<'reflection' | 'thoughts' | 'mood'>('reflection');

  const handleSend = (msg: string) => {
    setMessages([...messages, msg]);
  };

  return (
    <div className="h-screen w-full flex flex-col">
      <div className="flex-1 flex overflow-hidden">
        <Sidebar selected={panel} onSelect={setPanel} />
        <ChatWindow messages={messages} />
      </div>
      <MessageInput onSend={handleSend} />
    </div>
  );
}

// src/components/Sidebar.tsx
interface SidebarProps {
  selected: 'reflection' | 'thoughts' | 'mood';
  onSelect: (panel: 'reflection' | 'thoughts' | 'mood') => void;
}

export function Sidebar({ selected, onSelect }: SidebarProps) {
  return (
    <div className="w-28 bg-gray-800 text-white flex flex-col items-center py-4 space-y-4">
      <button
        onClick={() => onSelect('reflection')}
        className={`text-sm ${selected === 'reflection' ? 'font-bold text-yellow-300' : ''}`}
      >
        Phản tư
      </button>
      <button
        onClick={() => onSelect('thoughts')}
        className={`text-sm ${selected === 'thoughts' ? 'font-bold text-yellow-300' : ''}`}
      >
        Suy nghĩ
      </button>
      <button
        onClick={() => onSelect('mood')}
        className={`text-sm ${selected === 'mood' ? 'font-bold text-yellow-300' : ''}`}
      >
        Cảm xúc
      </button>
    </div>
  );
}

// src/components/ChatWindow.tsx
interface ChatWindowProps {
  messages: string[];
}

export function ChatWindow({ messages }: ChatWindowProps) {
  return (
    <div className="flex-1 bg-white overflow-y-auto p-4 space-y-2">
      {messages.map((msg, idx) => (
        <div key={idx} className="bg-gray-100 px-4 py-2 rounded shadow-sm">
          {msg}
        </div>
      ))}
    </div>
  );
}

// src/components/MessageInput.tsx
import { useState } from 'react';

interface MessageInputProps {
  onSend: (msg: string) => void;
}

export function MessageInput({ onSend }: MessageInputProps) {
  const [value, setValue] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim()) return;
    onSend(value.trim());
    setValue('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex p-2 border-t bg-white">
      <input
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className="flex-1 border rounded px-3 py-2 text-sm focus:outline-none"
        placeholder="Nhập tin nhắn..."
      />
      <button type="submit" className="ml-2 px-4 py-2 bg-blue-600 text-white rounded">
        Gửi
      </button>
    </form>
  );
}
