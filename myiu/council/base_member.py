from abc import ABC, abstractmethod
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext

class CouncilMember(AsyncModule, ABC):
    def __init__(self, app_context: AppContext, name: str, role: str):
        super().__init__(app_context)
        self.name = name
        self.role = role
        self.llm_core = self.app_context.get_service("llm_core")
        self.memory = self.app_context.get_service("memory")
        self.affect = self.app_context.get_service("affect")

    @abstractmethod
    async def evaluate(self, topic: str, context: dict) -> str:
        """Mỗi thành viên phải thực thi phương pháp đánh giá riêng."""
        pass
