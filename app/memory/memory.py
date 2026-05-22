"""
Jarvis Vector Memory — ChromaDB-based long-term memory engine.

Stores and retrieves:
  - Learned skills (dynamic code snippets Jarvis generated)
  - User preferences ("always use dark mode", etc.)
  - Past task outcomes
"""

import os
import json
import hashlib
import chromadb
from chromadb.config import Settings as ChromaSettings

# Store DB inside the project folder
_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "jarvis_memory")
os.makedirs(_DB_PATH, exist_ok=True)

_client = chromadb.PersistentClient(
    path=_DB_PATH,
    settings=ChromaSettings(anonymized_telemetry=False),
)

# Two collections: skills and preferences
_skills_col = _client.get_or_create_collection("skills")
_prefs_col  = _client.get_or_create_collection("preferences")


# ── Utility ────────────────────────────────────────────────────────────────

def _uid(text: str) -> str:
    """Stable short ID based on content hash."""
    return hashlib.md5(text.encode()).hexdigest()[:16]


# ── Skills ─────────────────────────────────────────────────────────────────

def save_skill(task_description: str, code: str) -> None:
    """Persist a successful dynamic skill for future reuse."""
    uid = _uid(task_description)
    payload = json.dumps({"description": task_description, "code": code})
    _skills_col.upsert(
        ids=[uid],
        documents=[task_description],
        metadatas=[{"code": code, "description": task_description}],
    )


def find_skill(task_description: str, n: int = 1) -> list[dict]:
    """
    Returns up to n most relevant saved skills for a given task description.
    Each item: {"description": ..., "code": ..., "distance": float}
    """
    try:
        results = _skills_col.query(
            query_texts=[task_description],
            n_results=min(n, _skills_col.count()),
        )
        skills = []
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            dist = results["distances"][0][i]
            skills.append({
                "description": meta["description"],
                "code": meta["code"],
                "distance": dist,
            })
        return skills
    except Exception:
        return []


def list_skills() -> list[str]:
    """List all saved skill descriptions."""
    try:
        return [m["description"] for m in _skills_col.get()["metadatas"]]
    except Exception:
        return []


# ── Preferences ────────────────────────────────────────────────────────────

def save_preference(key: str, value: str) -> None:
    """Store a user preference (e.g. key='browser', value='Chrome')."""
    uid = _uid(key)
    _prefs_col.upsert(
        ids=[uid],
        documents=[f"{key}: {value}"],
        metadatas=[{"key": key, "value": value}],
    )


def get_all_preferences() -> dict:
    """Return all stored preferences as a plain dict."""
    try:
        metas = _prefs_col.get()["metadatas"]
        return {m["key"]: m["value"] for m in metas}
    except Exception:
        return {}


def format_preferences_for_prompt() -> str:
    """Returns a string suitable for injecting into LLM prompts."""
    prefs = get_all_preferences()
    if not prefs:
        return ""
    lines = [f"- {k}: {v}" for k, v in prefs.items()]
    return "USER PREFERENCES:\n" + "\n".join(lines)
