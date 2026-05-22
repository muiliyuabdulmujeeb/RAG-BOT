from pydantic import BaseModel, Field

class GenerateRequest(BaseModel):
    question: str = Field(..., min_length=1)
    context_chunks: list[str] = Field(..., min_length=1)
    temperature: float = 0.1


class GenerateResponse(BaseModel):
    answer: str
