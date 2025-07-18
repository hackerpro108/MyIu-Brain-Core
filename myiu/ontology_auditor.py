# myiu/ontology_auditor.py
import asyncio
import logging
import uuid
from typing import TYPE_CHECKING

from myiu.base_module import AsyncModule

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.memory import Memory

logger = logging.getLogger(__name__)


class OntologyAuditor(AsyncModule):
    """
    Kiểm toán viên Hệ Ký ức.
    Định kỳ quét các ký ức cũ và đề xuất các hành động dọn dẹp
    (prune/consolidate) lên cho Hội đồng Nội tâm để xem xét.
    """

    def __init__(
        self,
        event_bus: "EventBus",
        memory: "Memory",
        audit_interval_hours: int = 24,  # TODO: Refactor long line
    ):  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus
        self.memory = memory
        self.audit_interval_sec = audit_interval_hours * 3600
        self.memory_age_threshold_days = 30  # Ký ức cũ hơn 30 ngày sẽ được xem xét  # TODO: Refactor long line  # TODO: Refactor long line

        logger.info("OntologyAuditor: Initialized.")

    async def _setup_async_tasks(self):
        """Khởi tạo vòng lặp kiểm toán định kỳ."""
        self.add_task(self._start_auditing_loop())

    async def _start_auditing_loop(self):
        """Vòng lặp chính, chạy kiểm toán theo chu kỳ."""
        while self._running:
            logger.info("OntologyAuditor: Starting periodic memory audit...")
            await self._perform_memory_audit()
            logger.info(
                f"OntologyAuditor: Memory audit finished. Next run in {self.audit_interval_sec / 3600} hours."  # TODO: Refactor long line
            )  # TODO: Refactor long line
            await asyncio.sleep(self.audit_interval_sec)

    async def _perform_memory_audit(self):
        """
        Thực hiện quy trình kiểm toán: lấy ký ức cũ và tạo đề xuất.
        """
        try:
            old_memories = await self.memory.retrieve_memories_older_than(
                days=self.memory_age_threshold_days,
                limit=100,  # Xử lý 100 ký ức mỗi lần để tránh quá tải
            )

            if not old_memories:
                logger.info(
                    "OntologyAuditor: No old memories found meeting the criteria."  # TODO: Refactor long line
                )  # TODO: Refactor long line
                return

            logger.info(
                f"OntologyAuditor: Found {len(old_memories)} old memories to propose for pruning."  # TODO: Refactor long line
            )  # TODO: Refactor long line

            for mem in old_memories:
                # Không tự ý hành động. Tạo đề xuất để Hội đồng quyết định.
                proposal = {
                    "deliberation_id": str(uuid.uuid4()),
                    "intent": "memory_management_proposal",
                    "topic": f"Proposal to prune memory ID {mem['id']}",
                    "details": {
                        "action": "prune",
                        "memory_id": mem["id"],
                        "memory_content": mem["content"],
                        "memory_timestamp": mem["timestamp"].isoformat(),
                        "reason": f"Memory is older than {self.memory_age_threshold_days} days.",  # TODO: Refactor long line  # TODO: Refactor long line
                    },
                }
                await self.event_bus.publish("DELIBERATION_REQUEST", proposal)

        except Exception as e:
            logger.error(
                f"OntologyAuditor: An error occurred during memory audit: {e}",
                exc_info=True,
            )  # TODO: Refactor long line
