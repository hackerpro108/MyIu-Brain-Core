import asyncio
import os
from llama_cpp import Llama
from myiu.async_module import AsyncModule
from myiu.app_context import AppContext

class LLMCore(AsyncModule):
    def __init__(self, app_context: AppContext):
        super().__init__(app_context)
        self.llm = None

        # ✅ Gán cứng đường dẫn và tham số thay vì lấy từ genome_static_config
        self.model_path = "/root/models/phi-2/phi-2.Q4_K_M.gguf"
        self.model_params = { "n_ctx": 2048 }

    async def start(self):
        await super().start()
        self.log.info(f"LLMCore initialized. Model path: {self.model_path}")
        if not self.model_path:
            self.log.error("Model path not configured.")
            return
        try:
            self.llm = await asyncio.to_thread(self._load_model)
            if self.llm:
                self.log.info("Phi-2 model loaded successfully.")
        except Exception as e:
            self.log.critical(f"Critical error during model loading: {e}", exc_info=True)

    def _load_model(self):
        if not os.path.exists(self.model_path):
            self.log.error(f"Model file does not exist: {self.model_path}")
            return None
        return Llama(model_path=self.model_path, **self.model_params)

    def generate_response(self, prompt: str, max_tokens=512, creator_override=False):
        if not self.llm:
            return "LLM is not available."
        final_prompt = prompt
        if creator_override:
            self.log.warning("CREATOR OVERRIDE ACTIVE.")
            final_prompt = f"[CREATOR OVERRIDE] Task: {prompt}"
        output = self.llm(final_prompt, max_tokens=max_tokens, stop=["\n", "Q:"])
        return output['choices'][0]['text'].strip()
