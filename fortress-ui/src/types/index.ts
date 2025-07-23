// src/types/index.ts

export type MessageType = 'user' | 'myiu' | 'system';

export interface Message {
  id: string;
  text: string;
  type: MessageType;
  timestamp: string;
}

export interface EmotionStatus {
  mood: '😃' | '😐' | '😢' | '🤔';
  currentThought: string;
}