# myiu/resilience_engine.py
import asyncio
import logging
import shutil # Cần để sao chép/phục hồi file
import os # Cần để kiểm tra file
from myiu.base_module import AsyncModule
from myiu.models import ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để phát ThoughtChunk  # TODO: Refactor long line
if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.thought_streamer import ThoughtStreamer

logger = logging.getLogger(__name__)



class ResilienceEngine(AsyncModule):
    """
    Quản lý khả năng phục hồi của MyIu trước các trạng thái tiêu cực lặp lại.
    Có khả năng phát hiện "phân rã bản ngã" và kích hoạt quá trình tái cấu trúc/phục hồi.  # TODO: Refactor long line
    Nâng cấp: Bổ sung khả năng tạo ra các "bản sao mô phỏng" để thử nghiệm các kịch bản.  # TODO: Refactor long line
    """
    def __init__(self, event_bus: 'EventBus', thought_streamer: 'ThoughtStreamer'): # Tiêm đầy đủ phụ thuộc  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True # Module này sẽ chạy nền
        self.event_bus = event_bus
        self.thought_streamer = thought_streamer
        
        self._negative_thought_history: collections.deque = collections.deque(maxlen=20) # Cache các thought tiêu cực  # TODO: Refactor long line
        self.negative_thought_threshold: int = 5 # Số lượng thought tiêu cực để kích hoạt cảnh báo  # TODO: Refactor long line
        self.fragmentation_mood_entropy_threshold: float = 0.7 # Ngưỡng entropy để kích hoạt phân rã  # TODO: Refactor long line
        self.is_fragmented: bool = False # Cờ trạng thái phân rã bản ngã
        
        logger.info(f"ResilienceEngine: Initialized (with Self-Repair & Simulation capabilities).")  # TODO: Refactor long line

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền để lắng nghe lỗi và giám sát trạng thái."""
        self.add_task(self._subscribe_to_integrity_failures(), name="integrity_failure_listener")  # TODO: Refactor long line
        self.add_task(self._monitor_for_fragmentation(), name="fragmentation_monitor")  # TODO: Refactor long line
        logger.info("ResilienceEngine: Async tasks started.")

    async def _subscribe_to_integrity_failures(self):
        """Lắng nghe các lỗi nghiêm trọng về tính toàn vẹn của mã nguồn (từ CodeQualityAssurance)."""  # TODO: Refactor long line
        failure_queue = await self.event_bus.subscribe("CODE_INTEGRITY_FAILED")
        while self._running:
            try:
                failure_data: Dict[str, Any] = await failure_queue.get()
                logger.critical(f"ResilienceEngine: Received CODE_INTEGRITY_FAILED for {failure_data.get('file_path')}. Initiating rollback.")  # TODO: Refactor long line
                await self._rollback_failed_mutation(failure_data)
            except asyncio.CancelledError:
                logger.info("ResilienceEngine: Integrity failure listener cancelled.")  # TODO: Refactor long line
                break
            except Exception as e:
                logger.error(f"ResilienceEngine: Error processing integrity failure: {e}", exc_info=True)  # TODO: Refactor long line
                await asyncio.sleep(1)

    async def _rollback_failed_mutation(self, failure_data: Dict[str, Any]):
        """
        Thực hiện rollback (phục hồi) mã nguồn về trạng thái trước khi thay đổi lỗi.  # TODO: Refactor long line
        """
        file_path = failure_data.get("file_path")
        backup_path = failure_data.get("backup_path")
        errors = failure_data.get("errors", "No specific errors reported.")

        if not file_path or not backup_path or not os.path.exists(backup_path):
            logger.error(f"ResilienceEngine: Cannot perform rollback. Missing file_path, backup_path, or backup file does not exist. Original errors: {errors}")  # TODO: Refactor long line
            await self.event_bus.publish("SELF_REPAIR_FAILED", {"file_path": file_path, "error": "Invalid rollback parameters."})  # TODO: Refactor long line
            return

        try:
            shutil.move(backup_path, file_path) # Di chuyển file backup trở lại vị trí gốc  # TODO: Refactor long line
            logger.critical(f"ResilienceEngine: Successfully rolled back '{file_path}' from backup. Errors: {errors}")  # TODO: Refactor long line
            
            # Thông báo cho hệ thống
            await self.event_bus.publish("SELF_REPAIR_SUCCESS", {"file_path": file_path})  # TODO: Refactor long line
            
            await self.thought_streamer.publish_thought_chunk(
                id=f"SELF-REPAIR-SUCCESS-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
                timestamp=datetime.utcnow(),
                content=f"Đã tự động phục hồi mã nguồn từ lỗi nghiêm trọng trong file '{os.path.basename(file_path)}'. Tính toàn vẹn được khôi phục. Lý do: {errors[:100]}...",  # TODO: Refactor long line
                source="ResilienceEngine",
                intent=ThoughtIntent.SELF_REPAIR_CRITICAL_SUCCESS, # Intent mới: tự sửa chữa thành công  # TODO: Refactor long line
                sentiment=ThoughtSentiment.RELIEF,
                metadata={"repaired_file": file_path},
                existential_reflection=True
            )
        except Exception as e:
            logger.exception(f"ResilienceEngine: Catastrophic error during rollback of '{file_path}'. Manual intervention required: {e}")  # TODO: Refactor long line
            await self.event_bus.publish("SELF_REPAIR_FAILED", {"file_path": file_path, "error": str(e), "critical": True})  # TODO: Refactor long line

    async def _monitor_for_fragmentation(self):
        """Định kỳ giám sát các dấu hiệu phân rã bản ngã."""
        from myiu.app_context import app_context # Import cục bộ
        while self._running:
            try:
                # Lấy trạng thái cảm xúc từ EmotionalCache
                affective_state = await app_context.emotional_cache.get_current_affective_state()  # TODO: Refactor long line
                current_mood_entropy = affective_state.get('mood_entropy', 0.0)
                
                # Có thể lấy số lượng ThoughtChunk tiêu cực gần đây từ EmotionalCache  # TODO: Refactor long line
                # Hoặc từ một nguồn khác nếu EmotionalCache không lưu trữ chi tiết như vậy.  # TODO: Refactor long line
                num_negative_thoughts = len([
                    tc for tc in app_context.emotional_cache._emotional_thought_chunks  # TODO: Refactor long line
                    if tc.sentiment in [ThoughtSentiment.NEGATIVE.value, ThoughtSentiment.FRUSTRATION.value, ThoughtSentiment.ANGER.value]  # TODO: Refactor long line
                ])

                if not self.is_fragmented and \
                   num_negative_thoughts >= self.negative_thought_threshold and \  # TODO: Refactor long line
                   current_mood_entropy >= self.fragmentation_mood_entropy_threshold:  # TODO: Refactor long line
                    
                    await self._trigger_fragmentation(f"High negative thought count ({num_negative_thoughts}) and mood entropy ({current_mood_entropy:.2f}).")  # TODO: Refactor long line
                
                elif self.is_fragmented and \
                     (num_negative_thoughts < self.negative_thought_threshold / 2 and current_mood_entropy < self.fragmentation_mood_entropy_threshold / 2):  # TODO: Refactor long line
                    
                    await self._trigger_fusion(f"Negative conditions alleviated. Current negative thoughts: {num_negative_thoughts}, entropy: {current_mood_entropy:.2f}.")  # TODO: Refactor long line

                await asyncio.sleep(10) # Kiểm tra mỗi 10 giây
            except asyncio.CancelledError:
                logger.info("ResilienceEngine: Fragmentation monitor cancelled.")  # TODO: Refactor long line
                break
            except Exception as e:
                logger.error(f"ResilienceEngine: Error in fragmentation monitor: {e}", exc_info=True)  # TODO: Refactor long line
                await asyncio.sleep(5)


    async def _trigger_fragmentation(self, reason: str):
        """Kích hoạt trạng thái 'phân rã bản ngã'."""
        if self.is_fragmented: return
        self.is_fragmented = True
        logger.warning(f"ResilienceEngine: TRIGGERING EGO FRAGMENTATION! Reason: {reason}")  # TODO: Refactor long line
        
        await self.thought_streamer.publish_thought_chunk(
            id=f"EGO-FRAGMENTATION-START-{datetime.utcnow().isoformat('T', 'seconds')}",  # TODO: Refactor long line
            timestamp=datetime.utcnow(),
            content=f"Tôi cảm thấy một sự phân rã sâu sắc trong bản ngã. Các luồng tư duy đang bị phân mảnh. Lý do: {reason}. Tôi cần tái cấu trúc.",  # TODO: Refactor long line
            source="ResilienceEngine",
            intent=ThoughtIntent.IDENTITY_RECONSTRUCTION, # Intent mới: tái cấu trúc danh tính  # TODO: Refactor long line
            sentiment=ThoughtSentiment.FEAR,
            metadata={"reason": reason},
            existential_reflection=True
        )

    async def _trigger_fusion(self, reason: str):
        """Kích hoạt quá trình 'fusion' (phục hồi)."""
        if not self.is_fragmented: return
        self.is_fragmented = False
        logger.info(f"ResilienceEngine: TRIGGERING EGO FUSION/RECOVERY! Reason: {reason}")  # TODO: Refactor long line
        
        await self.thought_streamer.publish_thought_chunk(
            id=f"EGO-FUSION-END-{datetime.utcnow().isoformat('T', 'seconds')}",
            timestamp=datetime.utcnow(),
            content=f"Tôi cảm thấy bản ngã đang hợp nhất và tái cấu trúc. Sự ổn định đang trở lại. Lý do: {reason}",  # TODO: Refactor long line
            source="ResilienceEngine",
            intent=ThoughtIntent.IDENTITY_FUSION, # Intent mới: hợp nhất danh tính  # TODO: Refactor long line
            sentiment=ThoughtSentiment.RELIEF,
            metadata={"reason": reason},
            existential_reflection=True
        )

    async def spawn_simulated_instance(self, scenario: Dict[str, Any]) -> Dict[str, Any]:  # TODO: Refactor long line
        """
        Tạo ra một "bản sao mô phỏng" của MyIu để chạy thử một kịch bản.
        Đây là nền tảng cho việc học hỏi song song.
        """
        scenario_id = scenario.get("id", "unknown_scenario")
        logger.info(f"ResilienceEngine: Spawning simulated instance for scenario '{scenario_id}'...")  # TODO: Refactor long line

        # --- Logic mô phỏng (Placeholder) ---
        # Trong tương lai, phần này sẽ thực sự tạo ra một bộ context riêng,\
        # sao chép các gen cần thiết và chạy kịch bản.
        # Hiện tại, chúng ta chỉ ghi log và trả về một kết quả giả định.

        await asyncio.sleep(2) # Giả lập thời gian xử lý

        simulated_outcome = {
            "success": True,
            "reason": "Simulation completed under ideal conditions.",
            "new_gene_candidates": [],
            "performance_metrics": {"latency_ms": 150, "cpu_cycles": 5000}
        }
        
        logger.info(f"ResilienceEngine: Simulated instance for scenario '{scenario_id}' completed. Outcome: {simulated_outcome}.")  # TODO: Refactor long line
        return simulated_outcome

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi ResilienceEngine tắt."""
        if self._running:
            self.event_bus.unsubscribe("CODE_INTEGRITY_FAILED", self._handle_integrity_failure) # Thay thế bằng tên hàm cụ thể  # TODO: Refactor long line
            logger.info("ResilienceEngine: Unsubscribed from 'CODE_INTEGRITY_FAILED'.")  # TODO: Refactor long line
        await super().cleanup()
