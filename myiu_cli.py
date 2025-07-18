import argparse
import json
import uuid
import os
import asyncio
import websockets
import requests

# --- SỬA LỖI: Cập nhật lại đúng Port ---
SERVER_HOST = "localhost"
SERVER_PORT = 80

def send_message_to_myiu(message_text):
    api_url = f"http://{SERVER_HOST}:{SERVER_PORT}/ipc/message"
    event_data = { "topic": "user_message", "message": {"text": message_text} }
    try:
        response = requests.post(api_url, json=event_data, timeout=5)
        if response.status_code == 200:
            print(f"Đã gửi lệnh thành công: '{message_text}'")
        else:
            print(f"Lỗi gửi lệnh. Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Lỗi kết nối. MyIu (main.py) đã chạy chưa?")

async def listen_to_stream():
    ws_uri = f"ws://{SERVER_HOST}:{SERVER_PORT}/ws/live_stream"
    print(f"--- Đang lắng nghe dòng suy nghĩ từ {ws_uri} ---")
    try:
        async with websockets.connect(ws_uri) as websocket:
            print("--- KẾT NỐI THÀNH CÔNG ---")
            while True:
                message = await websocket.recv()
                print(f"[MyIu] > {message}")
    except Exception:
        print("Lỗi: Không thể kết nối hoặc kết nối bị ngắt.")

def main():
    parser = argparse.ArgumentParser(description="MyIu CLI 4.0")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    ask_parser = subparsers.add_parser("ask", help="Gửi lệnh tới MyIu")
    ask_parser.add_argument("message", help="Nội dung lệnh")
    
    stream_parser = subparsers.add_parser("stream", help="Lắng nghe dòng suy nghĩ")

    args = parser.parse_args()
    try:
        if args.command == "ask":
            send_message_to_myiu(args.message)
        elif args.command == "stream":
            asyncio.run(listen_to_stream())
    except KeyboardInterrupt:
        print("\\nĐã thoát.")

if __name__ == "__main__":
    main()
