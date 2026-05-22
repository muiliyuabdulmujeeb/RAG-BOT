import logging
import time
from fastapi import FastAPI

from app.schemas.embedding import EmbedRequest, EmbedResponse
from app.schemas.chunking import ChunkRequest, ChunkItem, ChunkResponse
from app.services.embedding_service import EmbeddingModelService
from app.services.chunking_service import ChunkingService

logger = logging.getLogger(__name__)

app = FastAPI(title="Embedding Service")

embedding_service = EmbeddingModelService()
chunking_service = ChunkingService()


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/embed", response_model=EmbedResponse)
async def embed(payload: EmbedRequest):
    start_time = time.time()
    embeddings = embedding_service.embed(payload.texts)
    logger.info("embedding took %s seconds", time.time()-start_time)
    return EmbedResponse(embeddings=embeddings)

@app.post("/chunk", response_model=ChunkResponse)
async def chunk(payload: ChunkRequest):
    start_time = time.time()
    chunk_dicts = chunking_service.chunk_pages(
        pages=[page.model_dump() for page in payload.pages],
        chunk_size=payload.chunk_size,
        overlap=payload.overlap
    )
    logger.info("embedding took %s seconds", time.time()-start_time)
    return ChunkResponse(chunks=[ChunkItem(**chunk) for chunk in chunk_dicts])


