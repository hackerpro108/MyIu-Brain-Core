# bot_worker/config.py

import os

# --- Mỏ neo Tuyệt đối ---
# Lấy đường dẫn tuyệt đối của thư mục chứa file config.py này (tức là bot_worker/)  # TODO: Refactor long line  # TODO: Refactor long line
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# PROJECT_ROOT được định nghĩa là thư mục cha của thư mục chứa file này.
# Cấu trúc của chúng ta là: myiu-brain-core/bot_worker/
# Vì vậy, thư mục cha của bot_worker/ chính là myiu-brain-core/
PROJECT_ROOT = os.path.dirname(_CURRENT_DIR)

# --- Các hằng số khác ---
# Định nghĩa các đường dẫn thư mục nhiệm vụ một cách tập trung
# os.path.join đảm bảo đường dẫn hoạt động trên mọi hệ điều hành.
TASKS_DIR = os.path.join(PROJECT_ROOT, "tasks")
TASKS_PENDING_DIR = os.path.join(TASKS_DIR, "pending")
TASKS_COMPLETED_DIR = os.path.join(TASKS_DIR, "completed")
TASKS_FAILED_DIR = os.path.join(TASKS_DIR, "failed")
