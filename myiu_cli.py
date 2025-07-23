# Tên file: myiu_cli.py (phiên bản đã sửa lỗi)

import argparse
import asyncio
import requests
import websockets

# Cấu hình để nói chuyện với Nginx (cổng 80)
SERVER_HOST = "localhost"
SERVER_PORT = 80

def send_message_to_myiu(message_text):
    # 1. SỬA LỖI: Trỏ đến đúng đường dẫn API mà Nginx đang quản lý
    api_url = f"http://{SERVER_HOST}:{SERVER_PORT}/api/chat"
    
    # 2. SỬA LỖI: Gửi đúng định dạng dữ liệu mà fortress_api.py cần
    payload = {"message": message_text}
    
    try:
        # Gửi yêu cầu POST với payload mới
        response = requests.post(api_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            # In ra phản hồi từ Não bộ
            response_data = response.json()
            myiu_response = response_data.get("message", {}).get("text", "Không nhận được phản hồi text.")
            print(f"[MyIu] > {myiu_response}")
        else:
            print(f"Lỗi gửi lệnh. Status: {response.status_code}, Body: {response.text}")

    except requests.exceptions.ConnectionError:
        print("Lỗi kết nối. MyIu (main.py) đã chạy chưa?")
    except Exception as e:
        print(f"Đã có lỗi xảy ra: {e}")

async def listen_to_stream():
    # Giữ nguyên phần websocket
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
    
    subparsers.add_parser("stream", help="Lắng nghe dòng suy nghĩ")

    args = parser.parse_args()
    try:
        if args.command == "ask":
            send_message_to_myiu(args.message)
        elif args.command == "stream":
            asyncio.run(listen_to_stream())
    except KeyboardInterrupt:
        print("\nĐã thoát.")

if __name__ == "__main__":
    main()