import json
import asyncio
import logging
import os
from datetime import datetime
from myiu.base_module import AsyncModule
from bot_worker.config import PROJECT_ROOT # <-- SỬ DỤNG NEO
from typing import Dict, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from myiu.event_bus import EventBus

logger = logging.getLogger(__name__)

class GenEditor(AsyncModule):
    def __init__(self, event_bus: "EventBus"):
        super().__init__()
        self.event_bus = event_bus
        # Xây dựng đường dẫn tuyệt đối
        self.genome_file_path = os.path.join(PROJECT_ROOT, "genome_dynamic.json")
        self.lock = asyncio.Lock()
        self.genes: Dict[str, Any] = self._load_genes()
        logger.info(f"GenEditor: Initialized with absolute path: {self.genome_file_path}")

    def _load_genes(self) -> Dict[str, Any]:
        try:
            if not os.path.exists(self.genome_file_path): return {}
            with open(self.genome_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("dynamic_genes", {})
        except (json.JSONDecodeError, FileNotFoundError) as e:
             logger.warning(f"GenEditor: Could not load dynamic genome: {e}")
             return {}

    async def _save_genes(self):
         async with self.lock:
            full_genome_data = {
                "dynamic_genes": self.genes,
                "last_updated": datetime.utcnow().isoformat() + "Z",
            }
            with open(self.genome_file_path, "w", encoding="utf-8") as f:
                json.dump(full_genome_data, f, indent=2, ensure_ascii=False)

    # (Các phương thức khác giữ nguyên)
    async def get_all_genes(self) -> Dict[str, Any]:
        return self.genes

    async def add_gene(self, gene_data: Dict[str, Any]):
        gene_id = gene_data.get("id")
        if not gene_id: return
        self.genes[gene_id] = gene_data
        await self._save_genes()

