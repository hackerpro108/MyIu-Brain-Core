# myiu/sensing_manager.py
import asyncio
import logging
from typing import Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime, timedelta
import random # Để mô phỏng sự kiện cảm nhận

from myiu.base_module import AsyncModule
    from myiu.models import ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để tạo ThoughtChunk  # TODO: Refactor long line
    from myiu.thought_streamer import ThoughtStreamer
    from myiu.personality_core import PersonalityCore


logger = logging.getLogger(__name__)



class SensingManager(AsyncModule):
    """
    Module này quản lý các cơ chế "cảm nhận" và thu thập dữ liệu đầu vào từ môi trường bên ngoài.  # TODO: Refactor long line
    Nó cũng chịu trách nhiệm nhận diện các tín hiệu môi trường "ngầm" để thích nghi bối cảnh.  # TODO: Refactor long line
    """
    def __init__(self, event_bus: 'EventBus', thought_streamer: 'ThoughtStreamer', personality_core: 'PersonalityCore',  # TODO: Refactor long line
                 sensing_interval_seconds: int = 15): # Nhận đủ phụ thuộc
        super().__init__()
        self.is_background_service = True # Module này sẽ chạy nền để thu thập dữ liệu  # TODO: Refactor long line
        self.event_bus = event_bus
        self.thought_streamer = thought_streamer
        self.personality_core = personality_core
        self.sensing_interval = timedelta(seconds=sensing_interval_seconds)
        self.last_sensing_time: Optional[datetime] = None
        
        logger.info("SensingManager: Initialized. Ready to perceive the world.")  # TODO: Refactor long line

    async def process_raw_input(self, raw_data: str) -> Dict[str, Any]:
        """
        Xử lý dữ liệu đầu vào thô từ môi trường (ví dụ: tin nhắn người dùng).
        Đây là nơi sẽ có các bước tiền xử lý như phân tích ngôn ngữ tự nhiên, v.v.  # TODO: Refactor long line
        """
        logger.info(f"SensingManager: Processing raw input: {raw_data[:100]}...")  # TODO: Refactor long line
        
        # Mô phỏng quá trình xử lý NLP cơ bản
        processed_text = raw_data.strip()
        detected_keywords = [word for word in processed_text.lower().split() if len(word) > 3]  # TODO: Refactor long line
        
        return {
            "text_content": processed_text,
            "detected_keywords": detected_keywords,
            "source_type": "user_input"
        }

    async def _monitor_environmental_signals(self):
        """
        Liên tục giám sát các tín hiệu môi trường "ngầm" và phân tích xu hướng.
        (Phần của "Hệ thống Nhận thức Môi trường Sâu & Thích nghi Bối cảnh")
        """
        while self._running:
            try:
                # Mô phỏng việc thu thập tín hiệu môi trường
                # Trong thực tế:
                # - Lắng nghe các thay đổi trong dữ liệu người dùng (tần suất, loại yêu cầu)  # TODO: Refactor long line
                # - Theo dõi tin tức công nghệ (qua API RSS/News)
                # - Giám sát hiệu suất mạng, tải server (nếu có quyền truy cập)
                
                # Ví dụ đơn giản: Giả định có sự thay đổi xu hướng nếu cứ 30s lại có một sự kiện ngẫu nhiên  # TODO: Refactor long line
                if random.random() < 0.2: # 20% cơ hội phát hiện xu hướng mới mỗi lần kiểm tra  # TODO: Refactor long line
                    event_type = random.choice(["new_topic_trend", "resource_fluctuation", "external_api_update"])  # TODO: Refactor long line
                    event_desc = f"Phát hiện xu hướng mới trong {event_type.replace('_', ' ')}."  # TODO: Refactor long line
                    logger.info(f"SensingManager: {event_desc}. Analyzing trends.")  # TODO: Refactor long line
                    
                    # Phát một sự kiện để các module khác (ví dụ: Cortex, DigitalMetabolismEngine) xử lý  # TODO: Refactor long line
                    await self.event_bus.publish('environmental.shift_detected', {  # TODO: Refactor long line
                        'type': event_type,
                        'description': event_desc,
                        'timestamp': self.event_bus.get_current_timestamp()
                    })

                await asyncio.sleep(self.sensing_interval.total_seconds()) # Kiểm tra mỗi khoảng thời gian xác định  # TODO: Refactor long line
            except asyncio.CancelledError:
                logger.info("SensingManager: Environmental monitoring cancelled.")  # TODO: Refactor long line
                break
            except Exception as e:
                logger.error(f"SensingManager: Error during environmental monitoring: {e}", exc_info=True)  # TODO: Refactor long line
                await asyncio.sleep(5) # Đợi trước khi thử lại


    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho SensingManager."""
        self.add_task(self._monitor_environmental_signals(), name="environmental_monitor_loop")  # TODO: Refactor long line
        logger.info("SensingManager: Environmental monitoring task started.")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi SensingManager tắt."""
        if self._running:
            logger.info("SensingManager: Cleanup complete.")
        await super().cleanup()
