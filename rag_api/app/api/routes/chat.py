from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse, RetrievedChunk
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService

router = APIRouter()

@router.post("/query", response_model=ChatQueryResponse)
async def query_documents(
    payload: ChatQueryRequest,
    db: AsyncSession = Depends(get_db),
):
    embedding_service = EmbeddingService()
    llm_service = LLMService()

    query_embedding =await embedding_service.embed_query(payload.question)

    rows = await RetrievalService.retrieve_relevant_chunks(
        db=db,
        query_embedding=query_embedding,
        document_ids=payload.document_ids,
        top_k=payload.top_k,
    )

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No relevant chunks found for the selected documents"
        )
    retrieved_chunks = []
    context_chunks = []
    for chunk, distance in rows:
        score = 1 - float(distance)
        retrieved_chunks.append(
            RetrievedChunk(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                content=chunk.content,
                score=score,
            )
        )

        context_chunks.append(chunk.content)

    answer = await llm_service.answer_question(
        question=payload.question,
        context_chunks=context_chunks,
        temperature=payload.temperature
    )

    return ChatQueryResponse(
        answer=answer,
        retrieved_chunks=retrieved_chunks
    )