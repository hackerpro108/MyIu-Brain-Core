from myiu.council.base_member import CouncilMember
from myiu.models import MemoryNode

class Historian(CouncilMember):
    def __init__(self, app_context):
        super().__init__(app_context, "Historian", "Đối chiếu với các ký ức trong quá khứ.")
        
    async def evaluate(self, topic: str, context: dict) -> str:
        # Tìm kiếm các ký ức có nội dung tương tự
        similar_memories = await self.memory.search_associative(query=topic, n_results=3)
        
        if not similar_memories:
            return "Trong quá khứ, chưa có ký ức nào tương tự trực tiếp với vấn đề này."
            
        # Trích xuất nội dung từ metadata
        # ChromaDB trả về một list các dictionary metadata
        memory_contents = [
            mem.get("metadata", {}).get("original_content", "Không có nội dung") 
            for mem in similar_memories
        ]
        
        summary = "\\n- ".join(memory_contents)
        return f"Dựa trên các ký ức tương tự trong quá khứ, tôi có những ghi nhận sau:\\n- {summary}"
