import chromadb
import networkx as nx
import logging
import json
import hashlib
from pathlib import Path

from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.models import MemoryNode

class Memory(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.journal_logger = None
        self.memory_collection = None
        self.content_fingerprints = set()

    async def start(self):
        await super().start()
        self.log.info("Multi-layered Memory System starting...")
        self._load_config()
        self._setup_journal()
        self._setup_vector_store()
        self.log.info("Multi-layered Memory System is ready.")

    def _load_config(self):
        config = self.app_context.get_service("genome_static_config").get("memory_system_config", {})
        self.log_path = Path(config.get("log_path", "data/memory.log"))
        self.vector_db_path = Path(config.get("vector_db_path", "data/vector_memory"))
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)

    def _setup_journal(self):
        self.journal_logger = logging.getLogger("MyIu.Journal")
        handler = logging.FileHandler(self.log_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        if not self.journal_logger.handlers: self.journal_logger.addHandler(handler)
        self.journal_logger.setLevel(logging.INFO)
        self.journal_logger.propagate = False

    def _setup_vector_store(self):
        client = chromadb.PersistentClient(path=str(self.vector_db_path))
        self.memory_collection = client.get_or_create_collection(name="memory_stream")
        for doc in self.memory_collection.get().get('documents', []):
            self.content_fingerprints.add(hashlib.sha256(doc.encode('utf-8')).hexdigest())
        self.log.info(f"Vector Store connected. Loaded {len(self.content_fingerprints)} fingerprints.")

    def _flatten_metadata(self, data: dict) -> dict:
        return {k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in data.items() if v is not None}

    async def add_memory(self, node: MemoryNode):
        fingerprint = hashlib.sha256(node.content.encode('utf-8')).hexdigest()
        if fingerprint in self.content_fingerprints:
            self.log.info(f"Duplicate memory skipped.")
            return
        self.content_fingerprints.add(fingerprint)
        self.journal_logger.info(node.model_dump_json(indent=2))
        
        if self.memory_collection:
            metadata_for_chroma = self._flatten_metadata(node.model_dump(exclude={'content'}))
            # --- HOÀN THIỆN: Thêm content vào metadata để Historian có thể đọc ---
            metadata_for_chroma['original_content'] = node.content
            
            self.memory_collection.add(
                documents=[node.content],
                metadatas=[metadata_for_chroma],
                ids=[node.id]
            )
        self.log.info(f"New memory recorded (ID: {node.id}).")

    async def search_associative(self, query: str, n_results: int = 5) -> list:
        if not self.memory_collection or self.memory_collection.count() == 0:
            return []
        try:
            results = self.memory_collection.query(query_texts=[query], n_results=n_results)
            # Trả về toàn bộ kết quả, bao gồm cả metadata
            return results.get('metadatas', [[]])[0]
        except Exception as e:
            self.log.error(f"Lỗi khi tìm kiếm trong Vector Store: {e}")
            return []

    async def stop(self):
        await super().stop()
