# Email, calendar & morning brief

## Purpose
Gmail, Google Calendar and the morning brief.

## Email
Registry `check_emails`, `list_unread`, `get_email_body`, `summarize_inbox` → `tools._mail_tool`: if `token.json` exists, try `gmail_tool` (Gmail API, OAuth, priority triage + LLM summaries). On "Gmail error"/exception it falls back to `browser_mail` (just opens Gmail search URLs). `smart_mail_action(task)` = browser compose URL.
**Status:** the Gmail token is revoked (`invalid_grant`). Re-auth: delete `token.json`, then run `python -c "from app.services.gmail_tool import _get_gmail_service; _get_gmail_service()"`.

## Calendar
`calendar_tool`: `get_upcoming_events(days)`, `check_today_schedule()`, `add_event(title, date, time, notes)` (dateparser). OAuth token `calendar_token.json`, client `credentials.json` (repo root, git-ignored).

## Morning brief
`memory_tool.get_morning_brief()` = calendar + Gmail summary + facts → LLM narrative. Triggers: "good morning", "morning brief".

## Gotchas
- Never let the OAuth flow run inside the server without a token file: `run_local_server` blocks the request waiting on a browser.

## Graphify
`graphify explain "_mail_tool"` · `graphify explain "get_morning_brief"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/gmail_tool.py` (342 lines): gmail_tool.py — Jarvis Gmail Integration (Step 5)
  L35 _SCOPES · L39 _get_gmail_service() · L83 _decode_body() · L108 _get_header() · L116 _format_date() · L126 _truncate() · L136 check_emails() · L190 list_unread() · L263 get_email_body() · L298 summarize_inbox()
- `app/services/browser_mail.py` (98 lines): browser_mail.py — Standard Browser Mail Automation
  L14 _get_api_key() · L28 check_emails() · L34 list_unread() · L37 get_email_body() · L40 summarize_inbox() · L44 smart_mail_action()
- `app/services/calendar_tool.py` (220 lines): calendar_tool.py — Jarvis Google Calendar Integration (Step 8)
  L21 _SCOPES · L25 _get_calendar_service() · L51 get_upcoming_events() · L91 check_today_schedule() · L138 add_event()
- `app/services/memory_tool.py` (204 lines): memory_tool.py — Jarvis Persistent Memory (Step 10 — ENHANCED)  *(filtered to this feature)*
  L159 get_morning_brief()
- `app/services/tools.py` (1217 lines): Jarvis Tool Registry — All callable actions Jarvis can perform.  *(filtered to this feature)*
  L1000 _mail_tool()
<!-- AUTO:END -->
