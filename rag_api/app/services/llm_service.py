import httpx

from app.core.config import settings

class LLMService:
    async def answer_question(
            self,
            question: str,
            context_chunks: list[str],
            temperature: float=0.1,
    ) -> str:
        
        async with httpx.AsyncClient(timeout=1800.0) as client:
            response = await client.post(
                f"{settings.generation_service_url}/generate",
                json={
                    "question": question,
                    "context_chunks": context_chunks,
                    "temperature": temperature,
                },
            )
            response.raise_for_status()
            data = response.json()

            return data["answer"]