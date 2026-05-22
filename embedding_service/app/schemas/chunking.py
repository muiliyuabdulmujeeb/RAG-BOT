from pydantic import BaseModel, Field

class PageInput(BaseModel):
    page_number: int
    text: str

class ChunkRequest(BaseModel):
    pages: list[PageInput] = Field(..., min_length=1)
    chunk_size: int = 200
    overlap: int = 40

class ChunkItem(BaseModel):
    page_number: int
    content: str
    token_count: int

class ChunkResponse(BaseModel):
    chunks: list[ChunkItem]