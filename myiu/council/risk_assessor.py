from myiu.council.base_member import CouncilMember
class RiskAssessor(CouncilMember):
    def __init__(self, app_context):
        super().__init__(app_context, "RiskAssessor", "Phân tích rủi ro và lợi ích.")
    async def evaluate(self, topic: str, context: dict) -> str:
        prompt = f"[System] Bạn là một nhà phân tích rủi ro. Hãy đánh giá lợi ích và hậu quả tiềm tàng của vấn đề sau: '{topic}'"
        return self.llm_core.generate_response(prompt)
