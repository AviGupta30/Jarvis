from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embeddings import get_embedding
from app.services.vector_store import save_document_chunk

router = APIRouter()

class IngestRequest(BaseModel):
    content: str

@router.post("/ingest")
async def ingest_memory(request: IngestRequest):
    embedding = await get_embedding(request.content)
    await save_document_chunk(request.content, embedding)
    return {"status": "success", "message": "Document ingested successfully"}
