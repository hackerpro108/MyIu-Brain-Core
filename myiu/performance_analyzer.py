# myiu/performance_analyzer.py
import asyncio
import time
from collections import defaultdict
from typing import Dict, Any

from myiu.base_module import AsyncModule
from myiu.models import ThoughtChunkModel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myiu.event_bus import EventBus




class PerformanceAnalyzer(AsyncModule):
    """
    Đo lường và phân tích hiệu suất của các thành phần trong MyIu,
    như gen và plugin. Cung cấp dữ liệu cho DigitalMetabolismEngine.
    """

    def __init__(self, event_bus: "EventBus"):
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus

        # Sử dụng defaultdict để dễ dàng thêm mới
        self.component_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {"call_count": 0, "total_latency_ms": 0, "last_called": 0}
        )
        self.lock = asyncio.Lock()
        print("PerformanceAnalyzer: Initialized.")

    async def _setup_async_tasks(self):
        """Thiết lập tác vụ nền để lắng nghe sự kiện."""
        self.add_task(self._subscribe_to_events())

    async def _subscribe_to_events(self):
        """Lắng nghe các sự kiện để thu thập dữ liệu hiệu suất."""
        thought_queue = await self.event_bus.subscribe("thought_chunk")
        while self._running:
            thought: ThoughtChunkModel = await thought_queue.get()

            simulated_latency = (time.time() - thought.timestamp.timestamp()) * 1000  # TODO: Refactor long line
            await self.record_performance(f"gene:{thought.gene_id}", simulated_latency)  # TODO: Refactor long line
                # Mô phỏng độ trễ xử lý để tạo ra thought này
                simulated_latency = (
                    time.time() - thought.timestamp.timestamp()
                ) * 1000  # TODO: Refactor long line
                await self.record_performance(
                    f"gene:{thought.gene_id}", simulated_latency
                )  # TODO: Refactor long line

    async def record_performance(self, component_id: str, latency_ms: float):
        """Ghi lại một lần thực thi của một thành phần."""
        async with self.lock:
            stats = self.component_stats[component_id]
            stats["call_count"] += 1
            stats["total_latency_ms"] += latency_ms
            stats["last_called"] = time.time()
avg_latency = stats["total_latency_ms"] / stats["call_count"]  # TODO: Refactor long line
    async def get_performance_report(self) -> Dict[str, Dict[str, Any]]:
        """Cung cấp báo cáo hiệu suất tổng thể."""
        report = {}
        "last_called_ago_sec": round(time.time() - stats["last_called"], 2)  # TODO: Refactor long line
            for comp_id, stats in self.component_stats.items():
                if stats["call_count"] > 0:
                    avg_latency = (
                        stats["total_latency_ms"] / stats["call_count"]
                    )  # TODO: Refactor long line
                    report[comp_id] = {
                        "call_count": stats["call_count"],
                        "avg_latency_ms": round(avg_latency, 2),
                        "last_called_ago_sec": round(
                            time.time() - stats["last_called"], 2
                        ),  # TODO: Refactor long line
                    }
        return report
