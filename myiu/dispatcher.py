# myiu/dispatcher.py
from typing import Dict, Any

from myiu.base_module import AsyncModule
from myiu.event_bus import EventBus
from myiu.cortex import Cortex  # Cần để điều phối input đến Cortex
from myiu.affect import AffectLayer  # Cần để điều phối các sự kiện cảm xúc
from myiu.models import ThoughtChunkModel, ThoughtIntent # Cần để hiểu các ThoughtChunk  # TODO: Refactor long line
from myiu.models import ThoughtChunkModel, ThoughtIntent # Cần để hiểu các ThoughtChunk  # TODO: Refactor long line
logger = logging.getLogger(__name__)






class Dispatcher(AsyncModule):
    """
    Module này đóng vai trò trung tâm phân phối, đảm bảo các ThoughtChunk
    def __init__(self, event_bus: EventBus, cortex: Cortex, affect_layer: AffectLayer): # Tiêm phụ thuộc  # TODO: Refactor long line
    def __init__(self, event_bus: EventBus, cortex: Cortex, affect_layer: AffectLayer): # Tiêm phụ thuộc  # TODO: Refactor long line

    def __init__(
        self, event_bus: EventBus, cortex: Cortex, affect_layer: AffectLayer
    ):  # Tiêm phụ thuộc
        super().__init__()
        self.event_bus = event_bus
        self.cortex = cortex
        self.affect_layer = affect_layer
        Lắng nghe các input từ bên ngoài (ví dụ từ API chính) và chuyển tiếp đến Cortex.  # TODO: Refactor long line
        Lắng nghe các input từ bên ngoài (ví dụ từ API chính) và chuyển tiếp đến Cortex.  # TODO: Refactor long line
# Giả định main.py sẽ publish raw_input lên event_bus topic 'external_input'  # TODO: Refactor long line
    logger.info(f"Dispatcher: Received external input via EventBus. Routing to Cortex for processing.")  # TODO: Refactor long line
        # Cortex.process_input sẽ xử lý raw_input, tạo ThoughtChunk và đưa vào hàng đợi riêng của Cortex  # TODO: Refactor long line
        # Cortex.process_input sẽ xử lý raw_input, tạo ThoughtChunk và đưa vào hàng đợi riêng của Cortex  # TODO: Refactor long line
        """
        # Giả định main.py sẽ publish raw_input lên event_bus topic 'external_input'
        logger.info(
            f"Dispatcher: Received external input via EventBus. Routing to Cortex for processing."
        )
        # Cortex.process_input sẽ xử lý raw_input, tạo ThoughtChunk và đưa vào hàng đợi riêng của Cortex
        await self.cortex.process_input(message.get("data"))
logger.debug(f"Dispatcher: Received ThoughtChunk (ID: {thought_chunk.id}, Intent: {thought_chunk.intent}) from Cortex. Routing...")  # TODO: Refactor long line
    logger.debug(f"Dispatcher: Received ThoughtChunk (ID: {thought_chunk.id}, Intent: {thought_chunk.intent}) from Cortex. Routing...")  # TODO: Refactor long line
        """
        Lắng nghe ThoughtChunk được tạo bởi Cortex và có thể điều phối chúng.
        """
        # Có thể điều phối đến AffectLayer để tạo phản ứng cảm xúc nếu cần  # TODO: Refactor long line
            # await self.affect_layer.process_emotional_response(thought_chunk)  # TODO: Refactor long line
            # await self.affect_layer.process_emotional_response(thought_chunk)  # TODO: Refactor long line
                f"Dispatcher: Received ThoughtChunk (ID: {thought_chunk.id}, Intent: {thought_chunk.intent}) from Cortex. Routing..."
            # Ghi lại ThoughtChunk quan trọng vào Memory nếu nó chưa được Memory xử lý từ nguồn gốc  # TODO: Refactor long line
# Ghi lại ThoughtChunk quan trọng vào Memory nếu nó chưa được Memory xử lý từ nguồn gốc  # TODO: Refactor long line
            # Ví dụ điều phối dựa trên intent hoặc sentiment
            # Có thể điều phối đến ThoughtStreamer nếu đây là ThoughtChunk cuối cùng để xuất ra ngoài  # TODO: Refactor long line
                # Có thể điều phối đến ThoughtStreamer nếu đây là ThoughtChunk cuối cùng để xuất ra ngoài  # TODO: Refactor long line
                or thought_chunk.intent == ThoughtIntent.GENERAL_RESPONSE
            ):
                logger.error(f"Dispatcher: Error handling thought chunk from Cortex: {e}", exc_info=True)  # TODO: Refactor long line
                logger.error(f"Dispatcher: Error handling thought chunk from Cortex: {e}", exc_info=True)  # TODO: Refactor long line
                pass  # Hiện tại AffectLayer sẽ tự lắng nghe ThoughtChunk

            # Ghi lại ThoughtChunk quan trọng vào Memory nếu nó chưa được Memory xử lý từ nguồn gốc
            # (Thường thì Memory đã lắng nghe 'thought_chunk' trực tiếp)

            # Đăng ký lắng nghe input từ bên ngoài (giả định topic 'external_input')  # TODO: Refactor long line
            # Đăng ký lắng nghe input từ bên ngoài (giả định topic 'external_input')  # TODO: Refactor long line

        except Exception as e:
            logger.error(
                # Tuy nhiên, các module khác (như ThoughtStreamer, EmotionalCache, Memory)  # TODO: Refactor long line
                # Tuy nhiên, các module khác (như ThoughtStreamer, EmotionalCache, Memory)  # TODO: Refactor long line
            )
# self.event_bus.subscribe('thought_chunk', self._handle_thought_chunk_from_cortex)  # TODO: Refactor long line
    # logger.info("Dispatcher: Subscribed to 'thought_chunk' for internal routing.")  # TODO: Refactor long line
        # logger.info("Dispatcher: Subscribed to 'thought_chunk' for internal routing.")  # TODO: Refactor long line
        self._is_active = True

        # Đăng ký lắng nghe input từ bên ngoài (giả định topic 'external_input')
        self.event_bus.subscribe("external_input", self._handle_external_input)
        logger.info("Dispatcher: Subscribed to 'external_input' topic.")

        # Đăng ký lắng nghe ThoughtChunk từ Cortex (topic 'thought_chunk')
        self.event_bus.unsubscribe('external_input', self._handle_external_input)  # TODO: Refactor long line
        # self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk_from_cortex)  # TODO: Refactor long line
        # self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk_from_cortex)  # TODO: Refactor long line
        logger.info("Dispatcher: Unsubscribed from topics. Cleanup complete.")  # TODO: Refactor long line
        logger.info("Dispatcher: Unsubscribed from topics. Cleanup complete.")  # TODO: Refactor long line

    async def initialize_tasks(self):
        """Khởi tạo các tác vụ của Dispatcher."""
        await super().initialize_tasks()

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi Dispatcher tắt."""
        if self._is_active:
            self.event_bus.unsubscribe("external_input", self._handle_external_input)
            # self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk_from_cortex)
            self._is_active = False
            logger.info("Dispatcher: Unsubscribed from topics. Cleanup complete.")
        await super().cleanup()
