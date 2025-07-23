#!/bin/bash

# === KỊCH BẢN CÀI ĐẶT TỰ ĐỘNG GIAO DIỆN PHÁO ĐÀI MYIU ===
set -e
echo "▶️ Bắt đầu quá trình cài đặt tự động cho Giao diện Pháo đài MyIu..."

# --- CÁC BIẾN CẤU HÌNH ---
PROJECT_DIR="/root/myiu-brain-core/fortress-ui"
NGINX_CONFIG_FILE="/etc/nginx/sites-available/default"

# --- BẮT ĐẦU ---
echo "▶️ Đi đến thư mục dự án: $PROJECT_DIR"
# Tạo thư mục nếu nó chưa tồn tại
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "▶️ Dọn dẹp môi trường cũ..."
rm -rf node_modules package-lock.json dist

echo "▶️ Tạo file package.json..."
cat > package.json << 'EOF'
{
  "name": "fortress-ui", "private": true, "version": "0.0.0", "type": "module",
  "scripts": { "dev": "vite", "build": "tsc && vite build", "preview": "vite preview" },
  "dependencies": { "react": "^18.2.0", "react-dom": "^18.2.0" },
  "devDependencies": { "@vitejs/plugin-react": "^4.2.1", "autoprefixer": "^10.4.19", "postcss": "^8.4.38", "tailwindcss": "^3.4.3", "typescript": "^5.2.2", "vite": "^5.2.0", "@types/react": "^18.2.66", "@types/react-dom": "^18.2.22" }
}
EOF

echo "▶️ Tạo file tsconfig.json..."
cat > tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "target": "ES2020", "useDefineForClassFields": true, "lib": ["ES2020", "DOM", "DOM.Iterable"], "module": "ESNext", "skipLibCheck": true,
    "moduleResolution": "bundler", "allowImportingTsExtensions": true, "resolveJsonModule": true, "isolatedModules": true, "noEmit": true, "jsx": "react-jsx",
    "strict": true, "noUnusedLocals": true, "noUnusedParameters": true, "noFallthroughCasesInSwitch": true
  },
  "include": ["src"], "references": [{ "path": "./tsconfig.node.json" }]
}
EOF

echo "▶️ Tạo file tsconfig.node.json..."
cat > tsconfig.node.json << 'EOF'
{
  "compilerOptions": {
    "composite": true, "skipLibCheck": true, "module": "ESNext", "moduleResolution": "bundler", "allowSyntheticDefaultImports": true, "strict": true
  },
  "include": ["vite.config.ts"]
}
EOF

echo "▶️ Tạo file index.html..."
cat > index.html << 'EOF'
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>MyIu Fortress</title>
  </head>
  <body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body>
</html>
EOF

echo "▶️ Tạo cấu trúc thư mục src và các file cần thiết..."
mkdir -p src/components src/api src/types
# Tạo file src/main.tsx
cat > src/main.tsx << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
ReactDOM.createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
EOF
# Tạo file src/App.tsx
# Tạo file src/App.tsx
cat > src/App.tsx << 'EOF'
import ChatBox from './components/ChatBox';

function App() { 
  return (
    <div className="flex h-screen bg-gray-900">
      <main className="flex-1 h-screen">
        <ChatBox />
      </main>
    </div>
  ); 
}

export default App;
EOF
# Tạo các file trống khác
touch src/index.css src/components/ChatBox.tsx src/components/Message.tsx src/api/api.ts src/types/index.ts

echo "▶️ Cấu hình API endpoint..."
cat > src/api/api.ts << 'EOF'
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
EOF

echo "▶️ Bắt đầu 'npm install'..."
npm install

echo "▶️ Bắt đầu 'npm run build'..."
npm run build

echo "▶️ Cấu hình Nginx Reverse Proxy..."
cp $NGINX_CONFIG_FILE "${NGINX_CONFIG_FILE}.bak_$(date +%F)"
cat > $NGINX_CONFIG_FILE << 'EOF'
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    root /root/myiu-brain-core/fortress-ui/dist;
    index index.html index.htm;
    server_name _;
    location / { try_files $uri $uri/ /index.html; }
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
EOF

echo "▶️ Khởi động lại Nginx..."
systemctl restart nginx

echo "✅ HOÀN TẤT!"