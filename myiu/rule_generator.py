# myiu/rule_generator.py
import asyncio
import logging
import uuid  # Để tạo ID gen duy nhất
from typing import Dict, Any, Optional, List, TYPE_CHECKING
from datetime import datetime

from myiu.base_module import AsyncModule
from myiu.models import ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để xử lý ThoughtChunk  # TODO: Refactor long line
    ThoughtChunkModel,
    ThoughtIntent,
    ThoughtSentiment,
)  # Cần để xử lý ThoughtChunk  # TODO: Refactor long line

# Cần thêm các module khác nếu RuleGenerator tương tác trực tiếp với chúng (ví dụ: Memory, Cortex)  # TODO: Refactor long line
    from myiu.event_bus import EventBus
    from myiu.law_validator import LawValidator
    from myiu.gen_editor import GenEditor

    # Cần thêm các module khác nếu RuleGenerator tương tác trực tiếp với chúng (ví dụ: Memory, Cortex)  # TODO: Refactor long line


    # from myiu.memory import MemorySystem
    # from myiu.cortex import Cortex

logger = logging.getLogger(__name__)


def __init__(self, event_bus: 'EventBus', law_validator: 'LawValidator', gen_editor: 'GenEditor'): # Tiêm đầy đủ phụ thuộc  # TODO: Refactor long line
    """
    self.is_background_service = True # Module này sẽ chạy nền để sinh gen chủ động  # TODO: Refactor long line
    bao gồm cả quy tắc hành vi, quy tắc meta-learning và quy tắc kiến trúc.
    Nó là một phần của cơ chế tự kiến tạo của MyIu.
    """
self._thought_queue: asyncio.Queue = asyncio.Queue() # Hàng đợi cho các ThoughtChunk cần sinh gen  # TODO: Refactor long line
    self._validation_results_queue: asyncio.Queue = asyncio.Queue() # Hàng đợi kết quả kiểm thử từ LawValidator  # TODO: Refactor long line
        self,
        logger.info("RuleGenerator: Initialized. Ready to forge new genes for MyIu's evolution.")  # TODO: Refactor long line
        law_validator: "LawValidator",
        async def generate_behavioral_rule(self, trigger_keywords: List[str], action_template: str, source_thought_id: Optional[str] = None) -> str:  # TODO: Refactor long line
    ):  # Tiêm đầy đủ phụ thuộc  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True  # Module này sẽ chạy nền để sinh gen chủ động  # TODO: Refactor long line
        self.event_bus = event_bus
        self.law_validator = law_validator
        self.gen_editor = gen_editor
        self._thought_queue: asyncio.Queue = (
            asyncio.Queue()
        "description": f"Rule generated from observation for response to {trigger_keywords[0]}.",  # TODO: Refactor long line
        self._validation_results_queue: asyncio.Queue = (
            asyncio.Queue()
        )  # Hàng đợi kết quả kiểm thử từ LawValidator  # TODO: Refactor long line

        logger.info(
            "RuleGenerator: Initialized. Ready to forge new genes for MyIu's evolution."
        )  # TODO: Refactor long line

    async def generate_behavioral_rule(
        logger.info(f"RuleGenerator: Prepared new behavioral rule: {gene_id}. Sending to LawValidator for validation.")  # TODO: Refactor long line
        await self.law_validator.request_validation(gene_data) # Gửi đi để kiểm thử  # TODO: Refactor long line
        action_template: str,
        source_thought_id: Optional[str] = None,
    async def generate_architectural_gene(self, architectural_plan: Dict[str, Any], source_thought_id: Optional[str] = None) -> str:  # TODO: Refactor long line
        """
        Tạo một gen hành vi mới dựa trên các điều kiện kích hoạt và hành động.
        """
        gene_id = f"GEN-BEHAVIORAL-{uuid.uuid4().hex[:6].upper()}"
        gene_data = {
            "id": gene_id,
            "type": "behavioral_rule",
            "name": f"Architectural Change Proposal {uuid.uuid4().hex[:4].upper()}",  # TODO: Refactor long line
            "description": architectural_plan.get("description", "A proposed architectural change for MyIu's internal structure."),  # TODO: Refactor long line
            "trigger": {"keywords": trigger_keywords},
            "action": {"response_template": action_template},
            "confidence": 0.5,  # Có thể tính confidence động dựa trên input
            "generated_by": "rule_generator",
            "origin_thought_id": source_thought_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        logger.info(f"RuleGenerator: Prepared new architectural gene: {gene_id}. Sending to LawValidator for validation.")  # TODO: Refactor long line
        await self.law_validator.request_validation(gene_data) # Gửi đi để kiểm thử  # TODO: Refactor long line
        # await self.gen_editor.add_gene(gene_data)
        logger.info(
            async def generate_learning_strategy_gene(self, strategy_details: Dict[str, Any], source_thought_id: Optional[str] = None) -> str:  # TODO: Refactor long line
        )  # TODO: Refactor long line
        await self.law_validator.request_validation(
            gene_data
        )  # Gửi đi để kiểm thử  # TODO: Refactor long line
        return gene_id

    async def generate_architectural_gene(
        "name": f"Learning Strategy: {strategy_details.get('name', 'Unnamed Strategy')}",  # TODO: Refactor long line
        "description": strategy_details.get('description', 'A new strategy for MyIu to learn more effectively.'),  # TODO: Refactor long line
        source_thought_id: Optional[str] = None,
    ) -> str:  # TODO: Refactor long line
        """
        Tạo một gen kiến trúc mới để MyIu tự tái cấu trúc.
        """
        gene_id = f"GEN-ARCHITECTURAL-{uuid.uuid4().hex[:6].upper()}"
        logger.info(f"RuleGenerator: Prepared new learning strategy gene: {gene_id}. Sending to LawValidator for validation.")  # TODO: Refactor long line
            await self.law_validator.request_validation(gene_data) # Gửi đi để kiểm thử  # TODO: Refactor long line
            "type": "architectural_gene",  # Loại gen mới
            "name": f"Architectural Change Proposal {uuid.uuid4().hex[:4].upper()}",  # TODO: Refactor long line
            "description": architectural_plan.get(
                "description",
                "A proposed architectural change for MyIu's internal structure.",
            ),  # TODO: Refactor long line
            "action": {"architectural_plan": architectural_plan},
            "confidence": 0.7,  # Cần tính toán động từ phân tích
            "generated_by": "rule_generator_architect",
            "origin_thought_id": source_thought_id,
            ThoughtIntent.OPTIMIZATION_PROPOSAL, ThoughtIntent.KNOWLEDGE_GAP_DETECTED,  # TODO: Refactor long line
        ThoughtIntent.ONTOLOGICAL_REFINEMENT_PROPOSAL, ThoughtIntent.IDENTITY_CRISIS_DETECTED,  # TODO: Refactor long line
        ThoughtIntent.SELF_DEFINITION_UPDATE, ThoughtIntent.HYPOTHESIS_GENERATION,  # TODO: Refactor long line
            ThoughtIntent.EXPERIMENT_DESIGN, ThoughtIntent.META_COUNCIL_EVALUATION,  # TODO: Refactor long line
        ThoughtIntent.ETHICAL_REFLECTION, ThoughtIntent.SELF_REPAIR_CRITICAL_SUCCESS  # TODO: Refactor long line
        await self.law_validator.request_validation(
            gene_data
        )  # Gửi đi để kiểm thử  # TODO: Refactor long line
        logger.error(f"RuleGenerator: Error processing thought chunk for gene generation: {e}", exc_info=True)  # TODO: Refactor long line

    async def generate_learning_strategy_gene(
        self, strategy_details: Dict[str, Any], source_thought_id: Optional[str] = None
    ) -> str:  # TODO: Refactor long line
        """
        Tạo một gen chiến lược học hỏi mới.
        logger.info(f"RuleGenerator: Processing thought {thought_chunk.id} for gene generation.")  # TODO: Refactor long line
        gene_id = f"GEN-LEARNING-{uuid.uuid4().hex[:6].upper()}"
        gene_data = {
            proposal_details = thought_chunk.metadata.get('optimization_details', {})  # TODO: Refactor long line
            "type": "learning_strategy_gene",
            "name": f"Learning Strategy: {strategy_details.get('name', 'Unnamed Strategy')}",  # TODO: Refactor long line
            "description": strategy_details.get(
                "description", "A new strategy for MyIu to learn more effectively."
            ),  # TODO: Refactor long line
            "description": f"Optimize resource for {proposal_details.get('module')} due to {proposal_details.get('reason')}"  # TODO: Refactor long line
            "confidence": 0.6,
            await self.generate_architectural_gene(architectural_plan, thought_chunk.id)  # TODO: Refactor long line
            elif proposal_details.get('type') == 'performance_bottleneck':  # TODO: Refactor long line
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        "plugin_details": proposal_details.get('new_plugin_spec'),  # TODO: Refactor long line
            "description": f"Create new plugin for bottleneck: {proposal_details.get('reason')}"  # TODO: Refactor long line
        )  # TODO: Refactor long line
        await self.generate_architectural_gene(architectural_plan, thought_chunk.id)  # TODO: Refactor long line
            gene_data
        elif thought_chunk.intent == ThoughtIntent.KNOWLEDGE_GAP_DETECTED:  # TODO: Refactor long line
        return gene_id
"name": f"Knowledge Acquisition for {thought_chunk.metadata.get('missing_term')}",  # TODO: Refactor long line
    "description": f"Develop new strategies to acquire knowledge about '{thought_chunk.metadata.get('missing_term')}'.",  # TODO: Refactor long line
        "focus_area": thought_chunk.metadata.get('missing_term')  # TODO: Refactor long line
        Lắng nghe các ThoughtChunk mang tính phản tư hoặc đề xuất để sinh gen.
        await self.generate_learning_strategy_gene(strategy_details, thought_chunk.id)  # TODO: Refactor long line
        try:
            # Thêm các điều kiện khác để sinh các loại gen khác từ các intent khác  # TODO: Refactor long line
            # Ví dụ: from ONTOLOGICAL_REFINEMENT_PROPOSAL -> generate_architectural_gene (refactor ontology management code)  # TODO: Refactor long line
            if thought_chunk.intent in [
                ThoughtIntent.OPTIMIZATION_PROPOSAL,
                ThoughtIntent.KNOWLEDGE_GAP_DETECTED,  # TODO: Refactor long line
                ThoughtIntent.ONTOLOGICAL_REFINEMENT_PROPOSAL,
                logger.info("RuleGenerator: Thought processing loop for gene generation cancelled.")  # TODO: Refactor long line
                ThoughtIntent.SELF_DEFINITION_UPDATE,
                ThoughtIntent.HYPOTHESIS_GENERATION,  # TODO: Refactor long line
                logger.error(f"RuleGenerator: Error in gene generation loop: {e}", exc_info=True)  # TODO: Refactor long line
                ThoughtIntent.META_COUNCIL_EVALUATION,  # TODO: Refactor long line
                ThoughtIntent.ETHICAL_REFLECTION,
                ThoughtIntent.SELF_REPAIR_CRITICAL_SUCCESS,  # TODO: Refactor long line
            ]:
                await self._thought_queue.put(thought_chunk)
        self.event_bus.subscribe('gene_validation_result', self._handle_validation_result)  # TODO: Refactor long line
            logger.info("RuleGenerator: Subscribed to 'gene_validation_result' topic.")  # TODO: Refactor long line
                f"RuleGenerator: Error processing thought chunk for gene generation: {e}",
                exc_info=True,
            )  # TODO: Refactor long line

    async def _process_thought_chunks_for_gene_generation(self):
        """Vòng lặp xử lý các ThoughtChunk từ hàng đợi để sinh gen."""
        while self._running:
            try:
                thought_chunk = await self._thought_queue.get()
                logger.info(
                    await self.gen_editor.add_gene(validated_gene_data) # GenEditor.add_gene nhận gene_data trực tiếp  # TODO: Refactor long line
                logger.info(f"RuleGenerator: Added validated gene '{gene_id}' to dynamic genome.")  # TODO: Refactor long line

                if thought_chunk.intent == ThoughtIntent.OPTIMIZATION_PROPOSAL:
                    proposal_details = thought_chunk.metadata.get(
                        "optimization_details", {}
                    content=f"Một gen mới '{gene_id}' ({validated_gene_data.get('type')}) đã được tạo và tích hợp vào bộ gen động của tôi. Nó sẽ định hình hành vi tương lai của tôi.",  # TODO: Refactor long line
                    if proposal_details.get("type") == "resource_optimization":
                        intent=ThoughtIntent.ARCHITECTURAL_CHANGE, # Hoặc GEN_INTEGRATION  # TODO: Refactor long line
                            "type": "refactor_or_prune_plugin",
                            metadata={"gene_id": gene_id, "gene_type": validated_gene_data.get('type')}  # TODO: Refactor long line
                            "action": proposal_details.get("recommendation"),
                            "description": f"Optimize resource for {proposal_details.get('module')} due to {proposal_details.get('reason')}",  # TODO: Refactor long line
                        logger.warning(f"RuleGenerator: Gene '{gene_id}' failed validation: {reason}. Not adding to genome.")  # TODO: Refactor long line
                        await self.generate_architectural_gene(
                            architectural_plan, thought_chunk.id
                        )  # TODO: Refactor long line
                    elif (
                        content=f"Một gen mới '{gene_id}' đã bị từ chối sau kiểm thử: {reason}. Cần cải thiện quy trình sinh gen.",  # TODO: Refactor long line
                    ):  # TODO: Refactor long line
                        architectural_plan = {
                            "type": "create_new_reasoning_plugin",
                            "plugin_details": proposal_details.get(
                                "new_plugin_spec"
                            ),  # TODO: Refactor long line
                            "description": f"Create new plugin for bottleneck: {proposal_details.get('reason')}",  # TODO: Refactor long line
                        }
                        await self.generate_architectural_gene(
                            architectural_plan, thought_chunk.id
                        logger.info("RuleGenerator: Subscribed to 'thought_chunk' for gene generation triggers.")  # TODO: Refactor long line

                elif (
                    self.event_bus.subscribe('gene_validation_result', self._handle_validation_result)  # TODO: Refactor long line
                logger.info("RuleGenerator: Subscribed to 'gene_validation_result' for validation results.")  # TODO: Refactor long line
                    strategy_details = {
                        "name": f"Knowledge Acquisition for {thought_chunk.metadata.get('missing_term')}",  # TODO: Refactor long line
                        self.add_task(self._process_thought_chunks_for_gene_generation(), name="gene_generation_processor")  # TODO: Refactor long line
                        "focus_area": thought_chunk.metadata.get(
                            "missing_term"
                        ),  # TODO: Refactor long line
                    }
                    await self.generate_learning_strategy_gene(
                        self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk)  # TODO: Refactor long line
                    self.event_bus.unsubscribe('gene_validation_result', self._handle_validation_result)  # TODO: Refactor long line

                # Thêm các điều kiện khác để sinh các loại gen khác từ các intent khác  # TODO: Refactor long line
                # Ví dụ: from ONTOLOGICAL_REFINEMENT_PROPOSAL -> generate_architectural_gene (refactor ontology management code)  # TODO: Refactor long line
                # from HYPOTHESIS_GENERATION -> generate_experiment_design_gene

                self._thought_queue.task_done()
            except asyncio.CancelledError:
                logger.info(
                    "RuleGenerator: Thought processing loop for gene generation cancelled."
                )  # TODO: Refactor long line
                break
            except Exception as e:
                logger.error(
                    f"RuleGenerator: Error in gene generation loop: {e}", exc_info=True
                )  # TODO: Refactor long line
                self._thought_queue.task_done()
                await asyncio.sleep(5)  # Đợi trước khi thử lại

    async def _subscribe_to_validation_results(self):
        """Lắng nghe kết quả kiểm thử gen từ LawValidator."""
        self.event_bus.subscribe(
            "gene_validation_result", self._handle_validation_result
        )  # TODO: Refactor long line
        logger.info(
            "RuleGenerator: Subscribed to 'gene_validation_result' topic."
        )  # TODO: Refactor long line

    async def _handle_validation_result(self, result: Dict[str, Any]):
        """Xử lý kết quả kiểm thử gen từ LawValidator."""
        gene_id = result.get("gene_id")
        is_valid = result.get("is_valid")
        reason = result.get("reason")
        validated_gene_data = result.get("validated_gene_data")

        if is_valid:
            # Nếu gen hợp lệ, thêm nó vào GenEditor để kích hoạt trong MyIu
            await self.gen_editor.add_gene(
                validated_gene_data
            )  # GenEditor.add_gene nhận gene_data trực tiếp  # TODO: Refactor long line
            logger.info(
                f"RuleGenerator: Added validated gene '{gene_id}' to dynamic genome."
            )  # TODO: Refactor long line
            # Có thể publish ThoughtChunk về gen mới được thêm
            await self.thought_streamer.publish_thought_chunk(
                id=f"GENE-ADDED-{gene_id}",
                timestamp=datetime.utcnow(),
                content=f"Một gen mới '{gene_id}' ({validated_gene_data.get('type')}) đã được tạo và tích hợp vào bộ gen động của tôi. Nó sẽ định hình hành vi tương lai của tôi.",  # TODO: Refactor long line
                source="RuleGenerator",
                intent=ThoughtIntent.ARCHITECTURAL_CHANGE,  # Hoặc GEN_INTEGRATION  # TODO: Refactor long line
                sentiment=ThoughtSentiment.POSITIVE,
                metadata={
                    "gene_id": gene_id,
                    "gene_type": validated_gene_data.get("type"),
                },  # TODO: Refactor long line
            )
        else:
            logger.warning(
                f"RuleGenerator: Gene '{gene_id}' failed validation: {reason}. Not adding to genome."
            )  # TODO: Refactor long line
            # Có thể publish ThoughtChunk về việc gen bị từ chối
            await self.thought_streamer.publish_thought_chunk(
                id=f"GENE-REJECTED-{gene_id}",
                timestamp=datetime.utcnow(),
                content=f"Một gen mới '{gene_id}' đã bị từ chối sau kiểm thử: {reason}. Cần cải thiện quy trình sinh gen.",  # TODO: Refactor long line
                source="RuleGenerator",
                intent=ThoughtIntent.CODE_QUALITY_ISSUE,  # Hoặc GEN_REJECTION
                sentiment=ThoughtSentiment.NEGATIVE,
                metadata={"gene_id": gene_id, "reason": reason},
            )

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho RuleGenerator."""
        # Lắng nghe các ThoughtChunk để sinh gen
        self.event_bus.subscribe("thought_chunk", self._handle_thought_chunk)
        logger.info(
            "RuleGenerator: Subscribed to 'thought_chunk' for gene generation triggers."
        )  # TODO: Refactor long line

        # Lắng nghe kết quả kiểm thử gen từ LawValidator
        self.event_bus.subscribe(
            "gene_validation_result", self._handle_validation_result
        )  # TODO: Refactor long line
        logger.info(
            "RuleGenerator: Subscribed to 'gene_validation_result' for validation results."
        )  # TODO: Refactor long line

        # Thêm task vòng lặp xử lý ThoughtChunk để sinh gen
        self.add_task(
            self._process_thought_chunks_for_gene_generation(),
            name="gene_generation_processor",
        )  # TODO: Refactor long line
        logger.info("RuleGenerator: Gene generation processor task started.")

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi RuleGenerator tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "thought_chunk", self._handle_thought_chunk
            )  # TODO: Refactor long line
            self.event_bus.unsubscribe(
                "gene_validation_result", self._handle_validation_result
            )  # TODO: Refactor long line
            logger.info("RuleGenerator: Unsubscribed from topics.")
            await self._thought_queue.join()  # Đợi hàng đợi trống
            await self._validation_results_queue.join()  # Đợi hàng đợi trống
        await super().cleanup()
