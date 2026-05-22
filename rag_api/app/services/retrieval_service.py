from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import DocumentChunk

class RetrievalService:
    @staticmethod
    async def retrieve_relevant_chunks(
        db: AsyncSession,
        query_embedding: list[float],
        document_ids: list[int],
        top_k: int = 5
    ):
        stmt = (
            select(
                DocumentChunk,
                DocumentChunk.embedding.cosine_distance(query_embedding).label("distance"),
            )
            .where(DocumentChunk.document_id.in_(document_ids))
            .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
        )
        result = await db.execute(stmt)
        return result.all()