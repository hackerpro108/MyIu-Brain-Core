# myiu/rule_evaluator.py
import asyncio
import logging
from myiu.base_module import AsyncModule
from myiu.models import (
    OpinionPayload,
    from myiu.models import OpinionPayload, ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để gửi ý kiến và ThoughtChunk  # TODO: Refactor long line
    ThoughtSentiment,
)  # Cần để gửi ý kiến và ThoughtChunk  # TODO: Refactor long line

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.gen_editor import GenEditor
    from myiu.thought_streamer import ThoughtStreamer




logger = logging.getLogger(__name__)
Module này chịu trách nhiệm đánh giá các quy tắc (gen) trong hệ thống của MyIu  # TODO: Refactor long line

class RuleEvaluator(AsyncModule):
    """
    def __init__(self, event_bus: 'EventBus', gen_editor: 'GenEditor', thought_streamer: 'ThoughtStreamer'): # Nhận đủ phụ thuộc  # TODO: Refactor long line
    về hiệu quả, độ tin cậy và sự phù hợp.
    Nó là "Thành viên Thử nghiệm & Đánh giá" trong Hội đồng Nội tâm.
    """

    def __init__(
        self._evaluation_queue: asyncio.Queue = asyncio.Queue() # Hàng đợi cho các sự kiện đánh giá gen  # TODO: Refactor long line
        event_bus: "EventBus",
        logger.info("RuleEvaluator: Initialized. Ready to evaluate MyIu's rules.")  # TODO: Refactor long line
        thought_streamer: "ThoughtStreamer",
    async def evaluate_rule(self, rule_id: str, context: Dict[str, Any]) -> Dict[str, Any]:  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True  # Module này sẽ chạy nền
        Đây là logic phức tạp, cần truy cập dữ liệu hiệu suất và có thể là mô hình dự đoán.  # TODO: Refactor long line
        self.gen_editor = gen_editor
        logger.info(f"RuleEvaluator: Evaluating rule ID: {rule_id} in context: {context.get('scenario', 'general')}.")  # TODO: Refactor long line
        self._evaluation_queue: asyncio.Queue = (
            asyncio.Queue()
        )  # Hàng đợi cho các sự kiện đánh giá gen  # TODO: Refactor long line

        logger.warning(f"RuleEvaluator: Gene {rule_id} not found for evaluation.")  # TODO: Refactor long line
            "RuleEvaluator: Initialized. Ready to evaluate MyIu's rules."
        )  # TODO: Refactor long line

    evaluation_score = round(random.uniform(0.0, 1.0), 2) # 0.0 (kém) đến 1.0 (tốt)  # TODO: Refactor long line
        performance_impact = "positive" if evaluation_score > 0.6 else "negative"  # TODO: Refactor long line
    ) -> Dict[str, Any]:  # TODO: Refactor long line
        """
        # - Lấy dữ liệu thực thi của rule từ LogManager hoặc PerformanceAnalyzer.  # TODO: Refactor long line
        # - So sánh hiệu suất của rule với các benchmark hoặc các rule khác cùng loại.  # TODO: Refactor long line
        """
        logger.info(
            f"RuleEvaluator: Evaluating rule ID: {rule_id} in context: {context.get('scenario', 'general')}."
        )  # TODO: Refactor long line

        # Lấy thông tin gen từ GenEditor
        "recommendation": "Keep" if evaluation_score > 0.5 else "Revise or remove",  # TODO: Refactor long line
        "details": f"Rule {rule_id} showed a performance impact of {performance_impact} with score {evaluation_score}."  # TODO: Refactor long line
            logger.warning(
                f"RuleEvaluator: Gene {rule_id} not found for evaluation."
            )  # TODO: Refactor long line
            return {"is_valid": False, "reason": "Gene not found."}

        # Mô phỏng kết quả đánh giá
        evaluation_score = round(
            random.uniform(0.0, 1.0), 2
        )  # 0.0 (kém) đến 1.0 (tốt)  # TODO: Refactor long line
        performance_impact = (
            "positive" if evaluation_score > 0.6 else "negative"
        )  # TODO: Refactor long line

        # Trong thực tế:
        # - Lấy dữ liệu thực thi của rule từ LogManager hoặc PerformanceAnalyzer.  # TODO: Refactor long line
        # - So sánh hiệu suất của rule với các benchmark hoặc các rule khác cùng loại.  # TODO: Refactor long line
        logger.warning("RuleEvaluator: Invalid deliberation request received (missing ID or description).")  # TODO: Refactor long line

        result = {
            logger.info(f"RuleEvaluator: Received DELIBERATION_REQUEST (ID: {request_id}). Providing rule evaluation opinion.")  # TODO: Refactor long line
            "evaluation_score": evaluation_score,
            # Nếu yêu cầu tranh luận liên quan đến một quy tắc cụ thể ('rule_id' trong context)  # TODO: Refactor long line
            "recommendation": (
                "Keep" if evaluation_score > 0.5 else "Revise or remove"
            evaluation_result = await self.evaluate_rule(rule_to_evaluate, context)  # TODO: Refactor long line
            opinion_content = f"Đánh giá quy tắc '{rule_to_evaluate}': {evaluation_result['details']}. Khuyến nghị: {evaluation_result['recommendation']}."  # TODO: Refactor long line
        }

        opinion_content = f"Vấn đề '{problem_description[:50]}...' được gửi tới RuleEvaluator. Hiện không có quy tắc cụ thể nào để đánh giá liên quan trực tiếp. Cần làm rõ thêm."  # TODO: Refactor long line
        confidence = 0.5 # Mức độ tự tin trung bình nếu không có dữ liệu cụ thể  # TODO: Refactor long line

        return result

    async def _handle_deliberation_request(self, message: Dict[str, Any]):
        """
        Xử lý yêu cầu tranh luận từ Hội đồng, đưa ra ý kiến đánh giá quy tắc.
        """
        request_id = message.get("request_id")
        metadata={"evaluation_result": evaluation_result if rule_to_evaluate else {}},  # TODO: Refactor long line
        intent=message.get('intent'), # Truyền intent gốc của cuộc thảo luận  # TODO: Refactor long line

        if not request_id or not problem_description:
            logger.info(f"RuleEvaluator: Published EVALUATION_OPINION for ID: {request_id}.")  # TODO: Refactor long line
                "RuleEvaluator: Invalid deliberation request received (missing ID or description)."
            async def _handle_thought_chunk_for_evaluation(self, message: Dict[str, Any]):  # TODO: Refactor long line
            return

        logger.info(
            f"RuleEvaluator: Received DELIBERATION_REQUEST (ID: {request_id}). Providing rule evaluation opinion."
        )  # TODO: Refactor long line

        # Nếu yêu cầu tranh luận liên quan đến một quy tắc cụ thể ('rule_id' trong context)  # TODO: Refactor long line
        rule_to_evaluate = context.get("rule_id")
        ThoughtIntent.ETHICAL_REFLECTION, ThoughtIntent.SELF_DEFINITION_UPDATE  # TODO: Refactor long line
            evaluation_result = await self.evaluate_rule(
                rule_to_evaluate, context
            )  # TODO: Refactor long line
            opinion_content = f"Đánh giá quy tắc '{rule_to_evaluate}': {evaluation_result['details']}. Khuyến nghị: {evaluation_result['recommendation']}."  # TODO: Refactor long line
            logger.error(f"RuleEvaluator: Error handling thought chunk for evaluation: {e}", exc_info=True)  # TODO: Refactor long line
        else:
            opinion_content = f"Vấn đề '{problem_description[:50]}...' được gửi tới RuleEvaluator. Hiện không có quy tắc cụ thể nào để đánh giá liên quan trực tiếp. Cần làm rõ thêm."  # TODO: Refactor long line
            confidence = 0.5  # Mức độ tự tin trung bình nếu không có dữ liệu cụ thể  # TODO: Refactor long line

        # Gửi ý kiến đánh giá lên EventBus cho ConsensusEngine
        await self.event_bus.publish(
            "opinion.evaluation",
            OpinionPayload(
                request_id=request_id,
                logger.info("RuleEvaluator: Evaluation processing loop cancelled.")  # TODO: Refactor long line
                opinion_content=opinion_content,
                confidence=confidence,
                logger.error(f"RuleEvaluator: Error processing evaluation: {e}", exc_info=True)  # TODO: Refactor long line
                metadata={
                    "evaluation_result": evaluation_result if rule_to_evaluate else {}
                },  # TODO: Refactor long line
                intent=message.get(
                    "intent"
                ),  # Truyền intent gốc của cuộc thảo luận  # TODO: Refactor long line
                self.event_bus.subscribe('deliberation.request', self._handle_deliberation_request)  # TODO: Refactor long line
            logger.info("RuleEvaluator: Subscribed to 'deliberation.request' topic.")  # TODO: Refactor long line
        )
        logger.info(
            self.event_bus.subscribe('thought_chunk', self._handle_thought_chunk_for_evaluation)  # TODO: Refactor long line
        logger.info("RuleEvaluator: Subscribed to 'thought_chunk' for behavioral evaluation.")  # TODO: Refactor long line

    async def _handle_thought_chunk_for_evaluation(
        self.add_task(self._process_evaluations_loop(), name="rule_evaluation_processor")  # TODO: Refactor long line
    ):  # TODO: Refactor long line
        """
        Lắng nghe các ThoughtChunk để kích hoạt việc đánh giá gen.
        """
        try:
            self.event_bus.unsubscribe('deliberation.request', self._handle_deliberation_request)  # TODO: Refactor long line
            self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk_for_evaluation)  # TODO: Refactor long line
            if thought_chunk.gene_id and thought_chunk.intent in [
                ThoughtIntent.GENERAL_RESPONSE,
                ThoughtIntent.PROBLEM_SOLVER,
                ThoughtIntent.ETHICAL_REFLECTION,
                ThoughtIntent.SELF_DEFINITION_UPDATE,  # TODO: Refactor long line
            ]:
                # Đưa vào hàng đợi để xử lý đánh giá
                await self._evaluation_queue.put(thought_chunk)
        except Exception as e:
            logger.error(
                f"RuleEvaluator: Error handling thought chunk for evaluation: {e}",
                exc_info=True,
            )  # TODO: Refactor long line

    async def _process_evaluations_loop(self):
        """Vòng lặp xử lý các sự kiện đánh giá từ hàng đợi."""
        while self._running:
            try:
                thought_chunk = await self._evaluation_queue.get()
                await self.evaluate_behavior(thought_chunk)
                self._evaluation_queue.task_done()
            except asyncio.CancelledError:
                logger.info(
                    "RuleEvaluator: Evaluation processing loop cancelled."
                )  # TODO: Refactor long line
                break
            except Exception as e:
                logger.error(
                    f"RuleEvaluator: Error processing evaluation: {e}", exc_info=True
                )  # TODO: Refactor long line
                self._evaluation_queue.task_done()
                await asyncio.sleep(5)  # Đợi trước khi thử lại

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho RuleEvaluator."""
        # Lắng nghe các yêu cầu tranh luận từ Hội đồng Nội tâm
        self.event_bus.subscribe(
            "deliberation.request", self._handle_deliberation_request
        )  # TODO: Refactor long line
        logger.info(
            "RuleEvaluator: Subscribed to 'deliberation.request' topic."
        )  # TODO: Refactor long line

        # Lắng nghe các ThoughtChunk để tự động kích hoạt đánh giá gen
        self.event_bus.subscribe(
            "thought_chunk", self._handle_thought_chunk_for_evaluation
        )  # TODO: Refactor long line
        logger.info(
            "RuleEvaluator: Subscribed to 'thought_chunk' for behavioral evaluation."
        )  # TODO: Refactor long line

        # Thêm task vòng lặp xử lý đánh giá
        self.add_task(
            self._process_evaluations_loop(), name="rule_evaluation_processor"
        )  # TODO: Refactor long line
        logger.info("RuleEvaluator: Evaluation processing loop started.")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi RuleEvaluator tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "deliberation.request", self._handle_deliberation_request
            )  # TODO: Refactor long line
            self.event_bus.unsubscribe(
                "thought_chunk", self._handle_thought_chunk_for_evaluation
            )  # TODO: Refactor long line
            logger.info("RuleEvaluator: Unsubscribed from topics.")
            await self._evaluation_queue.join()  # Đợi hàng đợi trống
        await super().cleanup()
