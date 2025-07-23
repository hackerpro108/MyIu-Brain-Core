// src/components/Message.tsx

import React from 'react';
import { Message } from '../types';

interface MessageProps {
  message: Message;
}

const MessageComponent: React.FC<MessageProps> = ({ message }) => {
  const getMessageStyle = () => {
    switch (message.type) {
      case 'user':
        return 'bg-blue-500 text-white self-end';
      case 'myiu':
        return 'bg-gray-700 text-gray-200 self-start';
      case 'system':
        return 'bg-yellow-500 text-black self-center text-sm italic';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className={`p-3 my-2 rounded-lg max-w-lg ${getMessageStyle()}`}>
      <p>{message.text}</p>
    </div>
  );
};

export default MessageComponent;