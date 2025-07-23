// src/components/ChatBox.tsx

import React, { useState, useRef, useEffect } from 'react';
import { Message } from '../types';
import MessageComponent from './Message';
import { sendMessageToMyIu } from '../api/api';

const ChatBox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      text: input,
      type: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    const myiuResponse = await sendMessageToMyIu(userMessage.text);
    setMessages(prev => [...prev, myiuResponse]);
    setIsLoading(false);
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      <div className="flex-1 p-4 overflow-y-auto">
        <div className="flex flex-col">
          {messages.map(msg => (
            <MessageComponent key={msg.id} message={msg} />
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="p-4 bg-gray-800 border-t border-gray-700">
        <div className="flex">
          <input
            type="text"
            className="flex-1 bg-gray-700 rounded-l-md p-2 focus:outline-none"
            placeholder={isLoading ? 'MyIu is thinking...' : 'Nhập lệnh hoặc tin nhắn...'}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && handleSend()}
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            className="bg-blue-600 rounded-r-md px-4 hover:bg-blue-700 disabled:bg-gray-500"
            disabled={isLoading}
          >
            Gửi
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;