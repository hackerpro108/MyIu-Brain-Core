from myiu.council.base_member import CouncilMember
class OppositionAgent(CouncilMember):
    def __init__(self, app_context):
        super().__init__(app_context, "OppositionAgent", "Đóng vai kẻ phản biện để tìm ra lỗ hổng.")
    async def evaluate(self, topic: str, context: dict) -> str:
        prompt = f"[System] Bạn là một người hoài nghi và phản biện. Hãy tìm ra những điểm yếu, lỗ hổng, và lý do tại sao chúng ta KHÔNG NÊN làm điều sau: '{topic}'"
        return self.llm_core.generate_response(prompt)
