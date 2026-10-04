# whatsapp_smart

> 24 nodes · cohesion 0.13

## Key Concepts

- **whatsapp_smart.py** (17 connections) — `app/services/whatsapp_smart.py`
- **confirm_whatsapp_send()** (11 connections) — `app/services/whatsapp_smart.py`
- **search_whatsapp_contact()** (8 connections) — `app/services/whatsapp_smart.py`
- **_focus_or_open_whatsapp()** (7 connections) — `app/services/whatsapp_smart.py`
- **read_whatsapp_messages()** (7 connections) — `app/services/whatsapp_smart.py`
- **Flows** (7 connections) — `docs/features/whatsapp.md`
- **initiate_whatsapp_send()** (5 connections) — `app/services/whatsapp_smart.py`
- **_type_via_clipboard()** (5 connections) — `app/services/whatsapp_smart.py`
- **_fuzzy_score()** (4 connections) — `app/services/whatsapp_smart.py`
- **_get_visible_search_results()** (3 connections) — `app/services/whatsapp_smart.py`
- **open_whatsapp()** (3 connections) — `app/services/whatsapp_smart.py`
- **_clear_search()** (2 connections) — `app/services/whatsapp_smart.py`
- **_get_whatsapp_window()** (2 connections) — `app/services/whatsapp_smart.py`
- **whatsapp_smart.py — Jarvis Smart WhatsApp Integration (Fully Isolated)…** (1 connections) — `app/services/whatsapp_smart.py`
- **After typing a search in WhatsApp, take a screenshot and use OCR to read…** (1 connections) — `app/services/whatsapp_smart.py`
- **Opens the WhatsApp desktop app and brings it to focus.** (1 connections) — `app/services/whatsapp_smart.py`
- **Fuzzy-search for a contact by keyword in WhatsApp's search. Opens WhatsApp,…** (1 connections) — `app/services/whatsapp_smart.py`
- **PHASE 1 — Confirmation step. Does NOT send yet. Returns a confirmation prompt…** (1 connections) — `app/services/whatsapp_smart.py`
- **PHASE 2 — Actually sends the WhatsApp message after user confirmed. Single…** (1 connections) — `app/services/whatsapp_smart.py`
- **Open a contact's chat in WhatsApp and use OCR to read the latest messages.…** (1 connections) — `app/services/whatsapp_smart.py`
- **Focus the WhatsApp window or open it if not running. Returns True on success.** (1 connections) — `app/services/whatsapp_smart.py`
- **Type text by copying to clipboard and pasting — handles Unicode names reliably.** (1 connections) — `app/services/whatsapp_smart.py`
- **Clear the WhatsApp search box.** (1 connections) — `app/services/whatsapp_smart.py`
- **Score how well 'query' matches 'candidate' name. Uses keyword matching so…** (1 connections) — `app/services/whatsapp_smart.py`

## Relationships

- [tools + window_layout](tools_+_window_layout.md) (4 shared connections)
- [tools + ui_inspector](tools_+_ui_inspector.md) (4 shared connections)
- [dump_wa_ui + find_call_btn](dump_wa_ui_+_find_call_btn.md) (2 shared connections)
- [whatsapp](whatsapp.md) (2 shared connections)
- [whatsapp_call](whatsapp_call.md) (2 shared connections)
- [reply_generator](reply_generator.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [server + persistence](server_+_persistence.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [thread_extractor](thread_extractor.md) (1 shared connections)

## Source Files

- `app/services/whatsapp_smart.py`
- `docs/features/whatsapp.md`

## Audit Trail

- EXTRACTED: 42 (75%)
- INFERRED: 14 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*