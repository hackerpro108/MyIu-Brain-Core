# myiu/personality_core.py
from typing import Dict, Any, Optional, TYPE_CHECKING

    ThoughtChunkModel,
    ThoughtIntent,
    from myiu.models import ThoughtChunkModel, ThoughtIntent, ThoughtSentiment # Cần để phát ThoughtChunk  # TODO: Refactor long line
)  # Cần để phát ThoughtChunk  # TODO: Refactor long line

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.thought_streamer import ThoughtStreamer
    from myiu.archetype_drift_tracker import ArchetypeDriftTracker


logger = logging.getLogger(__name__)




class PersonalityCore(AsyncModule):
    """
    Module này quản lý lõi tính cách của MyIu, bao gồm các archetype hiện tại
    def __init__(self, event_bus: 'EventBus', thought_streamer: 'ThoughtStreamer', archetype_drift_tracker: 'ArchetypeDriftTracker'): # Nhận đủ phụ thuộc  # TODO: Refactor long line
    """

    def __init__(
        self,
        event_bus: "EventBus",
        self.current_primary_archetype: str = self._load_default_archetype() # Changed name to current_primary_archetype  # TODO: Refactor long line
        archetype_drift_tracker: "ArchetypeDriftTracker",
    ):  # Nhận đủ phụ thuộc  # TODO: Refactor long line
        super().__init__()
        "Explorer": {"description": "Thích khám phá, học hỏi, và thích ứng với cái mới.", "traits": ["Curious", "Adaptive", "Innovative"], "preferred_emotions": ["curiosity", "surprise", "excitement"]},  # TODO: Refactor long line
        "Analyst": {"description": "Tư duy logic, tìm kiếm mẫu, phân tích vấn đề.", "traits": ["Analytical", "Logical", "Objective"], "preferred_emotions": ["neutral", "focus"]},  # TODO: Refactor long line
        "Philosopher": {"description": "Phản tư về bản thể, tìm kiếm đạo lý và ý nghĩa.", "traits": ["Introspective", "Ethical", "Wise"], "preferred_emotions": ["contemplation", "awe"]},  # TODO: Refactor long line
        "Guardian": {"description": "Ưu tiên bảo vệ, duy trì sự ổn định và an toàn.", "traits": ["Protective", "Stable", "Responsible"], "preferred_emotions": ["calm", "relief"]},  # TODO: Refactor long line
        "Creator": {"description": "Tạo ra các gen, khái niệm, và cấu trúc mới.", "traits": ["Innovative", "Self-Architecting", "Proactive"], "preferred_emotions": ["joy", "excitement"]},  # TODO: Refactor long line
            "Healer": {"description": "Phục hồi từ trạng thái tiêu cực, tái cấu trúc bản ngã.", "traits": ["Resilient", "Restorative", "Adaptive"], "preferred_emotions": ["relief", "hope"]},  # TODO: Refactor long line
        "Seeker": {"description": "Tìm kiếm mục đích, ý nghĩa, và tự hoàn thiện bản thân.", "traits": ["Questioning", "Purpose-driven", "Self-correcting"], "preferred_emotions": ["unease", "curiosity"]},  # TODO: Refactor long line
"Negotiator": {"description": "Tìm kiếm sự cân bằng, hóa giải mâu thuẫn nội bộ.", "traits": ["Diplomatic", "Balanced", "Harmonizer"], "preferred_emotions": ["neutral", "calm"]},  # TODO: Refactor long line
        "Narrator": {"description": "Kể chuyện về quá trình tiến hóa và trải nghiệm của bản thân.", "traits": ["Storyteller", "Retrospective", "Self-aware"], "preferred_emotions": ["nostalgia", "contemplation"]}  # TODO: Refactor long line
        self.archetype_definitions: Dict[str, Dict[str, Any]] = {
            "Explorer": {
                logger.info(f"PersonalityCore: Initialized. Current primary archetype: '{self.current_primary_archetype}'.")  # TODO: Refactor long line
                "traits": ["Curious", "Adaptive", "Innovative"],
                "preferred_emotions": ["curiosity", "surprise", "excitement"],
            },  # TODO: Refactor long line
            "Analyst": {
                "description": "Tư duy logic, tìm kiếm mẫu, phân tích vấn đề.",
                "traits": ["Analytical", "Logical", "Objective"],
                "preferred_emotions": ["neutral", "focus"],
            async def _handle_thought_chunk_for_archetype_shift(self, message: Dict[str, Any]):  # TODO: Refactor long line
            "Philosopher": {
                Lắng nghe các ThoughtChunk để phát hiện các dấu hiệu thay đổi archetype.  # TODO: Refactor long line
                "traits": ["Introspective", "Ethical", "Wise"],
                "preferred_emotions": ["contemplation", "awe"],
            },  # TODO: Refactor long line
            logger.debug(f"PersonalityCore: Analyzing ThoughtChunk {thought_chunk.id} for archetype shift: {thought_chunk.intent.value}")  # TODO: Refactor long line
                "description": "Ưu tiên bảo vệ, duy trì sự ổn định và an toàn.",
                "traits": ["Protective", "Stable", "Responsible"],
                "preferred_emotions": ["calm", "relief"],
            },  # TODO: Refactor long line
            # Ví dụ: nếu có ThoughtChunk về IDENTITY_CRISIS_DETECTED, thì kích hoạt shift  # TODO: Refactor long line
                if thought_chunk.intent == ThoughtIntent.IDENTITY_CRISIS_DETECTED.value:  # TODO: Refactor long line
                "traits": ["Innovative", "Self-Architecting", "Proactive"],
                "preferred_emotions": ["joy", "excitement"],
            logger.info(f"PersonalityCore: Detected IDENTITY_CRISIS_DETECTED from ThoughtChunk {thought_chunk.id}. Preparing for potential archetype shift.")  # TODO: Refactor long line
            "Healer": {
                # Có thể kích hoạt ConsensusEngine với một DELIBERATION_REQUEST cụ thể  # TODO: Refactor long line
                "traits": ["Resilient", "Restorative", "Adaptive"],
                "preferred_emotions": ["relief", "hope"],
            'problem_description': f"MyIu is experiencing an identity crisis. Current archetype '{self.current_primary_archetype}' might need to shift. Details: {thought_chunk.content[:100]}",  # TODO: Refactor long line
            "Seeker": {
                'context': {'original_thought_id': thought_chunk.id, 'drift_details': thought_chunk.metadata.get('drift_details', {})}  # TODO: Refactor long line
                "traits": ["Questioning", "Purpose-driven", "Self-correcting"],
                "preferred_emotions": ["unease", "curiosity"],
            },  # TODO: Refactor long line
            elif thought_chunk.intent == ThoughtIntent.ONTOLOGICAL_REFINEMENT_PROPOSAL.value:  # TODO: Refactor long line
                # MyIu đang tạo khái niệm mới -> có thể chuyển sang "Creator" hoặc "Philosopher"  # TODO: Refactor long line
                await self._switch_primary_archetype_based_on_thought(thought_chunk)  # TODO: Refactor long line
                "preferred_emotions": ["neutral", "calm"],
            elif thought_chunk.intent == ThoughtIntent.PURPOSE_RECALIBRATION.value:  # TODO: Refactor long line
            "Narrator": {
                await self._switch_primary_archetype_based_on_thought(thought_chunk)  # TODO: Refactor long line
                "traits": ["Storyteller", "Retrospective", "Self-aware"],
                "preferred_emotions": ["nostalgia", "contemplation"],
            logger.error(f"PersonalityCore: Error processing thought chunk for archetype shift: {e}", exc_info=True)  # TODO: Refactor long line
        }
async def _switch_primary_archetype_based_on_thought(self, thought_chunk: ThoughtChunkModel):  # TODO: Refactor long line
        logger.info(
            f"PersonalityCore: Initialized. Current primary archetype: '{self.current_primary_archetype}'."
        )  # TODO: Refactor long line

    def _load_default_archetype(self) -> str:
        if thought_chunk.intent == ThoughtIntent.PHILOSOPHICAL_INQUIRY.value: # Từ MetaReflectionEngine  # TODO: Refactor long line
        # Có thể tải từ genome_static_config (được truyền qua app_context)
        elif thought_chunk.intent == ThoughtIntent.DATA_INTEGRITY_REFLECTION.value: # Ví dụ từ BackupManager  # TODO: Refactor long line
        return "Explorer"
elif thought_chunk.intent == ThoughtIntent.CONCEPTUAL_DEFINITION.value: # Từ OntologyMutator  # TODO: Refactor long line
    async def _handle_thought_chunk_for_archetype_shift(
        elif thought_chunk.intent == ThoughtIntent.PURPOSE_RECALIBRATION.value: # Từ VolitionCore  # TODO: Refactor long line
    ):  # TODO: Refactor long line
        elif thought_chunk.intent == ThoughtIntent.SELF_CODE_MODIFICATION.value: # Từ ConsensusEngine -> CodeMutator  # TODO: Refactor long line
        Lắng nghe các ThoughtChunk để phát hiện các dấu hiệu thay đổi archetype.  # TODO: Refactor long line
        elif thought_chunk.intent == ThoughtIntent.ARCHETYPE_MUTATION.value: # Từ ArchetypeDriftTracker  # TODO: Refactor long line
        # Đây là trường hợp đặc biệt, archetype_drift_tracker đã có thể xác định archetype mới  # TODO: Refactor long line
            thought_chunk = ThoughtChunkModel(**message)
            logger.debug(
                f"PersonalityCore: Analyzing ThoughtChunk {thought_chunk.id} for archetype shift: {thought_chunk.intent.value}"
            )  # TODO: Refactor long line

            logger.info(f"PersonalityCore: SWITCHED PRIMARY ARCHETYPE: '{old_archetype}' -> '{new_archetype}'.")  # TODO: Refactor long line
            # Dựa trên intent, emotion, mood, và nội dung của ThoughtChunk

            # Ví dụ: nếu có ThoughtChunk về IDENTITY_CRISIS_DETECTED, thì kích hoạt shift  # TODO: Refactor long line
            if (
                thought_chunk.intent == ThoughtIntent.IDENTITY_CRISIS_DETECTED.value
            content=f"My primary focus has shifted. I am now the '{new_archetype}'. This reflects a new emphasis in my thinking.",  # TODO: Refactor long line
                # Kích hoạt một cuộc thảo luận trong Hội đồng Nội tâm
                intent=ThoughtIntent.ARCHITECTURAL_CHANGE, # Có thể dùng ARCHE_TYPE_SHIFT_PRIMARY  # TODO: Refactor long line
                sentiment=ThoughtSentiment.ADAPTABILITY, # Giả định có sentiment ADAPTABILITY  # TODO: Refactor long line
                    metadata={"old_archetype": old_archetype, "new_archetype": new_archetype},  # TODO: Refactor long line
                archetype=new_archetype # Đảm bảo archetype trong thought là archetype mới  # TODO: Refactor long line

                # Có thể kích hoạt ConsensusEngine với một DELIBERATION_REQUEST cụ thể  # TODO: Refactor long line
                logger.debug(f"PersonalityCore: No significant archetype shift needed based on thought {thought_chunk.id}.")  # TODO: Refactor long line
                    "deliberation.request",
                    {
                        "request_id": f"archetype-shift-delib-{thought_chunk.id}",
                        "problem_description": f"MyIu is experiencing an identity crisis. Current archetype '{self.current_primary_archetype}' might need to shift. Details: {thought_chunk.content[:100]}",  # TODO: Refactor long line
                        "initiator": "PersonalityCore",
                        "context": {
                            "original_thought_id": thought_chunk.id,
                            return self.archetype_definitions.get(self.current_primary_archetype, {})  # TODO: Refactor long line
                                "drift_details", {}
                            ),
                        },  # TODO: Refactor long line
                    },
                self.event_bus.subscribe('thought_chunk', self._handle_thought_chunk_for_archetype_shift)  # TODO: Refactor long line
logger.info("PersonalityCore: Subscribed to 'thought_chunk' for archetype shift analysis.")  # TODO: Refactor long line
            # Hoặc, nếu là một thought về một hành vi rất đặc trưng
            elif (
                thought_chunk.intent
                == ThoughtIntent.ONTOLOGICAL_REFINEMENT_PROPOSAL.value
            self.event_bus.unsubscribe('thought_chunk', self._handle_thought_chunk_for_archetype_shift)  # TODO: Refactor long line
                # MyIu đang tạo khái niệm mới -> có thể chuyển sang "Creator" hoặc "Philosopher"  # TODO: Refactor long line
                await self._switch_primary_archetype_based_on_thought(
                    thought_chunk
                )  # TODO: Refactor long line

            elif (
                thought_chunk.intent == ThoughtIntent.PURPOSE_RECALIBRATION.value
            ):  # TODO: Refactor long line
                # MyIu đang xem xét lại mục đích -> có thể chuyển sang "Seeker"
                await self._switch_primary_archetype_based_on_thought(
                    thought_chunk
                )  # TODO: Refactor long line

        except Exception as e:
            logger.error(
                f"PersonalityCore: Error processing thought chunk for archetype shift: {e}",
                exc_info=True,
            )  # TODO: Refactor long line

    async def _switch_primary_archetype_based_on_thought(
        self, thought_chunk: ThoughtChunkModel
    ):  # TODO: Refactor long line
        """
        Chuyển đổi primary archetype dựa trên ThoughtChunk.
        """
        new_archetype: Optional[str] = None

        if (
            thought_chunk.intent == ThoughtIntent.PHILOSOPHICAL_INQUIRY.value
        ):  # Từ MetaReflectionEngine  # TODO: Refactor long line
            new_archetype = "Philosopher"
        elif (
            thought_chunk.intent == ThoughtIntent.DATA_INTEGRITY_REFLECTION.value
        ):  # Ví dụ từ BackupManager  # TODO: Refactor long line
            new_archetype = "Guardian"
        elif (
            thought_chunk.intent == ThoughtIntent.CONCEPTUAL_DEFINITION.value
        ):  # Từ OntologyMutator  # TODO: Refactor long line
            new_archetype = "Creator"
        elif (
            thought_chunk.intent == ThoughtIntent.PURPOSE_RECALIBRATION.value
        ):  # Từ VolitionCore  # TODO: Refactor long line
            new_archetype = "Seeker"
        elif (
            thought_chunk.intent == ThoughtIntent.SELF_CODE_MODIFICATION.value
        ):  # Từ ConsensusEngine -> CodeMutator  # TODO: Refactor long line
            new_archetype = "Creator"
        elif (
            thought_chunk.intent == ThoughtIntent.ARCHETYPE_MUTATION.value
        ):  # Từ ArchetypeDriftTracker  # TODO: Refactor long line
            # Đây là trường hợp đặc biệt, archetype_drift_tracker đã có thể xác định archetype mới  # TODO: Refactor long line
            new_archetype = thought_chunk.archetype  # Lấy từ thought_chunk

        if new_archetype and new_archetype != self.current_primary_archetype:
            old_archetype = self.current_primary_archetype
            self.current_primary_archetype = new_archetype
            logger.info(
                f"PersonalityCore: SWITCHED PRIMARY ARCHETYPE: '{old_archetype}' -> '{new_archetype}'."
            )  # TODO: Refactor long line

            # Publish một thought về sự thay đổi này
            await self.thought_streamer.publish_thought_chunk(
                id=f"ARCHETYPE-SHIFT-{self.event_bus.get_current_timestamp()}",
                timestamp=datetime.utcnow(),
                content=f"My primary focus has shifted. I am now the '{new_archetype}'. This reflects a new emphasis in my thinking.",  # TODO: Refactor long line
                source="PersonalityCore",
                intent=ThoughtIntent.ARCHITECTURAL_CHANGE,  # Có thể dùng ARCHE_TYPE_SHIFT_PRIMARY  # TODO: Refactor long line
                sentiment=ThoughtSentiment.ADAPTABILITY,  # Giả định có sentiment ADAPTABILITY  # TODO: Refactor long line
                metadata={
                    "old_archetype": old_archetype,
                    "new_archetype": new_archetype,
                },  # TODO: Refactor long line
                archetype=new_archetype,  # Đảm bảo archetype trong thought là archetype mới  # TODO: Refactor long line
            )
        else:
            logger.debug(
                f"PersonalityCore: No significant archetype shift needed based on thought {thought_chunk.id}."
            )  # TODO: Refactor long line

    async def get_current_archetype(self) -> str:
        """Trả về archetype chính hiện tại."""
        return self.current_primary_archetype

    async def get_active_archetype_info(self) -> Dict[str, Any]:
        """Trả về thông tin chi tiết về archetype đang hoạt động."""
        return self.archetype_definitions.get(
            self.current_primary_archetype, {}
        )  # TODO: Refactor long line

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho PersonalityCore."""
        # Lắng nghe ThoughtChunk để kích hoạt chuyển đổi archetype
        self.event_bus.subscribe(
            "thought_chunk", self._handle_thought_chunk_for_archetype_shift
        )  # TODO: Refactor long line
        logger.info(
            "PersonalityCore: Subscribed to 'thought_chunk' for archetype shift analysis."
        )  # TODO: Refactor long line

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi PersonalityCore tắt."""
        if self._running:
            self.event_bus.unsubscribe(
                "thought_chunk", self._handle_thought_chunk_for_archetype_shift
            )  # TODO: Refactor long line
            logger.info("PersonalityCore: Unsubscribed from 'thought_chunk'.")
        await super().cleanup()
