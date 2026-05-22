from fastapi import FastAPI
from app.api.routes import documents, chat

app = FastAPI(title="RAG API DEMO")




app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chats"])

@app.get("/health")
async def app_health():
    return {"message": "RAG API DEMO is running"}