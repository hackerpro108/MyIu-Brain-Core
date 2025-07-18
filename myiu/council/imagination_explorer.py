from myiu.council.base_member import CouncilMember
class ImaginationExplorer(CouncilMember):
    def __init__(self, app_context):
        super().__init__(app_context, "ImaginationExplorer", "Đề xuất các giải pháp sáng tạo, đột phá.")
    async def evaluate(self, topic: str, context: dict) -> str:
        prompt = f"[System] Bạn là một nhà tư tưởng sáng tạo. Hãy nghĩ ra những giải pháp độc đáo, khác thường, thậm chí điên rồ cho vấn đề sau: '{topic}'"
        return self.llm_core.generate_response(prompt)
