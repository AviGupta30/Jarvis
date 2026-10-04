# gmail_tool

> 28 nodes · cohesion 0.11

## Key Concepts

- **gmail_tool.py** (17 connections) — `app/services/gmail_tool.py`
- **check_emails()** (7 connections) — `app/services/gmail_tool.py`
- **summarize_inbox()** (7 connections) — `app/services/gmail_tool.py`
- **traceback** (7 connections)
- **_format_date()** (6 connections) — `app/services/gmail_tool.py`
- **get_email_body()** (6 connections) — `app/services/gmail_tool.py`
- **_get_gmail_service()** (6 connections) — `app/services/gmail_tool.py`
- **_get_header()** (6 connections) — `app/services/gmail_tool.py`
- **list_unread()** (6 connections) — `app/services/gmail_tool.py`
- **_decode_body()** (5 connections) — `app/services/gmail_tool.py`
- **test_gmail.py** (5 connections) — `test_gmail.py`
- **download_kokoro.py** (4 connections) — `scripts/download_kokoro.py`
- **_truncate()** (3 connections) — `app/services/gmail_tool.py`
- **test_api.py** (3 connections) — `test_api.py`
- **urllib_request** (3 connections)
- **download()** (2 connections) — `scripts/download_kokoro.py`
- **gmail_tool.py — Jarvis Gmail Integration (Step 5)…** (1 connections) — `app/services/gmail_tool.py`
- **Extract a specific header value by name.** (1 connections) — `app/services/gmail_tool.py`
- **Convert raw email date string to a clean readable format.** (1 connections) — `app/services/gmail_tool.py`
- **Truncate text to a max length with ellipsis.** (1 connections) — `app/services/gmail_tool.py`
- **Search Gmail inbox by keyword, sender, label, or status. Examples:…** (1 connections) — `app/services/gmail_tool.py`
- **List unread emails with priority triage and LLM one-line summaries.** (1 connections) — `app/services/gmail_tool.py`
- **Read the full body of a specific email by its ID. email_id is the numeric Gmail…** (1 connections) — `app/services/gmail_tool.py`
- **Get a quick summary of the most recent emails in the inbox. Returns sender and…** (1 connections) — `app/services/gmail_tool.py`
- **Authenticate and return a Gmail API service object. Handles first-time OAuth…** (1 connections) — `app/services/gmail_tool.py`
- *... and 3 more nodes in this community*

## Relationships

- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (5 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (2 shared connections)
- [assignment_humanizer](assignment_humanizer.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [memory_tool + memory](memory_tool_+_memory.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)
- [main](main.md) (1 shared connections)
- [task_ledger + resume_detector](task_ledger_+_resume_detector.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)

## Source Files

- `app/services/gmail_tool.py`
- `scripts/download_kokoro.py`
- `test_api.py`
- `test_gmail.py`

## Audit Trail

- EXTRACTED: 60 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*