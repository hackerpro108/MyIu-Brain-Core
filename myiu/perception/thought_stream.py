import logging
from pathlib import Path
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext
from myiu.perception.thought_chunk import ThoughtChunk

class ThoughtStream(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.stream_logger = None
        self.log_path = Path("data/thought_stream.log")

    async def start(self):
        await super().start()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._setup_stream_logger()
        self.log.info("Luồng suy nghĩ (ThoughtStream) đã được kích hoạt.")

    def _setup_stream_logger(self):
        self.stream_logger = logging.getLogger("MyIu.ThoughtStream")
        handler = logging.FileHandler(self.log_path, encoding='utf-8')
        formatter = logging.Formatter('%(message)s') # Chỉ ghi lại nội dung JSON
        handler.setFormatter(formatter)
        if not self.stream_logger.handlers:
            self.stream_logger.addHandler(handler)
        self.stream_logger.setLevel(logging.INFO)
        self.stream_logger.propagate = False
    
    def record(self, chunk: ThoughtChunk):
        if self.stream_logger:
            self.stream_logger.info(chunk.model_dump_json())

    async def stop(self):
        await super().stop()
        self.log.info("Luồng suy nghĩ đã dừng.")
