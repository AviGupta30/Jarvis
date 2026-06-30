"""
resume_detector.py — Jarvis Resume Intent Classifier
-----------------------------------------------------
Isolated service (JARVIS_ARCHITECTURE Rule #1, #2, #3, #4):
  - Pure-function classifier — NO LLM calls, NO network, runs in <1ms
  - Detects when a user wants to CONTINUE/EXTEND/MODIFY a prior task
  - Works for BOTH frontend and voice via the unified /chat route (Rule #4)
  - Imports NOTHING from other tool modules (Rule #1)
  - All functions wrapped in try/except (Rule #2)
  - Stateless — takes inputs, returns output, no side effects (Rule #3)

How it works:
  1. REFERENCE SCAN — looks for referential phrases ("that document", "it", "the same file")
  2. ACTION SCAN — looks for continuation verbs ("add", "append", "continue", "update", "extend")
  3. TASK MATCHING — maps the intent to the most recent matching ledger entry
  4. CONFIDENCE CHECK — only triggers if confidence is HIGH (conservative to avoid false positives)

Returns None for any ambiguous case, letting normal flow handle it safely.
"""

import re

# ── Reference phrases that signal "I mean the thing I just worked on" ─────────
# These are strong indicators of resume intent.
_REFERENCE_PATTERNS = [
    # Pronouns referencing prior work
    r"\b(that|the same|it|this|the)\s+(file|document|doc|word doc|docx|ppt|presentation|slide deck|message|report|assignment)\b",
    r"\b(that|the)\s+(one|thing)\s+(i|you|we)\s+(just|recently|earlier)\b",

    # Explicit continuation phrases
    r"\b(continue|resume|pick up|carry on|keep going)\s+(from|where|on|with)\b",
    r"\bcontinue\s+(writing|editing|working)\b",
    r"\bwhere (you|we) left off\b",
    r"\bfrom (where|the point) (i|we|you) stopped\b",
    r"\bfrom (the )?last (time|session|chat)\b",
    r"\bpick(ing)? up\s+(from|where)\b",

    # Possessive references to known recent outputs
    r"\b(the|that)\s+(last|previous|recent)\s+(document|doc|file|ppt|presentation|message|email)\b",
    r"\b(the document|the file|the ppt|the presentation|the message)\s+(you|jarvis)\s+(just|recently|already)\s+(made|created|wrote|sent|built|drafted)\b",
    r"\b(same|existing)\s+(document|doc|file|ppt|presentation|message)\b",

    # "Add to / append to" patterns (with or without explicit object noun)
    r"\badd(ing)?\s+(more|to|a section|a slide|content|text|paragraph|details|information)\s+(to|in|on)\s+(it|that|the|this)\b",
    r"\badd\s+(more|some|additional|extra)\s*(content|text|details|info|information|stuff)?\s*(to\s+it|to\s+that|in\s+it)?\b",
    r"\badd\s+(more|content|text|details)\s+to\s+it\b",
    r"\bappend(ing)?\s+(to|it|that|the)\b",
    r"\binsert(ing)?\s+(into|to)\s+(it|that|the|this)\b",
    r"\bupdate(ing)?\s+(it|that|the|this)\s+(document|doc|file|ppt|presentation|message)?\b",
    r"\bextend(ing)?\s+(it|that|the|this)\b",
    r"\bedit(ing)?\s+(it|that|the|this)\s+(document|doc|file|ppt|presentation)?\b",
    r"\bmodify(ing)?\s+(it|that|the|this)\b",

    # WhatsApp-specific
    r"\b(send|message)\s+(?:him|her|them|the same person|that person)\s+(again|another|more)\b",
    r"\banother\s+message\s+to\s+(the same|him|her|them|that person)\b",
    r"\bsend\s+another\s+(message|msg|text)\s+to\b",
    r"\bmessage\s+(him|her|them|the same person|that person)\s+again\b",
    r"\breply\s+to\s+(him|her|them|that|the same)\b",
    r"\bfollow.?up\s+with\s+(him|her|them|the same)\b",
]

# ── Continuation action verbs — strengthen the signal ─────────────────────────
_CONTINUATION_VERBS = {
    "add", "append", "insert", "extend", "expand", "continue", "resume",
    "update", "edit", "modify", "change", "fix", "correct", "improve",
    "include", "attach", "write more", "add more", "put in", "include in",
    "follow up", "reply", "respond", "send another", "message again",
}

# ── Fresh-task indicators — if these are present, do NOT resume ───────────────
# These override resume intent even if a reference phrase is found.
# NOTE: 'send another message' is deliberately EXCLUDED — it is a resume (send again),
# not a fresh task creation. Only 'create/make/write/new message' should block.
_FRESH_TASK_INDICATORS = [
    r"\b(create|make|build|generate|new|fresh|brand new|another)\s+(a\s+)?(new\s+)?(word|document|doc|file|ppt|presentation)\b",
    r"\b(create|make|write|draft)\s+(a\s+)?(new\s+)?message\b",   # new message composition (not send-again)
    r"\bstart\s+(a\s+)?(new|fresh|different)\b",
    r"\bopen\s+a\s+new\b",
    r"\bdifferent\s+(document|file|ppt|topic)\b",
]

# ── Task type → resume action mapping ─────────────────────────────────────────
_TASK_RESUME_ACTIONS = {
    "write_file":              "append",
    "append_file":             "append",
    "create_word_doc":         "append",
    "append_to_file":          "append",
    "ppt_create":              "extend",
    "ppt_edit":                "modify",
    "do_assignment":           "continue",
    "assemble_assignment":     "modify",
    "initiate_whatsapp_send":  "continue",
    "confirm_whatsapp_send":   "continue",
    "send_whatsapp_message":   "continue",
    "generate_answers":        "continue",
    "humanize_all_answers":    "continue",
    "check_emails":            "continue",
    "agentic_web_action":      "extend",
    "browse_and_read":         "extend",
}

# ── Task type → file-context key ──────────────────────────────────────────────
# Where to look in the context dict to find the file/resource being resumed
_CONTEXT_PATH_KEYS = [
    "file_path", "path", "filename", "contact_name", "url", "pdf_path"
]


def _has_reference_phrase(text: str) -> bool:
    """Return True if the text contains a strong resume-intent reference phrase."""
    text_lower = text.lower().strip()
    for pattern in _REFERENCE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def _has_fresh_task_indicator(text: str) -> bool:
    """Return True if the text clearly indicates a FRESH (new) task, not a continuation."""
    text_lower = text.lower().strip()
    for pattern in _FRESH_TASK_INDICATORS:
        if re.search(pattern, text_lower):
            return True
    return False


def _has_continuation_verb(text: str) -> bool:
    """Return True if the text contains an action verb suggesting continuation."""
    text_lower = text.lower().strip()
    return any(verb in text_lower for verb in _CONTINUATION_VERBS)


def _extract_task_resource(entry: dict) -> str:
    """
    Extract the most human-readable resource identifier from a ledger entry.
    E.g., the file path, contact name, URL, etc.
    """
    ctx = entry.get("context", {})
    # Check the args sub-dict (how task_ledger.py stores it)
    args = ctx.get("args", {})
    for key in _CONTEXT_PATH_KEYS:
        val = ctx.get(key) or args.get(key)
        if val and isinstance(val, str):
            return val
    return ""


def _find_best_task_match(text: str, recent_tasks: list) -> dict | None:
    """
    Given the user's text and a list of recent ledger entries, find the
    best matching resumable task. Searches newest-first.
    """
    text_lower = text.lower().strip()

    # Build keyword hints from the user's text to narrow down task type
    _KEYWORD_TO_TYPES = {
        "word":         ["write_file", "create_word_doc", "append_file"],
        "document":     ["write_file", "create_word_doc", "append_file"],
        "doc":          ["write_file", "create_word_doc", "append_file"],
        "file":         ["write_file", "append_file", "create_word_doc"],
        "ppt":          ["ppt_create", "ppt_edit"],
        "presentation": ["ppt_create", "ppt_edit"],
        "slide":        ["ppt_create", "ppt_edit"],
        "deck":         ["ppt_create", "ppt_edit"],
        "whatsapp":     ["initiate_whatsapp_send", "confirm_whatsapp_send", "send_whatsapp_message"],
        "message":      ["initiate_whatsapp_send", "confirm_whatsapp_send", "send_whatsapp_message"],
        "email":        ["check_emails", "summarize_inbox"],
        "assignment":   ["do_assignment", "assemble_assignment", "generate_answers"],
        "website":      ["agentic_web_action", "browse_and_read"],
        "web":          ["agentic_web_action", "browse_and_read"],
    }

    preferred_types: set[str] = set()
    for keyword, types in _KEYWORD_TO_TYPES.items():
        if keyword in text_lower:
            preferred_types.update(types)

    # Search newest-first for a resumable match
    for entry in reversed(recent_tasks):
        if not entry.get("resumable", False):
            continue
        task_type = entry.get("task_type", "")

        # If we have preferred types, only match those
        if preferred_types and task_type not in preferred_types:
            continue

        # If no preferred types, match ANY resumable task (most recent wins)
        return entry

    return None


# ── Public API ────────────────────────────────────────────────────────────────

def detect_resume_intent(user_text: str, recent_tasks: list) -> dict | None:
    """
    Determine whether the user's message is a continuation of a prior task.

    This is the main entry point called by chat.py before keyword detection.

    Args:
        user_text:    The raw user prompt string.
        recent_tasks: List of recent ledger entries (from task_ledger.get_recent_tasks_raw()).

    Returns:
        A dict with resume metadata if resume intent is detected, or None.

        On resume detection:
        {
            "is_resume": True,
            "task_id": "uuid-of-original-task",
            "resume_action": "append" | "modify" | "continue" | "extend",
            "original_task": { ...full ledger entry... },
            "resource": "path/to/file or contact name or url",
            "extracted_instruction": "Add a section on entanglement",
        }
    """
    try:
        if not user_text or not recent_tasks:
            return None

        # GATE 1: Immediately bail if this looks like a fresh task
        if _has_fresh_task_indicator(user_text):
            return None

        # GATE 2: Must have either a reference phrase OR a continuation verb
        has_ref  = _has_reference_phrase(user_text)
        has_verb = _has_continuation_verb(user_text)

        # We require BOTH for ambiguous cases — only reference phrase alone
        # is strong enough to trigger (e.g., "add more to that document")
        if not has_ref and not has_verb:
            return None

        # GATE 3: If only verb (no reference), be extra cautious
        # e.g., "edit the file" alone is not enough — user might mean a different file
        if has_verb and not has_ref:
            # Only trigger if verb is explicit continuation (not a general edit)
            strong_continuation_only = {
                "continue", "resume", "pick up", "carry on", "keep going",
                "follow up", "follow-up"
            }
            text_lower = user_text.lower()
            if not any(verb in text_lower for verb in strong_continuation_only):
                return None

        # GATE 4: Find the best matching task
        matched_task = _find_best_task_match(user_text, recent_tasks)
        if not matched_task:
            return None

        task_type      = matched_task.get("task_type", "")
        resume_action  = _TASK_RESUME_ACTIONS.get(task_type, "continue")
        resource       = _extract_task_resource(matched_task)

        return {
            "is_resume":              True,
            "task_id":                matched_task.get("task_id", ""),
            "resume_action":          resume_action,
            "original_task":          matched_task,
            "resource":               resource,
            "extracted_instruction":  user_text,
        }

    except Exception:
        # Safety net — NEVER crash the main chat flow
        return None


def get_resume_context_string(resume_info: dict) -> str:
    """
    Convert a resume detection result into a human-readable context string
    that can be prepended to the user's prompt before it goes to the LLM.

    Args:
        resume_info: The dict returned by detect_resume_intent().

    Returns:
        A formatted string providing the LLM with context about the prior task.
    """
    try:
        if not resume_info or not resume_info.get("is_resume"):
            return ""

        orig     = resume_info.get("original_task", {})
        action   = resume_info.get("resume_action", "continue")
        resource = resume_info.get("resource", "")
        desc     = orig.get("description", "")[:200]
        ts       = orig.get("timestamp", "")[:16].replace("T", " ")
        ctx      = orig.get("context", {})

        parts = [
            f"[RESUMING PRIOR TASK]",
            f"Original task: {desc}",
            f"Performed at: {ts}",
            f"Suggested action: {action}",
        ]

        if resource:
            parts.append(f"Resource to {action}: {resource}")

        # Include any relevant context from the original task
        args = ctx.get("args", {})
        for key in _CONTEXT_PATH_KEYS:
            val = ctx.get(key) or args.get(key)
            if val and isinstance(val, str) and val != resource:
                parts.append(f"Context ({key}): {val}")
                break  # Only show one extra context hint

        parts.append(
            f"INSTRUCTION: {action.upper()} the above — do NOT create a new file/resource "
            f"unless the user explicitly asks for a new one."
        )

        return "\n".join(parts)

    except Exception:
        return ""
