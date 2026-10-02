# thread_extractor

> 14 nodes · cohesion 0.19

## Key Concepts

- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **extract_thread_as_string()** (5 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_open_contact_chat()** (4 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_find_latest_incoming()** (3 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_group_into_turns()** (3 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_get_current_chat_title()** (2 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Merges consecutive messages from the same sender into a single turn. This makes…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Scans the thread from the end to find the most recent message from 'them' —…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Main entry point. Opens the contact's chat and extracts a structured thread.…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Tool-registry-friendly wrapper. Returns human-readable string. Called by…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Opens a specific contact's chat using Ctrl+N → paste → Enter. Mirrors the exact…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Tries to read the active chat's contact name from the WhatsApp window title.…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`

## Relationships

- [message_reader](message_reader.md) (5 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (4 shared connections)
- [reply_generator](reply_generator.md) (4 shared connections)
- [ssml_processor + debug_wa](ssml_processor_+_debug_wa.md) (1 shared connections)
- [whatsapp_smart + tools](whatsapp_smart_+_tools.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)

## Source Files

- `app/services/whatsapp_intelligence/thread_extractor.py`

## Audit Trail

- EXTRACTED: 33 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*