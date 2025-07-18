# myiu/ontology_cache.py
import asyncio
import logging
from typing import Dict, Any, Optional, Set, List, TYPE_CHECKING
from datetime import datetime

from myiu.base_module import AsyncModule

if TYPE_CHECKING:
    from myiu.event_bus import EventBus


logger = logging.getLogger(__name__)


class OntologyCache(AsyncModule):
    """
    Module này quản lý bộ nhớ đệm cho bản thể luận (ontology) của MyIu.
    Nó lưu trữ các khái niệm, mối quan hệ và định nghĩa nội tại của MyIu
để truy cập nhanh chóng và hiệu quả. Nó cũng tự động phát hiện khái niệm mới.  # TODO: Refactor long line
    """

    def __init__(self, event_bus: "EventBus"):  # Nhận EventBus
        super().__init__()
        self.is_background_service = (
            True  # Module này sẽ chạy nền để theo dõi và phát hiện khái niệm
        )
        self.event_bus = event_bus
        self.concepts: Dict[str, Dict[str, Any]] = (
            {}
        )  # Lưu trữ các định nghĩa khái niệm
        self.relationships: Dict[str, List[Dict[str, Any]]] = (
            {}
        )  # Lưu trữ các mối quan hệ giữa các khái niệm
        self.known_concepts: Set[str] = (
            set()
        )  # Set các tên khái niệm đã biết để kiểm tra nhanh
        self._new_concept_queue: asyncio.Queue = (
            asyncio.Queue()
        )  # Hàng đợi cho các khái niệm mới được phát hiện

logger.info("OntologyCache: Initialized. Ready to store MyIu's world model.")  # TODO: Refactor long line

    async def add_concept(self, concept_id: str, concept_data: Dict[str, Any]):
        """Thêm hoặc cập nhật một khái niệm vào bộ nhớ đệm."""
        if concept_id in self.concepts:
            logger.warning(
f"OntologyCache: Concept '{concept_id}' already exists. Updating."  # TODO: Refactor long line
            )
        self.concepts[concept_id] = concept_data
        self.known_concepts.add(
            concept_data.get("name", concept_id).lower()
        )  # Thêm tên khái niệm vào set đã biết
        logger.info(
f"OntologyCache: Added/Updated concept: {concept_id} ({concept_data.get('name')})."  # TODO: Refactor long line
        )

    async def get_concept(self, concept_id: str) -> Optional[Dict[str, Any]]:
        """Lấy một khái niệm từ bộ nhớ đệm."""
        return self.concepts.get(concept_id)

async def get_concept_by_name(self, concept_name: str) -> Optional[Dict[str, Any]]:  # TODO: Refactor long line
        """Lấy một khái niệm từ bộ nhớ đệm bằng tên của nó."""
        for concept_data in self.concepts.values():
            if concept_data.get("name", "").lower() == concept_name.lower():
                return concept_data
        return None

    async def add_relationship(
        self,
        source_id: str,
        relationship_type: str,
        target_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """Thiết lập một mối quan hệ giữa hai khái niệm."""
        if source_id not in self.concepts or target_id not in self.concepts:
            logger.warning(
f"OntologyCache: Cannot add relationship. Source '{source_id}' or target '{target_id}' concept not found."  # TODO: Refactor long line
            )
            return

        rel_data = {
            "type": relationship_type,
            "target": target_id,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.relationships.setdefault(source_id, []).append(rel_data)
        logger.info(
f"OntologyCache: Established relationship '{relationship_type}' from '{source_id}' to '{target_id}'."  # TODO: Refactor long line
        )

    async def get_relationships(self, concept_id: str) -> List[Dict[str, Any]]:
        """Lấy tất cả các mối quan hệ của một khái niệm."""
        return self.relationships.get(concept_id, [])

    async def get_new_concept_for_definition(self) -> Optional[str]:
        """
Trả về một khái niệm mới được phát hiện cần được định nghĩa bởi OntologyMutator.  # TODO: Refactor long line
        """
        try:
            return self._new_concept_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    async def _handle_thought_chunk(self, message: Dict[str, Any]):
        """
Lắng nghe các ThoughtChunk và tự động phát hiện các khái niệm mới từ nội dung.  # TODO: Refactor long line
        (Phần "Bộ Thu hoạch Tri thức Tiềm ẩn")
        """
        from myiu.models import ThoughtChunkModel  # Import cục bộ

        try:
            thought_chunk = ThoughtChunkModel(**message)
            text_content = thought_chunk.content

# Phân tích nội dung để phát hiện khái niệm mới (mô phỏng NLP đơn giản)  # TODO: Refactor long line
            words = set(
                word.lower().strip(".,!?;:'\"").replace("_", " ")
                for word in text_content.split()
            )

            for word in words:
# Điều chỉnh logic phát hiện khái niệm để tránh từ dừng và từ quá chung chung  # TODO: Refactor long line
                if (
                    len(word) > 3
                    and word.isalpha()
                    and word not in self.known_concepts
                    and word
                    not in [
                        "the",
                        "a",
                        "an",
                        "is",
                        "of",
                        "to",
                        "in",
                        "it",
                        "that",
                        "myiu",
                        "this",
                        "là",
                        "và",
                        "của",
                        "những",
                        "đã",
                        "đang",
                        "sẽ",
                        "được",
                        "bị",
                        "là",
                        "không",
                        "rất",
                        "quá",
                        "như",
                        "vậy",
                        "mà",
                        "khi",
                        "tôi",
                    ]
                ):

                    self.known_concepts.add(word)
                    await self._new_concept_queue.put(word)
                    logger.info(
f"OntologyCache: Implicitly harvested new concept '{word}' from ThoughtChunk {thought_chunk.id}."  # TODO: Refactor long line
                    )
# Có thể publish một ThoughtChunk về việc phát hiện khái niệm mới nếu muốn  # TODO: Refactor long line

        except Exception as e:
            logger.error(
f"OntologyCache: Error processing thought chunk for new concept detection: {e}",  # TODO: Refactor long line
                exc_info=True,
            )

    async def _setup_async_tasks(self):
        """Thiết lập các tác vụ bất đồng bộ cho OntologyCache."""
        # Lắng nghe các ThoughtChunk để phát hiện các khái niệm mới
        self.event_bus.subscribe("thought_chunk", self._handle_thought_chunk)
        logger.info(
"OntologyCache: Subscribed to 'thought_chunk' for new concept detection."  # TODO: Refactor long line
        )

    async def cleanup(self):
        """Dọn dẹp tài nguyên khi OntologyCache tắt."""
        if self._running:
self.event_bus.unsubscribe("thought_chunk", self._handle_thought_chunk)  # TODO: Refactor long line
            logger.info("OntologyCache: Unsubscribed from 'thought_chunk'.")
        await super().cleanup()
