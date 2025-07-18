#!/bin/bash

# --- Màu sắc để output dễ đọc hơn ---
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}--- BẮT ĐẦU CHẨN ĐOÁN HỆ THỐNG MYIU ---${NC}"

# === KIỂM TRA 1: TIẾN TRÌNH ỨNG DỤNG ===
echo -e "\n[1] Kiểm tra tiến trình trên cổng 80..."
PROCESS_INFO=$(sudo lsof -i :80 | grep LISTEN)
if [ -z "$PROCESS_INFO" ]; then
    echo -e "${RED}[FAIL]${NC} Không có tiến trình nào đang chạy trên cổng 80."
else
    if echo "$PROCESS_INFO" | grep -q "python"; then
        echo -e "${GREEN}[PASS]${NC} Đã tìm thấy tiến trình Python đang chạy trên cổng 80."
        echo "$PROCESS_INFO"
    else
        echo -e "${RED}[FAIL]${NC} Cổng 80 đang bị chiếm bởi một dịch vụ khác không phải MyIu:"
        echo "$PROCESS_INFO"
    fi
fi

# === KIỂM TRA 2: TÍNH TOÀN VẸN CỦA main.py ===
echo -e "\n[2] Kiểm tra mã nguồn main.py..."
if ! grep -q 'from fastapi.staticfiles import StaticFiles' main.py || \
   ! grep -q 'app.mount("/", StaticFiles' main.py || \
   ! grep -q 'from fortress_api import app as fortress_app' main.py || \
   ! grep -q 'app.mount("/fortress-api", fortress_app)' main.py; then
    echo -e "${RED}[FAIL]${NC} Tệp main.py bị thiếu các dòng mã quan trọng để phục vụ giao diện hoặc API."
else
    echo -e "${GREEN}[PASS]${NC} Tệp main.py có vẻ chứa đầy đủ các cấu hình cần thiết."
fi

# === KIỂM TRA 3: HỆ THỐNG TỆP GIAO DIỆN (FRONTEND) ===
echo -e "\n[3] Kiểm tra hệ thống tệp frontend..."
if [ ! -d "frontend" ]; then
    echo -e "${RED}[FAIL]${NC} Không tìm thấy thư mục 'frontend'."
elif [ ! -f "frontend/index.html" ] && [ ! -f "frontend/nexus.html" ]; then
    echo -e "${RED}[FAIL]${NC} Không tìm thấy tệp 'index.html' hoặc 'nexus.html' trong thư mục 'frontend'."
elif [ ! -r "frontend/index.html" ] && [ ! -r "frontend/nexus.html" ]; then
    echo -e "${RED}[FAIL]${NC} Không có quyền đọc tệp giao diện."
else
    echo -e "${GREEN}[PASS]${NC} Thư mục và tệp giao diện frontend có vẻ ổn."
fi

# === KIỂM TRA 4: ĐƯỜNG DẪN BÊN TRONG HTML ===
echo -e "\n[4] Kiểm tra đường dẫn tài nguyên trong tệp index.html..."
HTML_FILE="frontend/index.html"
if [ ! -f "$HTML_FILE" ]; then
    HTML_FILE="frontend/nexus.html"
fi

if [ -f "$HTML_FILE" ]; then
    if grep -q 'src="/frontend/' "$HTML_FILE" || grep -q 'href="/frontend/' "$HTML_FILE"; then
        echo -e "${RED}[FAIL]${NC} Tệp $HTML_FILE chứa đường dẫn tài nguyên sai (vẫn còn /frontend/)."
    else
        echo -e "${GREEN}[PASS]${NC} Đường dẫn tài nguyên bên trong $HTML_FILE có vẻ đúng."
    fi
else
    echo -e "${YELLOW}[WARN]${NC} Không tìm thấy tệp HTML để kiểm tra đường dẫn."
fi

# === KIỂM TRA 5: KẾT NỐI MẠNG NỘI BỘ ===
echo -e "\n[5] Kiểm tra kết nối tới máy chủ từ localhost..."
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" http://localhost:80)
if [ "$HTTP_CODE" == "200" ]; then
    echo -e "${GREEN}[PASS]${NC} Máy chủ phản hồi với mã 200 (OK) tại địa chỉ gốc."
elif [ "$HTTP_CODE" == "404" ]; then
    echo -e "${RED}[FAIL]${NC} Máy chủ đang chạy nhưng trả về lỗi 404 (Not Found) tại địa chỉ gốc."
else
    echo -e "${RED}[FAIL]${NC} Không thể kết nối tới http://localhost:80 (Mã lỗi: $HTTP_CODE)."
fi

echo -e "\n${YELLOW}--- HOÀN TẤT CHẨN ĐOÁN ---${NC}"
