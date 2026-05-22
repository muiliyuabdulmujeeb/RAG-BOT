from pydantic import BaseModel, Field
from typing import List


class ChatQueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    document_ids: List[int] = Field(..., min_length=1)
    top_k: int = 5
    temperature: int = 0.1


class RetrievedChunk(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    score: float


class ChatQueryResponse(BaseModel):
    answer: str
    retrieved_chunks: list[RetrievedChunk]