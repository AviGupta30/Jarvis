# gmail_tool

> 21 nodes · cohesion 0.17

## Key Concepts

- **gmail_tool.py** (17 connections) — `app/services/gmail_tool.py`
- **check_emails()** (7 connections) — `app/services/gmail_tool.py`
- **summarize_inbox()** (7 connections) — `app/services/gmail_tool.py`
- **_format_date()** (6 connections) — `app/services/gmail_tool.py`
- **get_email_body()** (6 connections) — `app/services/gmail_tool.py`
- **_get_gmail_service()** (6 connections) — `app/services/gmail_tool.py`
- **_get_header()** (6 connections) — `app/services/gmail_tool.py`
- **list_unread()** (6 connections) — `app/services/gmail_tool.py`
- **_decode_body()** (5 connections) — `app/services/gmail_tool.py`
- **test_gmail.py** (5 connections) — `test_gmail.py`
- **_truncate()** (3 connections) — `app/services/gmail_tool.py`
- **gmail_tool.py — Jarvis Gmail Integration (Step 5)…** (1 connections) — `app/services/gmail_tool.py`
- **Extract a specific header value by name.** (1 connections) — `app/services/gmail_tool.py`
- **Convert raw email date string to a clean readable format.** (1 connections) — `app/services/gmail_tool.py`
- **Truncate text to a max length with ellipsis.** (1 connections) — `app/services/gmail_tool.py`
- **Search Gmail inbox by keyword, sender, label, or status. Examples:…** (1 connections) — `app/services/gmail_tool.py`
- **List unread emails with priority triage and LLM one-line summaries.** (1 connections) — `app/services/gmail_tool.py`
- **Read the full body of a specific email by its ID. email_id is the numeric Gmail…** (1 connections) — `app/services/gmail_tool.py`
- **Get a quick summary of the most recent emails in the inbox. Returns sender and…** (1 connections) — `app/services/gmail_tool.py`
- **Authenticate and return a Gmail API service object. Handles first-time OAuth…** (1 connections) — `app/services/gmail_tool.py`
- **Recursively extract readable text from an email payload.** (1 connections) — `app/services/gmail_tool.py`

## Relationships

- [benchmark + server](benchmark_+_server.md) (2 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (2 shared connections)
- [memory_tool + email-calendar](memory_tool_+_email-calendar.md) (2 shared connections)
- [repair + renderer](repair_+_renderer.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)

## Source Files

- `app/services/gmail_tool.py`
- `test_gmail.py`

## Audit Trail

- EXTRACTED: 47 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*