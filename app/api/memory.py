"""
app/api/memory.py — Jarvis Long-Term Memory API Router
-------------------------------------------------------
Exposes REST endpoints for the RAG memory system:
  POST /memory/recall    — semantic search over all past turns
  GET  /memory/history   — paginated conversation history
  GET  /memory/stats     — storage statistics
  DELETE /memory/forget  — soft-delete turns matching a query

Also retains the original /ingest endpoint for knowledge-base injection.
All endpoints obey JARVIS_ARCHITECTURE Rule #4 (dual frontend + voice access).
"""

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/memory", tags=["memory"])


# ── Request Models ────────────────────────────────────────────────────────────

class IngestRequest(BaseModel):
    content: str

class RecallRequest(BaseModel):
    query: str
    top_k: int = 5
    min_score: float = 0.30

class ForgetRequest(BaseModel):
    query: str


# ── Original ingest endpoint (keep for backward compat) ───────────────────────

@router.post("/ingest")
async def ingest_memory(request: IngestRequest):
    """Ingest a knowledge chunk into the vector store."""
    try:
        from app.services.embeddings import get_embedding
        from app.services.vector_store import save_document_chunk
        embedding = await get_embedding(request.content)
        await save_document_chunk(request.content, embedding)
        return {"status": "success", "message": "Document ingested successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── Long-Term RAG Memory Endpoints ───────────────────────────────────────────

@router.post("/recall")
async def recall_memory(request: RecallRequest):
    """
    Semantic search over all stored conversation turns.
    Returns the most relevant past turns with timestamps and citations.

    Example:
        POST /memory/recall
        {"query": "my exam schedule", "top_k": 5}
    """
    try:
        from app.services.rag_memory import recall, format_recall_for_prompt
        results = await recall(
            query=request.query,
            top_k=request.top_k,
            min_score=request.min_score,
        )
        formatted = format_recall_for_prompt(results, query=request.query)
        return {
            "status": "success",
            "query": request.query,
            "results": results,
            "formatted_context": formatted,
            "count": len(results),
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "results": []}


@router.get("/history")
async def get_history(
    limit: int = Query(default=50, ge=1, le=500),
    date: Optional[str] = Query(default=None, description="Filter by date YYYY-MM-DD"),
):
    """
    Retrieve paginated conversation history from MySQL.

    Query params:
        limit (int): Max number of turns (default 50, max 500)
        date  (str): Optional date filter in YYYY-MM-DD format
    """
    try:
        from app.services.rag_memory import get_history
        rows = await get_history(limit=limit, date_filter=date)
        return {
            "status": "success",
            "count": len(rows),
            "date_filter": date,
            "turns": rows,
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "turns": []}


@router.get("/stats")
async def memory_stats():
    """
    Return statistics about Jarvis's long-term memory store.
    Includes total turns, total sessions, oldest/newest memory, FAISS vector count.
    """
    try:
        from app.services.rag_memory import get_memory_stats
        stats = await get_memory_stats()
        return {"status": "success", **stats}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.delete("/forget")
async def forget_memory(request: ForgetRequest):
    """
    Soft-delete conversation turns that are semantically related to the query.
    Useful when the user wants Jarvis to forget something specific.

    Example:
        DELETE /memory/forget
        {"query": "my exam schedule"}
    """
    try:
        from app.services.rag_memory import forget_turns
        result = await forget_turns(request.query)
        return {"status": "success", **result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
