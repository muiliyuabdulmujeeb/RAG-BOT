import httpx

from app.core.config import settings

class ChunkingService:
    async def chunk_pages(
            self,
            pages: list[dict],
            chunk_size: int = 200,
            overlap: int = 40
    ) -> list[dict]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{settings.embedding_service_url}/chunk",
                json={
                    "pages": pages,
                    "chunk_size": chunk_size,
                    "overlap": overlap,
                }
            )
            response.raise_for_status()
            data = response.json()
            return data["chunks"]