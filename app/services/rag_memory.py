"""
rag_memory.py — Jarvis Long-Term RAG Memory Engine
----------------------------------------------------
Isolated service (JARVIS_ARCHITECTURE Rule #1):
  - Stores every meaningful conversation turn to MySQL + FAISS
  - Recalls semantically similar past turns on every query
  - Works automatically for BOTH voice and frontend via /chat (Rule #4)

Architecture:
  MySQL  → structured metadata (timestamp, session, role, topic tags)
  FAISS  → local vector index for fast semantic similarity search
  fastembed BAAI/bge-small-en-v1.5 → 384-dim embeddings (already in project)
"""

import asyncio
import hashlib
import json
import logging
import os
import re
import uuid
from datetime import datetime
from pathlib import Path

try:
    import aiomysql
except ImportError:
    aiomysql = None  # Will fail gracefully at runtime if MySQL is not available

logger = logging.getLogger(__name__)

# ── Paths ─────────────────────────────────────────────────────────────────────
_DATA_DIR   = Path(__file__).resolve().parent.parent.parent / "data"
_DATA_DIR.mkdir(parents=True, exist_ok=True)

_FAISS_INDEX_PATH = _DATA_DIR / "jarvis_faiss.index"
_FAISS_IDS_PATH   = _DATA_DIR / "jarvis_faiss_ids.json"

# ── Module-level FAISS state ──────────────────────────────────────────────────
_faiss_index = None          # faiss.IndexFlatIP instance
_faiss_ids: list[int] = []   # maps FAISS position → MySQL row id
_session_id: str = str(uuid.uuid4())   # new UUID per server boot
_faiss_lock: asyncio.Lock | None = None  # lazily initialized inside the event loop

def _get_faiss_lock() -> asyncio.Lock:
    """Lazily create the FAISS lock inside a running event loop."""
    global _faiss_lock
    if _faiss_lock is None:
        _faiss_lock = asyncio.Lock()
    return _faiss_lock

# ── Trivial turn filter ───────────────────────────────────────────────────────
_TRIVIAL_PATTERNS = re.compile(
    r"^(ok|okay|k|thanks|thank you|thx|ty|yes|no|yeah|nope|sure|got it|"
    r"great|nice|cool|good|fine|alright|hmm|hm|lol|haha|👍|✅|"
    r"yep|nah|yup|roger|right|understood|noted|done|perfect|awesome|wow)[\s!.?]*$",
    re.IGNORECASE,
)

# ── Topic extraction stopwords ────────────────────────────────────────────────
_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "can", "i", "me", "my", "you", "your",
    "he", "she", "it", "we", "they", "them", "their", "this", "that", "these",
    "those", "what", "which", "who", "when", "where", "why", "how", "and",
    "or", "but", "for", "on", "in", "at", "to", "of", "with", "about",
    "from", "by", "as", "into", "through", "so", "if", "just", "also",
    "get", "got", "tell", "said", "say", "make", "know", "want", "use",
    "jarvis", "please", "ok", "okay", "thanks", "need", "like",
}


# ── Initialization ────────────────────────────────────────────────────────────

def _load_faiss_index():
    """Load FAISS index from disk, or create a fresh one."""
    global _faiss_index, _faiss_ids
    try:
        import faiss
        if _FAISS_INDEX_PATH.exists() and _FAISS_IDS_PATH.exists():
            _faiss_index = faiss.read_index(str(_FAISS_INDEX_PATH))
            _faiss_ids = json.loads(_FAISS_IDS_PATH.read_text(encoding="utf-8"))
            logger.info(f"✅ [rag_memory] Loaded FAISS index ({_faiss_index.ntotal} vectors).")
        else:
            # 384-dim inner product index (cosine similarity after L2 normalization)
            _faiss_index = faiss.IndexFlatIP(384)
            _faiss_ids = []
            logger.info("✅ [rag_memory] Created fresh FAISS index.")
    except ImportError:
        logger.error("❌ [rag_memory] faiss-cpu not installed. Run: pip install faiss-cpu")
        _faiss_index = None
        _faiss_ids = []
    except Exception as e:
        logger.error(f"❌ [rag_memory] FAISS load error: {e}")
        _faiss_index = None
        _faiss_ids = []


def _save_faiss_index():
    """Persist FAISS index and ID map to disk (sync, runs in thread executor)."""
    try:
        import faiss
        if _faiss_index is not None:
            faiss.write_index(_faiss_index, str(_FAISS_INDEX_PATH))
            _FAISS_IDS_PATH.write_text(
                json.dumps(_faiss_ids, indent=2), encoding="utf-8"
            )
    except Exception as e:
        logger.warning(f"[rag_memory] FAISS save warning: {e}")

async def _save_faiss_index_async():
    """Run the sync FAISS save in a thread pool to avoid blocking the event loop."""
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _save_faiss_index)


async def init_rag_memory():
    """
    Boot the RAG memory system:
      1. Initialize MySQL pool + ensure tables exist
      2. Load FAISS index from disk
    Called once from main.py startup_event().
    """
    try:
        from app.core.mysql_db import init_mysql
        await init_mysql()
    except Exception as e:
        logger.error(f"[rag_memory] MySQL init failed: {e}")
    _load_faiss_index()
    logger.info(f"[rag_memory] Session ID: {_session_id}")


# ── Smart Filter ──────────────────────────────────────────────────────────────

def smart_filter(role: str, content: str) -> bool:
    """
    Returns True if the turn is meaningful enough to store.
    Skips trivial single-word/emoji responses.
    """
    stripped = content.strip()
    if len(stripped) < 12:
        return False
    if _TRIVIAL_PATTERNS.match(stripped):
        return False
    return True


# ── Topic Extraction ──────────────────────────────────────────────────────────

def _extract_topics(text: str, max_topics: int = 8) -> str:
    """
    Lightweight keyword-based topic extraction (no LLM call).
    Returns a CSV of the most significant content words.
    """
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    freq: dict[str, int] = {}
    for w in words:
        if w not in _STOPWORDS:
            freq[w] = freq.get(w, 0) + 1
    # Sort by frequency desc, take top N
    sorted_words = sorted(freq, key=lambda w: freq[w], reverse=True)
    return ",".join(sorted_words[:max_topics])


# ── Store Turn ────────────────────────────────────────────────────────────────

async def store_turn(
    role: str,
    content: str,
    turn_index: int = 0,
) -> None:
    """
    Save a conversation turn to MySQL + FAISS.
    Silently skips trivial turns and exact duplicates.

    Args:
        role:        'user' or 'assistant'
        content:     The message text
        turn_index:  Position within the current session
    """
    if not smart_filter(role, content):
        return

    # Dedup via MD5 hash
    content_hash = hashlib.md5(content.encode("utf-8")).hexdigest()

    try:
        from app.core.mysql_db import get_mysql_pool
        pool = await get_mysql_pool()
    except Exception as e:
        logger.warning(f"[rag_memory] MySQL unavailable, skipping store: {e}")
        return

    async with _get_faiss_lock():
        try:
            import numpy as np
            from app.services.embeddings import get_embedding

            # Get embedding
            vector = await get_embedding(content)
            vec_np = np.array([vector], dtype=np.float32)

            # L2-normalize for cosine similarity via inner product
            norm = np.linalg.norm(vec_np)
            if norm > 0:
                vec_np = vec_np / norm

            # Extract topics
            topics = _extract_topics(content)

            # Insert into MySQL
            async with pool.acquire() as conn:
                async with conn.cursor() as cur:
                    # Check for duplicate
                    await cur.execute(
                        "SELECT id FROM conversation_turns WHERE content_hash = %s LIMIT 1",
                        (content_hash,),
                    )
                    if await cur.fetchone():
                        return  # Already stored

                    # Insert new turn (faiss_id will be set after FAISS add)
                    await cur.execute(
                        """
                        INSERT INTO conversation_turns
                            (session_id, turn_index, role, content, content_hash, topic_tags)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (_session_id, turn_index, role, content, content_hash, topics),
                    )
                    mysql_id = cur.lastrowid

                    # Add to FAISS and record position
                    if _faiss_index is not None:
                        faiss_pos = len(_faiss_ids)  # current ntotal before add
                        _faiss_index.add(vec_np)
                        _faiss_ids.append(mysql_id)

                        # Update MySQL row with the faiss_id (= FAISS position)
                        await cur.execute(
                            "UPDATE conversation_turns SET faiss_id = %s WHERE id = %s",
                            (faiss_pos, mysql_id),
                        )

            # Persist FAISS index to disk asynchronously (non-blocking)
            await _save_faiss_index_async()

        except Exception as e:
            logger.warning(f"[rag_memory] store_turn error: {e}")


# ── Recall ────────────────────────────────────────────────────────────────────

async def recall(
    query: str,
    top_k: int = 5,
    min_score: float = 0.30,
) -> list[dict]:
    """
    Semantically recall the most relevant past conversation turns.

    Args:
        query:     The user's current message or a search phrase
        top_k:     Maximum number of results to return
        min_score: Minimum cosine similarity threshold (0-1). Lower = wider recall.

    Returns:
        List of dicts: {role, content, timestamp, session_id, faiss_id, score, topic_tags}
    """
    if _faiss_index is None or _faiss_index.ntotal == 0:
        return []

    try:
        import numpy as np
        from app.services.embeddings import get_embedding

        vector = await get_embedding(query)
        vec_np = np.array([vector], dtype=np.float32)
        norm = np.linalg.norm(vec_np)
        if norm > 0:
            vec_np = vec_np / norm

        k = min(top_k, _faiss_index.ntotal)
        scores, positions = _faiss_index.search(vec_np, k)

        if scores is None or len(scores[0]) == 0:
            return []

        # Filter by score threshold and map to MySQL IDs
        candidates = []
        for score, pos in zip(scores[0], positions[0]):
            if pos < 0 or pos >= len(_faiss_ids):
                continue
            if float(score) < min_score:
                continue
            candidates.append((float(score), int(_faiss_ids[pos]), int(pos)))

        if not candidates:
            return []

        # Fetch from MySQL by ID
        mysql_ids = [c[1] for c in candidates]
        id_to_score = {c[1]: c[0] for c in candidates}

        from app.core.mysql_db import get_mysql_pool
        pool = await get_mysql_pool()

        placeholders = ",".join(["%s"] * len(mysql_ids))
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    f"""
                    SELECT id, session_id, role, content, timestamp, topic_tags
                    FROM conversation_turns
                    WHERE id IN ({placeholders})
                    ORDER BY timestamp ASC
                    """,
                    tuple(mysql_ids),
                )
                rows = await cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "role":       row["role"],
                "content":    row["content"],
                "timestamp":  row["timestamp"].strftime("%Y-%m-%d %H:%M") if row["timestamp"] else "?",
                "session_id": row["session_id"],
                "score":      id_to_score.get(row["id"], 0.0),
                "topic_tags": row["topic_tags"] or "",
                "is_current_session": row["session_id"] == _session_id,
            })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    except Exception as e:
        logger.warning(f"[rag_memory] recall error: {e}")
        return []


# ── Format for Prompt ─────────────────────────────────────────────────────────

def format_recall_for_prompt(results: list[dict], query: str = "") -> str:
    """
    Format recalled memory turns into an injectable LLM context block
    with clear citation (date, session type).
    """
    if not results:
        return ""

    lines = ["[LONG-TERM MEMORY] Jarvis recalled these relevant past exchanges:"]
    for r in results:
        session_label = "this session" if r["is_current_session"] else f"past session ({r['timestamp'][:10]})"
        role_label = "You said" if r["role"] == "user" else "Jarvis replied"
        lines.append(
            f"  - [{session_label} @ {r['timestamp'][11:]}] {role_label}: \"{r['content'][:250]}\""
        )

    lines.append(
        "\nUse the above memory naturally in your response. "
        "If directly relevant, cite it (e.g., 'You mentioned on June 15th that...'). "
        "Do NOT list all memories verbatim unless asked."
    )
    return "\n".join(lines)


# ── Memory Stats ──────────────────────────────────────────────────────────────

async def get_memory_stats() -> dict:
    """Return statistics about stored long-term memory."""
    try:
        from app.core.mysql_db import get_mysql_pool
        pool = await get_mysql_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(
                    "SELECT COUNT(*) as total, "
                    "COUNT(DISTINCT session_id) as sessions, "
                    "MIN(timestamp) as oldest, "
                    "MAX(timestamp) as newest "
                    "FROM conversation_turns"
                )
                row = await cur.fetchone()
        return {
            "total_turns":    row["total"] if row else 0,
            "total_sessions": row["sessions"] if row else 0,
            "oldest_memory":  str(row["oldest"]) if row and row["oldest"] else None,
            "newest_memory":  str(row["newest"]) if row and row["newest"] else None,
            "faiss_vectors":  _faiss_index.ntotal if _faiss_index else 0,
            "current_session": _session_id,
        }
    except Exception as e:
        return {"error": str(e)}


# ── History Retrieval ─────────────────────────────────────────────────────────

async def get_history(limit: int = 50, date_filter: str = None) -> list[dict]:
    """
    Retrieve paginated conversation history from MySQL.

    Args:
        limit:       Max rows to return
        date_filter: Optional date string 'YYYY-MM-DD' to filter by day
    """
    try:
        from app.core.mysql_db import get_mysql_pool
        pool = await get_mysql_pool()
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                if date_filter:
                    await cur.execute(
                        """
                        SELECT session_id, role, content, timestamp, topic_tags
                        FROM conversation_turns
                        WHERE DATE(timestamp) = %s
                        ORDER BY timestamp DESC
                        LIMIT %s
                        """,
                        (date_filter, limit),
                    )
                else:
                    await cur.execute(
                        """
                        SELECT session_id, role, content, timestamp, topic_tags
                        FROM conversation_turns
                        ORDER BY timestamp DESC
                        LIMIT %s
                        """,
                        (limit,),
                    )
                rows = await cur.fetchall()

        return [
            {
                "role":       r["role"],
                "content":    r["content"],
                "timestamp":  str(r["timestamp"]),
                "session_id": r["session_id"],
                "topic_tags": r["topic_tags"] or "",
            }
            for r in rows
        ]
    except Exception as e:
        logger.warning(f"[rag_memory] get_history error: {e}")
        return []


# ── Forget (Soft Delete) ──────────────────────────────────────────────────────

async def forget_turns(query: str) -> dict:
    """
    Soft-delete turns semantically related to a query.
    Removes from MySQL. FAISS index is rebuilt on next restart.

    Returns dict with count of deleted rows.
    """
    try:
        results = await recall(query, top_k=10, min_score=0.45)
        if not results:
            return {"deleted": 0, "message": "No matching memories found."}

        from app.core.mysql_db import get_mysql_pool
        pool = await get_mysql_pool()

        # Get their MySQL IDs via content hash matching
        deleted = 0
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                for r in results:
                    ch = hashlib.md5(r["content"].encode("utf-8")).hexdigest()
                    await cur.execute(
                        "DELETE FROM conversation_turns WHERE content_hash = %s",
                        (ch,),
                    )
                    deleted += cur.rowcount

        return {
            "deleted": deleted,
            "message": f"Removed {deleted} memory turn(s) related to your query.",
        }
    except Exception as e:
        return {"deleted": 0, "message": f"Error: {e}"}
