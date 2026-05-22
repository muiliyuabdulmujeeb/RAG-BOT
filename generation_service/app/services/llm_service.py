import httpx

from app.core.config import settings
from app.services.prompt_service import PromptService

class LLMService:
    async def generate_answer(self, question: str, context_chunks: list[str], temperature: float=0.1) -> str:
        prompt = PromptService.build_document_qa_prompt(question=question, context_chunks=context_chunks)

        async with httpx.AsyncClient(timeout=1800.0) as client:
            response = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.ollama_chat_model,
                    "prompt": prompt,
                    "stream": False,
                    "keep_alive": "30m",
                    "options": {
                        "temperature": temperature,
                        "num_ctx": 4096,
                    },
                },
            )

            response.raise_for_status()
            data = response.json()
            return data["response"].strip()