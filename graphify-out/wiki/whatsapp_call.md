# whatsapp_call

> 11 nodes · cohesion 0.27

## Key Concepts

- **whatsapp_call.py** (11 connections) — `app/services/whatsapp_call.py`
- **confirm_whatsapp_call()** (8 connections) — `app/services/whatsapp_call.py`
- **_click_voice_call_button()** (4 connections) — `app/services/whatsapp_call.py`
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp_call.py`
- **flow_stream()** (3 connections) — `app/api/chat.py`
- **_get_whatsapp_window()** (3 connections) — `app/services/whatsapp_call.py`
- **initiate_whatsapp_call()** (2 connections) — `app/services/whatsapp_call.py`
- **_type_via_clipboard()** (2 connections) — `app/services/whatsapp_call.py`
- **whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…** (1 connections) — `app/services/whatsapp_call.py`
- **Focus the WhatsApp window or open it if not running. Returns True on success.** (1 connections) — `app/services/whatsapp_call.py`
- **Click the audio call button in the WhatsApp Desktop chat header. Position is…** (1 connections) — `app/services/whatsapp_call.py`

## Relationships

- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (4 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (2 shared connections)
- [chat + llm](chat_+_llm.md) (2 shared connections)
- [tools](tools.md) (2 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/whatsapp_call.py`

## Audit Trail

- EXTRACTED: 22 (88%)
- INFERRED: 3 (12%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*