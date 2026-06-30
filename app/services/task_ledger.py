"""
task_ledger.py — Jarvis Task Context Ledger
--------------------------------------------
Isolated service (JARVIS_ARCHITECTURE Rule #1, #2, #3, #4):
  - Records every significant tool execution to a persistent JSON ledger
  - Makes recent task history queryable so Jarvis can resume/extend prior work
  - Works for BOTH frontend and voice via the unified /chat route (Rule #4)
  - Imports NOTHING from other tool modules (Rule #1)
  - All functions wrapped in try/except with human-readable return strings (Rule #2)
  - All state persisted to JSON — no in-memory singletons (Rule #3)

Storage: app/data/task_ledger.json
  Capped at 20 entries (FIFO rollover). Keeps file small and LLM context clean.

Public API:
  log_task(task_type, description, context, status, related_tool)  → str
  get_recent_tasks(n=5)                                             → str   (formatted for speech/display)
  get_recent_tasks_raw(n=10)                                        → list  (raw dicts for code use)
  find_resumable_task(query)                                        → dict | None
  update_task(task_id, updates)                                     → str
  get_task_ledger_for_prompt()                                      → str   (compact LLM injection string)
"""

import json
import uuid
import datetime
from pathlib import Path

# ── Storage Path ──────────────────────────────────────────────────────────────
# Mirrors the pattern of app/memory/facts.json
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_DATA_DIR     = _PROJECT_ROOT / "app" / "data"
_LEDGER_FILE  = _DATA_DIR / "task_ledger.json"

# Maximum number of entries to keep (oldest rolls off)
_MAX_ENTRIES = 20

# Task types that are "resumable" — user might want to continue these
_RESUMABLE_TASK_TYPES = {
    "write_file", "append_file", "create_word_doc", "append_to_file",
    "ppt_create", "ppt_edit", "do_assignment", "assemble_assignment",
    "initiate_whatsapp_send", "confirm_whatsapp_send", "send_whatsapp_message",
    "generate_answers", "humanize_all_answers",
    "check_emails", "summarize_inbox",
    "agentic_web_action", "browse_and_read",
}

# ── Internal helpers ──────────────────────────────────────────────────────────

def _ensure_ledger_file():
    """Create the data directory and ledger file if they don't exist."""
    _DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not _LEDGER_FILE.exists():
        _LEDGER_FILE.write_text(json.dumps([], indent=2), encoding="utf-8")


def _load_ledger() -> list:
    """Load the ledger from disk. Returns empty list on any error."""
    _ensure_ledger_file()
    try:
        return json.loads(_LEDGER_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_ledger(entries: list):
    """Persist the ledger to disk. Caps at _MAX_ENTRIES (FIFO)."""
    _ensure_ledger_file()
    try:
        # Keep only the most recent entries
        capped = entries[-_MAX_ENTRIES:]
        _LEDGER_FILE.write_text(json.dumps(capped, indent=2), encoding="utf-8")
    except Exception:
        pass  # Ledger writes are best-effort — never break the main flow


# ── Public API ────────────────────────────────────────────────────────────────

def log_task(
    task_type: str,
    description: str,
    context: dict = None,
    status: str = "completed",
    related_tool: str = None,
) -> str:
    """
    Record a completed (or in-progress) task to the persistent ledger.

    Args:
        task_type:    The tool name or category (e.g., 'write_file', 'ppt_create')
        description:  The original user instruction or a summary of what was done
        context:      Dict of tool-specific metadata (file paths, contacts, etc.)
        status:       'completed' | 'in_progress' | 'failed'
        related_tool: The exact tool name called (same as task_type usually)

    Returns:
        Human-readable confirmation string.
    """
    try:
        entries = _load_ledger()
        entry = {
            "task_id":     str(uuid.uuid4()),
            "timestamp":   datetime.datetime.now().isoformat(timespec="seconds"),
            "task_type":   task_type,
            "description": description[:500],  # cap to prevent huge files
            "context":     context or {},
            "status":      status,
            "resumable":   task_type in _RESUMABLE_TASK_TYPES,
            "related_tool": related_tool or task_type,
        }
        entries.append(entry)
        _save_ledger(entries)
        return f"Task logged: {task_type} — {description[:80]}"
    except Exception as e:
        return f"Task ledger log failed (non-fatal): {e}"


def get_recent_tasks(n: int = 5) -> str:
    """
    Return a formatted string of the last N tasks, suitable for display or speech.

    Returns:
        Human-readable string listing recent Jarvis actions.
    """
    try:
        entries = _load_ledger()
        if not entries:
            return "No recent tasks found in the task ledger."

        recent = entries[-n:]
        lines = [f"Here are my last {len(recent)} task(s):"]
        for i, e in enumerate(reversed(recent), 1):
            ts  = e.get("timestamp", "unknown time")
            typ = e.get("task_type", "unknown")
            desc = e.get("description", "")[:120]
            st  = e.get("status", "?")
            lines.append(f"  {i}. [{typ}] {desc}  (status: {st}, at: {ts})")
        return "\n".join(lines)
    except Exception as e:
        return f"Could not read task history: {e}"


def get_recent_tasks_raw(n: int = 10) -> list:
    """
    Return the last N raw ledger entries as a list of dicts.
    Used internally by resume_detector.py.

    Returns:
        List of task dicts (newest last). Empty list on error.
    """
    try:
        entries = _load_ledger()
        return entries[-n:] if entries else []
    except Exception:
        return []


def find_resumable_task(query: str) -> dict | None:
    """
    Fuzzy-search the ledger for the most recent resumable task matching the query.
    Used when user says things like 'that document', 'the ppt I just made', etc.

    Args:
        query: User's search string (e.g., 'word document', 'ppt', 'whatsapp message')

    Returns:
        Most recent matching ledger entry dict, or None if no match.
    """
    try:
        entries = _load_ledger()
        if not entries:
            return None

        query_lower = query.lower().strip()

        # Map friendly query terms to task_type patterns
        _TYPE_HINTS = {
            "word":        ["write_file", "create_word_doc", "append_file"],
            "document":    ["write_file", "create_word_doc", "append_file"],
            "doc":         ["write_file", "create_word_doc", "append_file"],
            "file":        ["write_file", "append_file", "create_word_doc"],
            "ppt":         ["ppt_create", "ppt_edit"],
            "presentation":["ppt_create", "ppt_edit"],
            "slide":       ["ppt_create", "ppt_edit"],
            "whatsapp":    ["initiate_whatsapp_send", "confirm_whatsapp_send", "send_whatsapp_message"],
            "message":     ["initiate_whatsapp_send", "confirm_whatsapp_send", "send_whatsapp_message"],
            "email":       ["check_emails", "summarize_inbox"],
            "assignment":  ["do_assignment", "assemble_assignment", "generate_answers"],
            "website":     ["agentic_web_action", "browse_and_read"],
            "web":         ["agentic_web_action", "browse_and_read"],
        }

        # Find matching task types from query
        matching_types = set()
        for keyword, types in _TYPE_HINTS.items():
            if keyword in query_lower:
                matching_types.update(types)

        # Search newest-first for a resumable task matching those types
        for entry in reversed(entries):
            if not entry.get("resumable", False):
                continue
            task_type = entry.get("task_type", "")
            desc_lower = entry.get("description", "").lower()

            # Match by mapped type OR by description containing query words
            type_match = (not matching_types) or (task_type in matching_types)
            desc_match = any(word in desc_lower for word in query_lower.split() if len(word) > 3)

            if type_match and (matching_types or desc_match):
                return entry

        return None
    except Exception:
        return None


def update_task(task_id: str, updates: dict) -> str:
    """
    Update an existing ledger entry by task_id.
    Used after successfully appending to or modifying a prior task.

    Args:
        task_id: UUID of the entry to update
        updates: Dict of fields to update (e.g., {'status': 'completed', 'description': '...'})

    Returns:
        Human-readable confirmation string.
    """
    try:
        entries = _load_ledger()
        for entry in entries:
            if entry.get("task_id") == task_id:
                entry.update(updates)
                entry["last_updated"] = datetime.datetime.now().isoformat(timespec="seconds")
                _save_ledger(entries)
                return f"Task {task_id[:8]}... updated successfully."
        return f"Task {task_id[:8]}... not found in ledger."
    except Exception as e:
        return f"Could not update task: {e}"


def get_task_ledger_for_prompt() -> str:
    """
    Returns a compact, LLM-friendly summary of recent tasks for injection
    into system prompts. Called by chat.py and planner.py.

    Returns:
        A short string (≤ 400 chars) describing what Jarvis recently did,
        or empty string if ledger is empty.
    """
    try:
        entries = _load_ledger()
        if not entries:
            return ""

        # Only show the last 5, only resumable ones are worth highlighting
        recent = [e for e in entries[-5:] if e.get("resumable", False)]
        if not recent:
            # Fall back to all recent
            recent = entries[-3:]

        if not recent:
            return ""

        lines = ["[JARVIS RECENT TASK HISTORY — for context on 'continue/resume/update' requests:]"]
        for e in recent[-5:]:
            ts   = e.get("timestamp", "")[:16].replace("T", " ")
            typ  = e.get("task_type", "?")
            desc = e.get("description", "")[:100]
            ctx  = e.get("context", {})

            # Pull out the most useful context fields
            ctx_hints = []
            if ctx.get("file_path"):
                ctx_hints.append(f"file={ctx['file_path']}")
            if ctx.get("args", {}).get("path"):
                ctx_hints.append(f"path={ctx['args']['path']}")
            if ctx.get("args", {}).get("contact_name"):
                ctx_hints.append(f"contact={ctx['args']['contact_name']}")
            ctx_str = f" ({', '.join(ctx_hints)})" if ctx_hints else ""

            lines.append(f"  • [{ts}] {typ}: {desc[:80]}{ctx_str}")

        return "\n".join(lines)
    except Exception:
        return ""
