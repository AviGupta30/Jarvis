# whatsapp_smart + whatsapp_call

> 39 nodes · cohesion 0.08

## Key Concepts

- **whatsapp_smart.py** (17 connections) — `app/services/whatsapp_smart.py`
- **whatsapp_call.py** (11 connections) — `app/services/whatsapp_call.py`
- **confirm_whatsapp_send()** (11 connections) — `app/services/whatsapp_smart.py`
- **confirm_whatsapp_call()** (8 connections) — `app/services/whatsapp_call.py`
- **search_whatsapp_contact()** (8 connections) — `app/services/whatsapp_smart.py`
- **_focus_or_open_whatsapp()** (7 connections) — `app/services/whatsapp_smart.py`
- **read_whatsapp_messages()** (7 connections) — `app/services/whatsapp_smart.py`
- **Flows** (7 connections) — `docs/features/whatsapp.md`
- **WhatsApp: send, call, read, reply-style cloning** (6 connections) — `docs/features/whatsapp.md`
- **_type_via_clipboard()** (5 connections) — `app/services/whatsapp_smart.py`
- **_click_voice_call_button()** (4 connections) — `app/services/whatsapp_call.py`
- **_focus_or_open_whatsapp()** (4 connections) — `app/services/whatsapp_call.py`
- **_fuzzy_score()** (4 connections) — `app/services/whatsapp_smart.py`
- **flow_stream()** (3 connections) — `app/api/chat.py`
- **_get_whatsapp_window()** (3 connections) — `app/services/whatsapp_call.py`
- **_get_visible_search_results()** (3 connections) — `app/services/whatsapp_smart.py`
- **open_whatsapp()** (3 connections) — `app/services/whatsapp_smart.py`
- **initiate_whatsapp_call()** (2 connections) — `app/services/whatsapp_call.py`
- **_type_via_clipboard()** (2 connections) — `app/services/whatsapp_call.py`
- **_clear_search()** (2 connections) — `app/services/whatsapp_smart.py`
- **_get_whatsapp_window()** (2 connections) — `app/services/whatsapp_smart.py`
- **whatsapp_call.py — Jarvis Smart WhatsApp Calling Integration (Fully Isolated)…** (1 connections) — `app/services/whatsapp_call.py`
- **Focus the WhatsApp window or open it if not running. Returns True on success.** (1 connections) — `app/services/whatsapp_call.py`
- **Click the audio call button in the WhatsApp Desktop chat header. Position is…** (1 connections) — `app/services/whatsapp_call.py`
- **whatsapp_smart.py — Jarvis Smart WhatsApp Integration (Fully Isolated)…** (1 connections) — `app/services/whatsapp_smart.py`
- *... and 14 more nodes in this community*

## Relationships

- [tools](tools.md) (11 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (6 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (3 shared connections)
- [refresh_docs + whatsapp](refresh_docs_+_whatsapp.md) (2 shared connections)
- [style_profiler + reply_generator](style_profiler_+_reply_generator.md) (2 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (1 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/whatsapp_call.py`
- `app/services/whatsapp_smart.py`
- `docs/features/whatsapp.md`

## Audit Trail

- EXTRACTED: 67 (83%)
- INFERRED: 14 (17%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*