import asyncio
from myiu.app_context import AppContext
from myiu.logging_config import get_logger

# Import tất cả các thành viên
from myiu.council.moral_simulator import MoralSimulator
from myiu.council.historian import Historian
from myiu.council.risk_assessor import RiskAssessor
from myiu.council.opposition_agent import OppositionAgent
from myiu.council.imagination_explorer import ImaginationExplorer

class ConsensusEngine:
    def __init__(self, app_context: AppContext):
        self.app_context = app_context
        self.llm_core = app_context.get_service("llm_core")
        self.log = get_logger(self.__class__.__name__)
        
        # Khởi tạo tất cả các thành viên của hội đồng
        self.members = [
            MoralSimulator(app_context),
            Historian(app_context),
            RiskAssessor(app_context),
            OppositionAgent(app_context),
            ImaginationExplorer(app_context)
        ]
        self.log.info(f"ConsensusEngine đã được tạo với {len(self.members)} thành viên.")

    async def deliberate(self, topic: str, context: dict) -> str:
        """
        Tổ chức một phiên họp của Hội đồng Nội tâm.
        """
        self.log.info(f"--- Bắt đầu phiên biện luận của Hội đồng về chủ đề: '{topic[:50]}...' ---")
        
        # Triệu tập tất cả thành viên để đánh giá đồng thời
        evaluation_tasks = [member.evaluate(topic, context) for member in self.members]
        opinions = await asyncio.gather(*evaluation_tasks)
        
        # Xây dựng báo cáo tổng hợp
        report = f"Chủ đề biện luận: {topic}\\n\\n"
        report += "="*20 + " CÁC Ý KIẾN TỪ HỘI ĐỒNG " + "="*20 + "\\n\\n"
        
        for member, opinion in zip(self.members, opinions):
            self.log.info(f"Ý kiến từ [{member.name}]: {opinion[:70]}...")
            report += f"Góc nhìn từ '{member.name}' ({member.role}):\\n{opinion}\\n\\n"
            
        report += "="*20 + " YÊU CẦU TỔNG HỢP " + "="*20 + "\\n"
        report += "Với vai trò là một nhà lãnh đạo sáng suốt, dựa trên tất cả các góc nhìn đa chiều trên, hãy đưa ra một kết luận hoặc quyết định cuối cùng."

        self.log.info("Tổng hợp các ý kiến để đưa ra quyết định cuối cùng...")
        final_decision = self.llm_core.generate_response(report, max_tokens=1024)
        
        self.log.info(f"--- Phiên biện luận kết thúc. Quyết định: {final_decision[:70]}... ---")
        return final_decision
