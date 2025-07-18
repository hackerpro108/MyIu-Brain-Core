# myiu/consensus_engine.py

import logging
from myiu.base_module import AsyncModule
from myiu.event_bus import EventBus
from myiu.models import (
    ThoughtChunkModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Đảm bảo ThoughtChunkModel, ThoughtIntent, ThoughtSentiment được import  # TODO: Refactor long line  # TODO: Refactor long line
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConsensusEngine(AsyncModule):
    def __init__(
        self, event_bus: EventBus
    ):  # Đảm bảo EventBus được tiêm phụ thuộc  # TODO: Refactor long line
        super().__init__()
        self.event_bus = event_bus
        self.deliberation_requests = (
            {}
)  # Dictionary để lưu trữ các yêu cầu tranh luận đang chờ xử lý  # TODO: Refactor long line  # TODO: Refactor long line
        logger.info("ConsensusEngine: Initialized as the 'Council Chairman'.")

    async def _subscribe_to_deliberation_requests(self):
        """
Lắng nghe các yêu cầu tranh luận (DELIBERATION_REQUEST) từ ReflectionEngine  # TODO: Refactor long line  # TODO: Refactor long line
        và các ý kiến từ các thành viên khác của Hội đồng.
        """
        logger.info(
"ConsensusEngine: Subscribing to deliberation requests and opinions..."  # TODO: Refactor long line
        )  # TODO: Refactor long line

        # Đăng ký lắng nghe DELIBERATION_REQUEST từ ReflectionEngine
        # Giả định topic cho yêu cầu này là 'deliberation.request'
        self.event_bus.subscribe(
            "deliberation.request", self._handle_deliberation_request
        )  # TODO: Refactor long line

        # Đăng ký lắng nghe các ý kiến từ các thành viên Hội đồng
        # Giả định topic cho ý kiến đạo đức là 'opinion.moral'
        self.event_bus.subscribe("opinion.moral", self._handle_moral_opinion)

        # Giả định topic cho ý kiến triết học là 'opinion.principle'
        self.event_bus.subscribe(
            "opinion.principle", self._handle_principle_opinion
        )  # TODO: Refactor long line

        # Thêm các đăng ký cho các loại ý kiến khác khi phát triển Hội đồng

        logger.info("ConsensusEngine: Subscriptions active.")

    async def _handle_deliberation_request(self, message: Dict[str, Any]):
        """
Xử lý yêu cầu tranh luận mới, lưu trữ nó và thông báo cho các thành viên Hội đồng.  # TODO: Refactor long line  # TODO: Refactor long line
        """
        request_id = message.get("request_id")
        problem_description = message.get("problem_description")
        initiator = message.get("initiator", "Unknown")

        if not request_id or not problem_description:
            logger.warning(
f"ConsensusEngine: Invalid deliberation request received: {message}"  # TODO: Refactor long line
            )  # TODO: Refactor long line
            return

        logger.info(
f"ConsensusEngine: Received DELIBERATION_REQUEST (ID: {request_id}) from {initiator} for: {problem_description[:50]}..."  # TODO: Refactor long line
        )  # TODO: Refactor long line

        # Lưu trữ yêu cầu và các ý kiến liên quan
        self.deliberation_requests[request_id] = {
            "problem_description": problem_description,
            "initiator": initiator,
            "opinions": {},  # Chứa các ý kiến từ các thành viên
            "status": "pending",
            "timestamp": message.get("timestamp"),
        }

        # Phát sóng yêu cầu này lại để các thành viên Hội đồng khác lắng nghe
# Chúng ta sẽ sử dụng một topic riêng để các thành viên biết đây là lời mời "tranh luận"  # TODO: Refactor long line  # TODO: Refactor long line
        await self.event_bus.publish(
            "council.deliberate",
            {
                "request_id": request_id,
                "problem_description": problem_description,
                "context": message.get("context", {}),  # Thêm ngữ cảnh nếu có
            },
        )
        logger.info(
f"ConsensusEngine: Broadcast DELIBERATION_REQUEST (ID: {request_id}) to council members."  # TODO: Refactor long line
        )  # TODO: Refactor long line

    async def _handle_moral_opinion(self, message: Dict[str, Any]):
        """
        Xử lý ý kiến đạo đức từ MoralSimulator.
        """
        request_id = message.get("request_id")
        opinion_content = message.get("opinion_content")
        confidence = message.get("confidence", 0.5)

        if request_id in self.deliberation_requests:
self.deliberation_requests[request_id]["opinions"]["moral_simulator"] = (  # TODO: Refactor long line
                {  # TODO: Refactor long line
                    "content": opinion_content,
                    "confidence": confidence,
                }
            )
            logger.info(
f"ConsensusEngine: Received MORAL_OPINION for ID: {request_id}. Content: {opinion_content[:50]}..."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await self._check_for_consensus(request_id)
        else:
            logger.warning(
f"ConsensusEngine: Received MORAL_OPINION for unknown request ID: {request_id}"  # TODO: Refactor long line
            )  # TODO: Refactor long line

    async def _handle_principle_opinion(self, message: Dict[str, Any]):
        """
        Xử lý ý kiến triết học từ LawSynthesizer.
        """
        request_id = message.get("request_id")
        opinion_content = message.get("opinion_content")
        confidence = message.get("confidence", 0.5)

        if request_id in self.deliberation_requests:
self.deliberation_requests[request_id]["opinions"]["law_synthesizer"] = (  # TODO: Refactor long line
                {  # TODO: Refactor long line
                    "content": opinion_content,
                    "confidence": confidence,
                }
            )
            logger.info(
f"ConsensusEngine: Received PRINCIPLE_OPINION for ID: {request_id}. Content: {opinion_content[:50]}..."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await self._check_for_consensus(request_id)
        else:
            logger.warning(
f"ConsensusEngine: Received PRINCIPLE_OPINION for unknown request ID: {request_id}"  # TODO: Refactor long line
            )  # TODO: Refactor long line

    async def _check_for_consensus(self, request_id: str):
        """
        Kiểm tra xem đã đủ ý kiến để tổng hợp ThoughtChunk chưa.
Đây là logic cơ bản. Có thể nâng cấp với timeout hoặc số lượng ý kiến tối thiểu.  # TODO: Refactor long line  # TODO: Refactor long line
        """
        request_data = self.deliberation_requests.get(request_id)
        if not request_data or request_data["status"] == "completed":
            return

        # Ví dụ: Giả định cần cả ý kiến đạo đức và triết học để tổng hợp
        if (
            "moral_simulator" in request_data["opinions"]
            and "law_synthesizer" in request_data["opinions"]
        ):

            logger.info(
f"ConsensusEngine: Enough opinions collected for ID: {request_id}. Synthesizing ThoughtChunk..."  # TODO: Refactor long line
            )  # TODO: Refactor long line

            # Tổng hợp ThoughtChunk cuối cùng
            moral_opinion = request_data["opinions"]["moral_simulator"]
            principle_opinion = request_data["opinions"]["law_synthesizer"]

# Logic tổng hợp đơn giản, có thể phát triển thành trọng số động, xử lý mâu thuẫn phức tạp  # TODO: Refactor long line  # TODO: Refactor long line
            summary_content = (
f"Phản tư sâu về vấn đề: {request_data['problem_description']}\n"  # TODO: Refactor long line  # TODO: Refactor long line
f" - Góc nhìn Đạo đức (Confidence: {moral_opinion['confidence']:.2f}): {moral_opinion['content']}\n"  # TODO: Refactor long line  # TODO: Refactor long line
f" - Góc nhìn Triết học (Confidence: {principle_opinion['confidence']:.2f}): {principle_opinion['content']}\n"  # TODO: Refactor long line  # TODO: Refactor long line
f"Kết luận Hội đồng: Đây là một vấn đề phức tạp đòi hỏi sự cân bằng."  # Cần logic phức tạp hơn  # TODO: Refactor long line  # TODO: Refactor long line
            )

            # Tạo ThoughtChunk
            thought_chunk = ThoughtChunkModel(
                id=f"THOUGHT-COUNCIL-{request_id}",
                timestamp=(
                    request_data["timestamp"]
                    if request_data["timestamp"]
                    else self.event_bus.get_current_timestamp()
                ),  # TODO: Refactor long line
                content=summary_content,
                source="ConsensusEngine",
intent=ThoughtIntent.REFLECTIVE_DELIBERATION,  # Hoặc một intent mới như ThoughtIntent.COUNCIL_DECISION  # TODO: Refactor long line  # TODO: Refactor long line
sentiment=ThoughtSentiment.NEUTRAL,  # Cần tính toán sentiment tổng hợp  # TODO: Refactor long line  # TODO: Refactor long line
                related_thoughts=[
                    f"DELIBERATION-REQUEST-{request_id}"
                ],  # Liên kết với yêu cầu gốc  # TODO: Refactor long line
            )

            # Publish ThoughtChunk lên EventBus
            await self.event_bus.publish(
                "thought_chunk", thought_chunk.model_dump_json()
            )  # TODO: Refactor long line

            request_data["status"] = "completed"
            logger.info(
f"ConsensusEngine: Published final ThoughtChunk for ID: {request_id}."  # TODO: Refactor long line
            )  # TODO: Refactor long line
        # else:
#     logger.debug(f"ConsensusEngine: Not enough opinions yet for ID: {request_id}.")  # TODO: Refactor long line  # TODO: Refactor long line

    async def initialize_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho ConsensusEngine."""
        await self._setup_async_tasks()

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho module này."""
        # Gọi phương thức đăng ký lắng nghe
        self.add_task(self._subscribe_to_deliberation_requests())

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi ConsensusEngine tắt."""
        logger.info(
            "ConsensusEngine: Shutting down and unsubscribing from topics."
        )  # TODO: Refactor long line
        self.event_bus.unsubscribe(
            "deliberation.request", self._handle_deliberation_request
        )  # TODO: Refactor long line
        self.event_bus.unsubscribe("opinion.moral", self._handle_moral_opinion)
        self.event_bus.unsubscribe(
            "opinion.principle", self._handle_principle_opinion
        )  # TODO: Refactor long line
        # Hủy đăng ký tất cả các subscription khác nếu có
