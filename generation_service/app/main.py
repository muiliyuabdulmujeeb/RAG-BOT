from fastapi import FastAPI

from app.schemas.generation import GenerateRequest, GenerateResponse
from app.services.llm_service import LLMService

app = FastAPI(title="Generation Service")

llm_service = LLMService()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(payload: GenerateRequest):
    answer = await llm_service.generate_answer(
        question=payload.question,
        context_chunks=payload.context_chunks,
        temperature=payload.temperature
    )
    return GenerateResponse(answer=answer)