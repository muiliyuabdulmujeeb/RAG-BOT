import logging
import time
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.models.document import Document
from app.models.chunk import DocumentChunk
from app.schemas.document import DocumentResponse
from app.services.pdf_service import PDFService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    start_time = time.time()
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid4()}_{file.filename}"
    file_path = upload_dir / unique_name

    content = await file.read()
    file_path.write_bytes(content)

    logger.info("extracting text...")
    pages = PDFService.extract_text(str(file_path))
    logger.info("chunking texts...")
    chunking_service = ChunkingService()
    chunks = await chunking_service.chunk_pages(pages)
    if not chunks:
        raise HTTPException(status_code=400, detail="No chunks could be created from this PDF file")    
    logger.info("embedding chunks")
    embedding_service = EmbeddingService()
    embeddings = await embedding_service.embed_texts([chunk["content"] for chunk in chunks])

    logger.info("persisting data...")
    document = Document(
        filename=file.filename,
        title=file.filename,
        file_path=str(file_path),
        status="processed"
    )
    db.add(document)
    await db.flush()

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        db.add(
            DocumentChunk(
                document_id=document.id,
                chunk_index=idx,
                page_number=chunk["page_number"],
                content=chunk["content"],
                embedding=embedding
            )
        )
        
    await db.commit()
    await db.refresh(document)
    logger.info("service took %s seconds", time.time()-start_time)
    return document


@router.get("", response_model=list[DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Document).order_by(Document.created_at.desc()))
    return list(result.scalars().all())