# thread_extractor

> 16 nodes · cohesion 0.16

## Key Concepts

- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **read_whatsapp_thread()** (5 connections) — `app/services/tools.py`
- **extract_thread_as_string()** (5 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_open_contact_chat()** (4 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_find_latest_incoming()** (3 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_group_into_turns()** (3 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_get_current_chat_title()** (2 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Open a WhatsApp chat, read the last N messages, and return a structured thread…** (1 connections) — `app/services/tools.py`
- **thread_extractor.py — Jarvis WhatsApp Intelligence: Thread Extractor…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Merges consecutive messages from the same sender into a single turn. This makes…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Scans the thread from the end to find the most recent message from 'them' —…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Main entry point. Opens the contact's chat and extracts a structured thread.…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Tool-registry-friendly wrapper. Returns human-readable string. Called by…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Opens a specific contact's chat using Ctrl+N → paste → Enter. Mirrors the exact…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **Tries to read the active chat's contact name from the WhatsApp window title.…** (1 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`

## Relationships

- [message_reader](message_reader.md) (5 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (3 shared connections)
- [reply_generator](reply_generator.md) (3 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [dump_wa_ui + find_call_btn](dump_wa_ui_+_find_call_btn.md) (2 shared connections)
- [whatsapp_smart](whatsapp_smart.md) (1 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [whatsapp](whatsapp.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`

## Audit Trail

- EXTRACTED: 34 (92%)
- INFERRED: 3 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*