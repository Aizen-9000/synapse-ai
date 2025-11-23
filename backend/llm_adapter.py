from dotenv import load_dotenv
import os, httpx
load_dotenv()

class LLMAdapter:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model_default = os.getenv("GROQ_MODEL_DEFAULT", "llama-3.1-8b-instant")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    async def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.7, model: str = None):
        if not self.api_key:
            return "[ERROR] GROQ_API_KEY not set!"
        model_to_use = model or self.model_default
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": model_to_use, "messages": [{"role": "user", "content": prompt}], "max_tokens": max_tokens, "temperature": temperature}
        async with httpx.AsyncClient(timeout=120) as client:
            try:
                response = await client.post(self.base_url, json=payload, headers=headers)
                if response.status_code != 200:
                    return f"[GROQ ERROR] {response.text}"
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                return f"[GROQ ERROR] {str(e)}"

llm = LLMAdapter()