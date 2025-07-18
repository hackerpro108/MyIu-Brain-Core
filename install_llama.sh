#!/bin/bash
# Script cài & build llama.cpp tối ưu cho MyIu VPS
set -e

log_info() {
    echo -e "\n\033[1;32m[INFO] $1\033[0m"
}

# --- BƯỚC 1: Cài công cụ & thư viện cần thiết ---
log_info "Cài đặt gói cần thiết..."
sudo apt-get update -y > /dev/null
sudo apt-get install -y build-essential cmake git python3 python3-pip ninja-build libcurl4-openssl-dev > /dev/null

# --- BƯỚC 2: Clone mã nguồn llama.cpp ---
cd ~
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp
fi
cd llama.cpp
git pull

# --- BƯỚC 3: Build llama.cpp với CMake ---
log_info "Bắt đầu biên dịch llama.cpp bằng CMake..."
rm -rf build
mkdir build
cd build

cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=ON -DLLAMA_OPENMP=ON -G Ninja
cmake --build .

log_info "✅ Biên dịch hoàn tất!"

# --- BƯỚC 4: Dọn dẹp ---
log_info "Dọn hệ thống..."
sudo apt-get autoremove --purge -y > /dev/null
sudo apt-get clean > /dev/null

log_info "--- HOÀN TẤT GIAI ĐOẠN 1.1! ---"
echo -e "\033[1;32mMyIu đã sẵn sàng để tích hợp lõi Trí Tuệ Tinh Gọn (Phi-2).\033[0m"
