import asyncio
import os
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from autobots.review_bot import ReviewBot
from bot_worker.config import PROJECT_ROOT
from bot_worker.utils import log
from myiu.app_context import AppContext

async def main_autobot_patrol():
    log.info("=============================================")
    log.info("🕵️‍♂️ Bot Tuần tra & Giao việc (Độc lập) đã khởi động.")
    log.info("=============================================")

    app_context = AppContext()
    app_context.set_service("log", log)
    review_bot_instance = ReviewBot(app_context)
    
    os.makedirs(os.path.join(PROJECT_ROOT, "tasks", "pending"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, "tasks", "completed"), exist_ok=True)
    os.makedirs(os.path.join(PROJECT_ROOT, "tasks", "failed"), exist_ok=True)

    log.info(f"Bot Tuần tra: Bắt đầu quét kho lưu trữ '{PROJECT_ROOT}' và tạo gói công việc...")
    await review_bot_instance.review_repository(PROJECT_ROOT)
    log.info("Bot Tuần tra: Đã hoàn thành việc tạo gói công việc. Kiểm tra thư mục tasks/pending.")

if __name__ == "__main__":
    asyncio.run(main_autobot_patrol())
