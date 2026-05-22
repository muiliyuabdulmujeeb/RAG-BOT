import httpx

from app.core.config import settings


class EmbeddingService:

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.embedding_service_url}/embed",
                json={"texts": texts},
            )
            response.raise_for_status()
            data = response.json()
            return data["embeddings"]
        
    async def embed_query(self, text: str) -> list[list[float]]:
        embeddings = await self.embed_texts([text])
        return embeddings[0]