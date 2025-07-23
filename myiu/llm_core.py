# Tên file: myiu/llm_core.py (Phiên bản Đồng bộ - Ổn định)
import os
import time
from typing import Dict, Any, List, Optional
from llama_cpp import Llama
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext

class LLMCore(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.llm: Optional[Llama] = None
        
        genome = self.app_context.get_service("genome_static_config")
        llm_config = genome.get("llm_config", {})

        self.model_params: Dict[str, Any] = {
            "model_path": llm_config.get("model_path"),
            "n_ctx": int(llm_config.get("n_ctx", 2048)),
            "n_threads": int(llm_config.get("n_threads", 2)),
            "n_gpu_layers": int(llm_config.get("n_gpu_layers", 0)),
            "verbose": llm_config.get("verbose", False)
        }
        
        gen_params = llm_config.get("generation_params", {})
        self.generation_params: Dict[str, Any] = {
            "system_prompt": gen_params.get("system_prompt", "You are a helpful AI."),
            "max_tokens": int(gen_params.get("max_tokens", 256)),
            "temperature": float(gen_params.get("temperature", 0.7)),
            "stop": gen_params.get("stop_tokens", ["<|im_end|>"])
        }
        
        try:
            self.llm = Llama(**self.model_params)
            self.log.info("LLMCore: Model đã được tải thành công.")
        except Exception as e:
            self.log.critical(f"Lỗi nghiêm trọng khi tải model: {e}", exc_info=True)
            raise e

    def generate_response(self, prompt: str) -> str:
        """
        Hàm suy luận đồng bộ, đơn giản và đáng tin cậy.
        """
        if not self.llm:
            return "Lỗi: Lõi suy luận chưa sẵn sàng."
        
        try:
            messages: List[Dict[str, str]] = [
                {"role": "system", "content": self.generation_params.get("system_prompt")},
                {"role": "user", "content": prompt}
            ]
            
            output = self.llm.create_chat_completion(
                messages=messages,
                max_tokens=self.generation_params.get("max_tokens"),
                temperature=self.generation_params.get("temperature"),
                stop=self.generation_params.get("stop")
            )
            
            return output['choices'][0]['message']['content'].strip()

        except Exception as e:
            self.log.error(f"Lỗi nghiêm trọng trong quá trình suy luận: {e}", exc_info=True)
            return "Xin lỗi sếp, tôi đã gặp một lỗi nghiêm trọng khi đang suy nghĩ."

    async def stop(self):
        self.log.info("LLMCore: Đang dừng module.")
        self.llm = None
        await super().stop()
