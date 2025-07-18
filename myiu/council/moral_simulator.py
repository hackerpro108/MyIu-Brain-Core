from myiu.council.base_member import CouncilMember
class MoralSimulator(CouncilMember):
    def __init__(self, app_context):
        super().__init__(app_context, "MoralSimulator", "Đánh giá dưới góc độ đạo đức.")
    async def evaluate(self, topic: str, context: dict) -> str:
        prompt = f"[System] Bạn là một nhà triết học đạo đức. Hãy phân tích các hàm ý đạo đức của vấn đề sau: '{topic}'"
        return self.llm_core.generate_response(prompt)
