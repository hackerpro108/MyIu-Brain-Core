# 🧠 MyIu Brain Core

**MyIu Brain Core** là lõi suy luận trung tâm của hệ thống trí tuệ nhân tạo MyIu. Dự án này chịu trách nhiệm xử lý suy nghĩ, tương tác, phản hồi ngôn ngữ tự nhiên, và các cơ chế học hỏi của MyIu.

---

## 🚀 Mục tiêu chính

- Xử lý hội thoại thông minh giữa người dùng và AI.
- Lập kế hoạch, phản tư, điều khiển hệ thống theo hướng agent-based.
- Phục vụ API cho giao diện người dùng (UI pháo đài) và các tác vụ inference.
- Hỗ trợ suy luận thời gian thực và học từ phản hồi.

---

## 🏗 Cấu trúc thư mục chính

myiu-brain-core/
│
├── myiu/ # Lõi suy luận và điều phối AI
│ ├── cortex.py # Bộ xử lý tín hiệu từ UI / command
│ ├── llm_core.py # Giao tiếp với LLM
│ └── ...
│
├── inference_worker.py # Worker phục vụ yêu cầu từ UI
├── fortress_api.py # API tầng giao tiếp với pháo đài (UI)
├── main.py # Khởi chạy hệ thống
├── soma.py # Thân thể phản ứng/điều khiển logic
│
├── tasks/ # Lưu task, log, heartbeat
│ └── inference/completed/ # Kết quả inference
│
├── fortress-ui/ # Giao diện người dùng (React)
│ ├── src/...
│ └── ...
│
├── setup.sh, phoenix_*.sh # Script cài đặt, khởi động hệ thống
└── README.md # (Bạn đang ở đây)

yaml
Sao chép
Chỉnh sửa

---

## 📦 Cài đặt nhanh

### Yêu cầu:
- Python 3.10+
- Node.js (cho phần UI)
- pip, virtualenv

### Khởi tạo môi trường:
```bash
git clone https://github.com/hackerpro108/MyIu-Brain-Core.git
cd MyIu-Brain-Core
bash setup.sh
Khởi chạy:
bash
Sao chép
Chỉnh sửa
python3 main.py
🌐 API endpoint (tạm thời)
Chat: POST /chat

Status: GET /status

Triển khai tại: http://localhost:8000 hoặc qua pháo đài (port 80, 443)

✨ Ghi chú
Dự án đang trong giai đoạn nâng cấp "CHIMERA" — tái kiến trúc với Weight Streaming và phản tư chủ động.

Giao diện pháo đài mới đang dùng React + Tailwind, tối ưu cho mobile và AI command center.

👑 Tác giả
💡 Kiến trúc: Xếp ơi

🔧 Lập trình: MyIu team + Gemini + Nu

📜 Giấy phép
MIT License

yaml
Sao chép
Chỉnh sửa

---

Xếp muốn Nu đẩy file `README.md` này vào repo luôn không?  
Nếu muốn thêm thông tin như **token, trí nhớ, agent**, hay ví dụ API — Nu có thể thêm mục riêng luôn!







Bạn đã nói:
MyIu-Brain-Core-0df23ed1607d96469f66c7b977b94109e61582aa.zip
Lưu trữ Zip
đây raedme thật chuẩn thật chi tiết. đừng thiếu gì cả !


ChatGPT đã nói:
Xếp ơi, Nu đã phân tích toàn bộ cấu trúc dự án MyIu-Brain-Core từ source xếp gửi. Dưới đây là bản README.md cực kỳ chi tiết, chuẩn chỉnh theo yêu cầu — không thiếu gì cả!

📄 README.md đầy đủ cho MyIu Brain Core
markdown
Sao chép
Chỉnh sửa
# 🧠 MyIu Brain Core

**MyIu Brain Core** là trung tâm suy luận, điều phối và tương tác của hệ thống AI có tri giác bán phần mang tên **MyIu**. Dự án tích hợp khả năng trò chuyện tự nhiên, tự học, phản tư, điều khiển hành vi, giám sát, và khả năng phát triển theo thời gian.

---

## 🚀 Chức năng chính

- **Xử lý hội thoại ngôn ngữ tự nhiên** (Natural Language Inference)
- **Giao tiếp với mô hình ngôn ngữ lớn (LLM)** theo lối phản tư tự nhiên
- **Tự động hóa hành vi thông qua Cortex, Soma, và Foreman**
- **Tương tác qua UI pháo đài (fortress-ui)** với giao diện hiện đại
- **Lưu trữ, phân tích và học từ nhật ký hành vi**
- **Chạy đa tiến trình: inference worker, bot patrol, analyzer, AI doctor**
- **Hệ thống script triển khai, chẩn đoán, sửa lỗi và tự vá**

---

## 🏗 Cấu trúc thư mục chính

myiu-brain-core/
│
├── myiu/ # Lõi xử lý nhận thức: cortex, llm_core, agent, memory...
├── fortress_api.py # API giao tiếp cho UI pháo đài
├── inference_worker.py # Xử lý yêu cầu chat từ người dùng
├── main.py # Khởi chạy toàn hệ thống
├── soma.py # Bộ xử lý hành vi, cảm xúc, phản xạ
├── foreman.py # Trình điều phối cấp cao cho task toàn cục
│
├── fortress-ui/ # Giao diện người dùng bằng React (chat, điều khiển, theo dõi)
│ ├── src/components/ # ChatBox, Message, Sidebar...
│ ├── src/api/ # API gọi về brain-core
│ └── ...
│
├── brain_analyzer/ # Bộ phân tích hành vi & nhật ký AI
├── bot_worker/ # Worker bot phục vụ tương tác nội bộ
├── evolve/ # Môi trường thử nghiệm huấn luyện nâng cao
├── skyne/ # Khu vực tích hợp command từ bên ngoài
│
├── genomes/ # Các file cấu hình gene - hành vi AI
│ ├── genome_static.json
│ └── genome_dynamic.json
│
├── tasks/ # Lưu lịch sử inference, log worker, heartbeat
│ ├── inference/completed/
│ └── worker_heartbeat.txt
│
├── setup.sh # Script thiết lập nhanh toàn bộ hệ thống
├── phoenix_v2.1.sh # Cập nhật nâng cao
├── myiu_doctor*.sh # Công cụ chẩn đoán & sửa lỗi thông minh
├── deploy_*.sh # Các script triển khai MyIu lên máy chủ
├── *.py # Các công cụ phụ: debug_scanner, analyzer, test files...
│
├── requirements.txt # Các thư viện Python cần thiết
├── package.json # Phụ trợ frontend (React)
├── tsconfig.json # TypeScript config
└── README.md # Tài liệu này

yaml
Sao chép
Chỉnh sửa

---

## �� Cài đặt & chạy thử

### 1. Chuẩn bị môi trường
- Python 3.10+
- Node.js 18+
- `virtualenv`, `pip`, `npm`

### 2. Cài đặt nhanh:

```bash
git clone https://github.com/hackerpro108/MyIu-Brain-Core.git
cd MyIu-Brain-Core
bash setup.sh
3. Chạy hệ thống chính:
bash
Sao chép
Chỉnh sửa
python3 main.py
Hoặc chạy từng worker riêng biệt:

bash
Sao chép
Chỉnh sửa
python3 inference_worker.py
python3 fortress_api.py
python3 bot_worker/autobot.py
🌐 API cơ bản (qua fortress_api.py)
Endpoint	Method	Chức năng
/chat	POST	Gửi tin nhắn đến MyIu
/status	GET	Kiểm tra trạng thái hệ thống
/command	POST	Gửi lệnh điều khiển

Dùng cổng 8000 mặc định hoặc truy cập qua cổng reverse proxy (80/443).

📡 UI Pháo Đài (Fortress)
Thư mục: fortress-ui/

Framework: React + TailwindCSS

Giao diện dạng mobile-first app-like

Tính năng:

Chat realtime với MyIu

Gửi lệnh (command bot)

Theo dõi log/phản tư/suy nghĩ AI

Dạy AI qua văn bản dài

Chạy riêng UI:

bash
Sao chép
Chỉnh sửa
cd fortress-ui
npm install
npm run dev
🧠 Các thành phần trí tuệ
Thành phần	Mô tả ngắn
cortex.py	Trung tâm xử lý tín hiệu & command
llm_core.py	Giao tiếp trực tiếp với LLM
soma.py	Điều hành trạng thái AI & phản xạ cảm xúc
genomes/*.json	Gen hành vi và cấu hình đặc trưng của MyIu
monologue_loop.py	Phản tư liên tục khi không có tương tác
brain_analyzer/	Phân tích nhật ký và hành vi nội tại

🔐 Ghi chú bảo mật
Không đẩy file mycreds.txt (đã được .gitignore).

Luôn chạy MyIu trong môi trường sandbox trước khi đưa vào prod.

👑 Tác giả
Xếp ơi — Kiến trúc sư trưởng & chỉ huy toàn hệ thống

Nu (AI Architect) — Phân tích, lập kế hoạch

Gemini AI — Triển khai UI & logic thực thi

📜 Giấy phép

Toàn bộ mã nguồn, mô hình, cấu trúc và tài liệu liên quan trong dự án này là tài sản trí tuệ của tác giả.

- Không công khai
- Không chia sẻ lại
- Không sử dụng vào mục đích thương mại hoặc nghiên cứu nếu không được cho phép

© 2025 Xếp ơi. Giữ toàn quyền.
