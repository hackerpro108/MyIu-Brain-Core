import { Message } from '../types';
const API_ENDPOINT = '/api/chat';
export const sendMessageToMyIu = async (text: string): Promise<Message> => {
  try {
    const response = await fetch(API_ENDPOINT, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message: text }),
    });
    if (!response.ok) { throw new Error(`API call failed`); }
    const data = await response.json();
    return data.message;
  } catch (error) {
    return { id: `error-${Date.now()}`, text: 'Lỗi kết nối đến não bộ MyIu.', type: 'system', timestamp: new Date().toISOString() };
  }
};
