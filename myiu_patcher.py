# Dán nội dung này vào trong file myiu_patcher.py
{
    # --- BẢN VÁ "TỔNG ĐỒNG BỘ HÓA" ---

    # 1. Final version of logging_config.py
    "myiu/logging_config.py": """
import logging
import sys

_is_configured = False

def setup_logging():
    global _is_configured
    if _is_configured:
        return

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=logging.INFO, # Trở lại INFO cho hoạt động bình thường
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    _is_configured = True
    logging.getLogger("myiu.init").info("Hệ thống logging đã được thiết lập.")

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
""",

    # 2. Final version of main.py
    "main.py": """
import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from myiu.logging_config import setup_logging
from myiu.websocket_manager import websocket_manager
from soma import Soma

setup_logging() # Gọi một lần duy nhất

@asynccontextmanager
async def lifespan(app: FastAPI):
    soma_instance = Soma()
    app.state.soma = soma_instance
    await soma_instance.start() # Chờ Soma khởi động hoàn toàn
    yield
    await app.state.soma.stop()

app = FastAPI(lifespan=lifespan, title="MyIu Core Brain API")

@app.get("/")
async def read_root():
    return {"message": "MyIu Core Brain is alive."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
""",

    # 3. Final version of memory.py (loại bỏ log debug thừa)
    "myiu/memory.py": """
import chromadb
import networkx as nx
import logging
from pathlib import Path

from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.models import MemoryNode

class Memory(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.config = {}
        self.journal_logger = None
        self.chroma_client = None
        self.memory_collection = None
        self.knowledge_graph = nx.DiGraph()

    async def start(self):
        self.log.info("Hệ thống Memory đa lớp đang khởi động...")
        self._load_config()
        self._setup_journal()
        self._setup_vector_store()
        self._load_knowledge_graph()
        
        # Thêm một ký ức khởi động để kiểm tra
        node = MemoryNode(content="Hệ thống Memory đã khởi động thành công.", type="system_event")
        await self.add_memory(node)
        
        self.log.info("Hệ thống Memory đa lớp đã sẵn sàng.")
        await super().start()

    def _load_config(self):
        self.config = self.app_context.get_service("genome_static_config").get("memory_system_config", {})
        self.log_path = Path(self.config.get("log_path", "data/memory.log"))
        self.vector_db_path = Path(self.config.get("vector_db_path", "data/vector_memory"))
        self.kg_path = Path(self.config.get("knowledge_graph_path", "data/knowledge.graphml"))
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.vector_db_path.mkdir(parents=True, exist_ok=True)
        self.kg_path.parent.mkdir(parents=True, exist_ok=True)

    def _setup_journal(self):
        self.journal_logger = logging.getLogger("MyIu.Journal")
        handler = logging.FileHandler(self.log_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        if not self.journal_logger.handlers:
            self.journal_logger.addHandler(handler)
        self.journal_logger.setLevel(logging.INFO)
        self.journal_logger.propagate = False
        self.journal_logger.info("Nhật ký Hiện sinh đã được thiết lập.")

    def _setup_vector_store(self):
        self.chroma_client = chromadb.PersistentClient(path=str(self.vector_db_path))
        self.memory_collection = self.chroma_client.get_or_create_collection(name="memory_stream")
        self.log.info(f"Bộ nhớ Liên tưởng (Vector Store) đã kết nối. Số lượng ký ức vector: {self.memory_collection.count()}")

    def _load_knowledge_graph(self):
        if self.kg_path.exists():
            try:
                self.knowledge_graph = nx.read_graphml(self.kg_path)
            except Exception:
                self.knowledge_graph = nx.DiGraph()
        self.log.info(f"Bản đồ Tri thức sẵn sàng. Số nút: {self.knowledge_graph.number_of_nodes()}")

    def _save_knowledge_graph(self):
        try:
            nx.write_graphml(self.knowledge_graph, self.kg_path)
        except Exception as e:
            self.log.error(f"Lỗi khi lưu Bản đồ Tri thức: {e}")
            
    async def add_memory(self, node: MemoryNode):
        self.journal_logger.info(node.model_dump_json(indent=2))
        if self.memory_collection:
            self.memory_collection.add(
                documents=[node.content],
                metadatas=[node.model_dump(exclude={'content'})],
                ids=[node.id]
            )
        self.knowledge_graph.add_node(node.id, **node.model_dump())
        self._save_knowledge_graph()

    async def stop(self):
        self.log.info("Hệ thống Memory đa lớp đang dừng...")
        self._save_knowledge_graph()
        await super().stop()
""",
    
    # 4. Final version of soma.py
    "soma.py": """
import asyncio
import json
from myiu.app_context import AppContext
from myiu.event_bus import EventBus
from myiu.logging_config import get_logger
from myiu.llm_core import LLMCore
from myiu.memory import Memory
from myiu.affect import Affect
from myiu.cortex import Cortex
from myiu.emotional_cache import EmotionalCache

class Soma:
    def __init__(self):
        self.app_context = AppContext()
        self.log = get_logger("Soma")
        self.app_context.set_service("log", self.log)
        self._load_config()

    def _load_config(self):
        try:
            with open("genome_static.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            self.app_context.set_service("genome_static_config", config)
        except Exception as e:
            self.log.error(f"Không thể tải genome_static.json: {e}")

    async def start(self):
        self.log.info("Soma: Bắt đầu khởi tạo các module cốt lõi...")
        
        core_modules = {
            "llm_core": LLMCore, "emotional_cache": EmotionalCache,
            "memory": Memory, "affect": Affect, "cortex": Cortex
        }
        
        # Khởi tạo tuần tự để đảm bảo các phụ thuộc được đáp ứng
        for name, module_class in core_modules.items():
            try:
                instance = module_class(self.app_context)
                self.app_context.set_service(name, instance)
                await instance.start() # Chờ mỗi module khởi động xong
                self.log.info(f"Module '{name.capitalize()}' đã khởi động thành công.")
            except Exception as e:
                self.log.error(f"Lỗi khi khởi tạo module {name}: {e}", exc_info=True)
        
        self.log.info("Soma: Tất cả các module cốt lõi đã khởi động xong.")

    async def stop(self):
        self.log.info("Soma: Đang dừng các module...")
        modules = self.app_context.get_all_services()
        for name in reversed(list(modules.keys())):
             if hasattr(modules[name], 'stop'):
                await modules[name].stop()
        self.log.info("Soma: Đã dừng xong.")
"""
}
