# gmail_tool + download_kokoro

> 26 nodes · cohesion 0.10

## Key Concepts

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
- **Extract a specific header value by name.** (1 connections) — `app/services/gmail_tool.py`
- **Convert raw email date string to a clean readable format.** (1 connections) — `app/services/gmail_tool.py`
- **Truncate text to a max length with ellipsis.** (1 connections) — `app/services/gmail_tool.py`
- **Search Gmail inbox by keyword, sender, label, or status. Examples:…** (1 connections) — `app/services/gmail_tool.py`
- **List unread emails with priority triage and LLM one-line summaries.** (1 connections) — `app/services/gmail_tool.py`
- **Read the full body of a specific email by its ID. email_id is the numeric Gmail…** (1 connections) — `app/services/gmail_tool.py`
- **Get a quick summary of the most recent emails in the inbox. Returns sender and…** (1 connections) — `app/services/gmail_tool.py`
- **Authenticate and return a Gmail API service object. Handles first-time OAuth…** (1 connections) — `app/services/gmail_tool.py`
- **Recursively extract readable text from an email payload.** (1 connections) — `app/services/gmail_tool.py`
- **progress()** (1 connections) — `scripts/download_kokoro.py`
- *... and 1 more nodes in this community*

## Relationships

- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (12 shared connections)
- [calendar_tool](calendar_tool.md) (1 shared connections)
- [memory_tool](memory_tool.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [dark_enhancement + dark_video_enhancement](dark_enhancement_+_dark_video_enhancement.md) (1 shared connections)
- [safe_executor](safe_executor.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [chat + rag_memory](chat_+_rag_memory.md) (1 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (1 shared connections)

## Source Files

- `app/services/gmail_tool.py`
- `scripts/download_kokoro.py`
- `test_api.py`
- `test_gmail.py`

## Audit Trail

- EXTRACTED: 53 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*