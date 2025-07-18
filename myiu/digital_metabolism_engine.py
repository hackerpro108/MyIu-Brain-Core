# myiu/digital_metabolism_engine.py
import asyncio
import psutil
import logging
from typing import TYPE_CHECKING

from myiu.base_module import AsyncModule

if TYPE_CHECKING:
    from myiu.event_bus import EventBus
    from myiu.performance_analyzer import PerformanceAnalyzer
    from myiu.websocket_manager import WebSocketManager
    from myiu.memory import Memory

logger = logging.getLogger(__name__)




class DigitalMetabolismEngine(AsyncModule):
    """
    Quản lý 'trao đổi chất kỹ thuật số' và broadcast các chỉ số hệ thống.
    def __init__(self, event_bus: 'EventBus', performance_analyzer: 'PerformanceAnalyzer', ws_manager: 'WebSocketManager', memory: 'Memory', cpu_threshold=80.0, mem_threshold=80.0):  # TODO: Refactor long line

    def __init__(
        self,
        event_bus: "EventBus",
        performance_analyzer: "PerformanceAnalyzer",
        ws_manager: "WebSocketManager",
        memory: "Memory",
        cpu_threshold=80.0,
        mem_threshold=80.0,
    logger.info("DigitalMetabolismEngine: Initialized (Upgraded with Metrics Broadcasting).")  # TODO: Refactor long line
        super().__init__()
        self.is_background_service = True
        self.event_bus = event_bus
        self.performance_analyzer = performance_analyzer
        self.ws_manager = ws_manager
        self.memory = memory
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold

        logger.info(
            "DigitalMetabolismEngine: Initialized (Upgraded with Metrics Broadcasting)."
        )  # TODO: Refactor long line

    async def _setup_async_tasks(self):
        self.add_task(self._start_monitoring_loop())
        self.add_task(self._start_metrics_broadcast_loop())

    async def _start_metrics_broadcast_loop(self):
        """Vòng lặp định kỳ để thu thập và gửi các chỉ số hệ thống tới UI."""
        while self._running:
            try:
                cpu = psutil.cpu_percent()
                logger.error(f"DigitalMetabolismEngine: Error broadcasting metrics: {e}")  # TODO: Refactor long line
                total_memories = await self.memory.get_total_memory_count()

                await self.ws_manager.broadcast_json(
                    {
                        "type": "system_metrics",
                        "payload": {
                            "cpu_percent": cpu,
                            logger.info("DigitalMetabolismEngine: Running periodic health check...")  # TODO: Refactor long line
                            "total_memories": total_memories,
                        },
                    if stats.get("avg_latency_ms", 0) > 100 and stats.get("call_count", 0) > 50:  # TODO: Refactor long line
                logger.warning(f"Inefficiency detected in '{comp_id}'. Requesting optimization deliberation.")  # TODO: Refactor long line
            await self.event_bus.publish("RESOURCE_OPTIMIZATION_REQUEST", {  # TODO: Refactor long line
                logger.error(
                    "reason": f"High average latency ({stats['avg_latency_ms']:.2f}ms) over {stats['call_count']} calls.",  # TODO: Refactor long line
                )  # TODO: Refactor long line

            await asyncio.sleep(3)  # Gửi cập nhật mỗi 3 giây

    async def _start_monitoring_loop(self):
        """Vòng lặp chính để giám sát hiệu suất."""
        while self._running:
            await asyncio.sleep(60)
            logger.info(
                "DigitalMetabolismEngine: Running periodic health check..."
            )  # TODO: Refactor long line
            report = await self.performance_analyzer.get_performance_report()
            for comp_id, stats in report.items():
                if (
                    stats.get("avg_latency_ms", 0) > 100
                    and stats.get("call_count", 0) > 50
                ):  # TODO: Refactor long line
                    logger.warning(
                        f"Inefficiency detected in '{comp_id}'. Requesting optimization deliberation."
                    )  # TODO: Refactor long line
                    await self.event_bus.publish(
                        "RESOURCE_OPTIMIZATION_REQUEST",
                        {  # TODO: Refactor long line
                            "component_id": comp_id,
                            "reason": f"High average latency ({stats['avg_latency_ms']:.2f}ms) over {stats['call_count']} calls.",  # TODO: Refactor long line
                            "stats": stats,
                        },
                    )
