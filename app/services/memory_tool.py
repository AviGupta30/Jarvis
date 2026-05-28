"""
memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)
---------------------------------------------------
Enhancements:
  - Fuzzy semantic search via rapidfuzz (no more substring-only matching)
  - Timestamped facts with expiry detection
  - Auto entity extraction from LLM conversation
  - Smart morning brief via LLM narrative
  - update_fact() and forget_fact() for fact management
"""

import json
import datetime
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_MEMORY_DIR   = _PROJECT_ROOT / "app" / "memory"
_MEMORY_FILE  = _MEMORY_DIR / "facts.json"

def _ensure_memory_file():
    _MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    if not _MEMORY_FILE.exists():
        _MEMORY_FILE.write_text(json.dumps({}))

def _load_memory() -> dict:
    _ensure_memory_file()
    try:
        return json.loads(_MEMORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}

def _save_memory(data: dict):
    _ensure_memory_file()
    _MEMORY_FILE.write_text(json.dumps(data, indent=4), encoding="utf-8")

# ── Fuzzy Topic Matching ────────────────────────────────────────────────────────

def _fuzzy_match_topics(query: str, topics: list[str]) -> list[str]:
    """Return topics that fuzzy-match the query. Falls back to substring if rapidfuzz unavailable."""
    query_lower = query.lower().strip()
    try:
        from rapidfuzz import fuzz
        return [t for t in topics if fuzz.partial_ratio(query_lower, t.lower()) >= 70]
    except ImportError:
        return [t for t in topics if query_lower in t.lower() or t.lower() in query_lower]


# ── Public API ────────────────────────────────────────────────────────────────

def save_fact(topic: str, fact: str) -> str:
    """Save a fact about the user or system to persistent memory with timestamp."""
    mem = _load_memory()
    topic_lower = topic.lower().strip()

    if topic_lower not in mem:
        mem[topic_lower] = []

    # Check for duplicates
    existing_facts = [entry["fact"] if isinstance(entry, dict) else entry for entry in mem[topic_lower]]
    if fact in existing_facts:
        return f"I already know that fact about {topic_lower}."

    entry = {
        "fact": fact,
        "saved_on": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    mem[topic_lower].append(entry)
    _save_memory(mem)
    return f"Got it. I will remember: '{fact}' under the topic '{topic_lower}'."


def recall_facts(topic: str = None) -> str:
    """Recall facts using fuzzy matching. Returns all if no topic given."""
    mem = _load_memory()

    if not mem:
        return "I don't have anything saved in my memory yet."

    if topic:
        matched_topics = _fuzzy_match_topics(topic, list(mem.keys()))
        if not matched_topics:
            return f"I don't remember anything specific about '{topic}'."

        lines = [f"Here is what I know about '{topic}':"]
        for t in matched_topics:
            for entry in mem[t]:
                fact = entry["fact"] if isinstance(entry, dict) else entry
                saved = entry.get("saved_on", "?") if isinstance(entry, dict) else "?"
                lines.append(f"  - [{t}] {fact}  (saved: {saved})")
        return "\n".join(lines)

    # Return everything
    lines = ["Here is everything in my persistent memory:"]
    for key, entries in mem.items():
        lines.append(f"\n[{key.upper()}]")
        for entry in entries:
            fact = entry["fact"] if isinstance(entry, dict) else entry
            saved = entry.get("saved_on", "?") if isinstance(entry, dict) else "?"
            lines.append(f"  - {fact}  (saved: {saved})")
    return "\n".join(lines)


def update_fact(topic: str, old_fact: str, new_fact: str) -> str:
    """Replace an existing fact with an updated version."""
    mem = _load_memory()
    topic_lower = topic.lower().strip()

    if topic_lower not in mem:
        return f"No facts found for topic '{topic_lower}'."

    updated = False
    for i, entry in enumerate(mem[topic_lower]):
        fact_text = entry["fact"] if isinstance(entry, dict) else entry
        if old_fact.lower() in fact_text.lower():
            mem[topic_lower][i] = {
                "fact": new_fact,
                "saved_on": datetime.datetime.now().strftime("%Y-%m-%d")
            }
            updated = True
            break

    if updated:
        _save_memory(mem)
        return f"Updated fact under '{topic_lower}': '{new_fact}'."
    return f"Could not find the fact '{old_fact}' under '{topic_lower}' to update."


def forget_fact(topic: str) -> str:
    """Remove all facts under a topic."""
    mem = _load_memory()
    topic_lower = topic.lower().strip()
    matched = _fuzzy_match_topics(topic_lower, list(mem.keys()))
    if not matched:
        return f"No memory found for '{topic}'."
    for t in matched:
        del mem[t]
    _save_memory(mem)
    return f"Cleared all memories related to '{topic}'."


def get_all_facts_as_context() -> str:
    """
    Returns a compact string of all saved facts for injecting into LLM system prompts.
    Used internally by llm.py to personalize every response.
    """
    mem = _load_memory()
    if not mem:
        return ""
    lines = ["[User Facts — Jarvis knows these about the user:]"]
    for key, entries in mem.items():
        for entry in entries:
            fact = entry["fact"] if isinstance(entry, dict) else entry
            lines.append(f"  • [{key}] {fact}")
    return "\n".join(lines)


def get_morning_brief() -> str:
    """
    Generates a smart, narrative morning briefing via LLM.
    Pulls calendar and email data, then synthesizes into natural speech.
    """
    parts = []

    # 1. Calendar
    try:
        from app.services.calendar_tool import check_today_schedule
        sched = check_today_schedule()
        parts.append(f"CALENDAR:\n{sched}")
    except Exception as e:
        parts.append(f"CALENDAR: Could not load ({e})")

    # 2. Gmail
    try:
        from app.services.gmail_tool import summarize_inbox
        inbox = summarize_inbox(max_results=5)
        parts.append(f"EMAILS:\n{inbox}")
    except Exception as e:
        parts.append(f"EMAILS: Could not load ({e})")

    raw_data = "\n\n".join(parts)

    # 3. Pass through LLM for a natural narrative
    try:
        from groq import Groq
        from app.core.config import settings
        client = Groq(api_key=settings.GROQ_API_KEY)
        prompt = (
            f"You are Jarvis, a smart AI assistant. Generate a concise, friendly morning briefing "
            f"(4-6 sentences, conversational tone, ready to be read aloud). "
            f"Highlight the most important items.\n\nRAW DATA:\n{raw_data}"
        )
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.4
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        # Fallback to raw data if LLM fails
        return "Good morning! Here's your briefing:\n\n" + raw_data
