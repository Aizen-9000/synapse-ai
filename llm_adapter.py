import asyncio
from typing import Optional, Any
from openai import OpenAI
from .config import settings
from .web_search import search_web


class LLMAdapter:
    def __init__(self):
        self.mode = settings.MODE
        self.client: Optional[Any] = None
        if self.mode != "mock" and settings.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except Exception as e:
                print(f"[LLM ERROR] Failed to initialize OpenAI client: {e}")

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 256,
        temperature: float = 0.7,
        search: bool = False
    ) -> str:
        if self.mode == "mock" or not self.client:
            return f"[MOCK-REPLY] Echo: {prompt[:200]}"

        # Optional web search
        if search:
            try:
                web_results = await search_web(prompt)
                prompt = f"Here are some recent web results:\n{web_results}\n\nNow answer the query:\n{prompt}"
            except Exception as e:
                prompt = f"[WEB SEARCH FAILED] {str(e)}\n\n{prompt}"

        def sync_call() -> str:
            try:
                # Avoid optional member access issues
                chat_api = getattr(self.client, "chat", None)
                completions_api = getattr(chat_api, "completions", None) if chat_api else None
                if completions_api:
                    resp = completions_api.create(
                        model=settings.OPENAI_MODEL,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens,
                        temperature=temperature,
                    )
                    choices = getattr(resp, "choices", [])
                    if choices:
                        choice = choices[0]
                        msg = getattr(choice, "message", None)
                        content = getattr(msg, "content", None) if msg else None
                        text = getattr(choice, "text", None)
                        return str(content or text or "[LLM ERROR] Empty response")
                return "[LLM ERROR] chat.completions not available"
            except Exception as e:
                return f"[LLM ERROR] {str(e)}"

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, sync_call)
        return str(result)

    async def translate_text(self, text: str, target_lang: str) -> str:
        prompt = f"Translate the following text to {target_lang}:\n{text}"
        return await self.generate(prompt)


# Global adapter instance
llm = LLMAdapter()