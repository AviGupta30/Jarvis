# message_reader + thread_extractor

> 33 nodes · cohesion 0.09

## Key Concepts

- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **thread_extractor.py** (17 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **extract_thread()** (9 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **extract_thread_as_string()** (5 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_uia()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_open_contact_chat()** (4 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_heuristic_parse_ocr_lines()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_parse_uia_message_string()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **read_messages_as_string()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_find_latest_incoming()** (3 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_group_into_turns()** (3 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **_get_current_chat_title()** (2 connections) — `app/services/whatsapp_intelligence/thread_extractor.py`
- **message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Restores and focuses WhatsApp window. Returns True on success.** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Parses a raw UIA ListItem Name string into a structured message dict.…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Screenshot-based OCR fallback. Crops the right 65% of the WhatsApp window (chat…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Turns raw OCR lines into message dicts. Heuristic: a line ending with a time…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Main entry point. Tries UIA first, falls back to OCR. Args: max_messages: How…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Tool-registry-friendly wrapper. Returns a human-readable string. Called by…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Finds the WhatsApp Desktop window safely. Mirrors the exact exclusion logic…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- *... and 8 more nodes in this community*

## Relationships

- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (7 shared connections)
- [persistence + server](persistence_+_server.md) (4 shared connections)
- [assignment_tool + assignment_humanizer](assignment_tool_+_assignment_humanizer.md) (3 shared connections)
- [reply_generator](reply_generator.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)

## Source Files

- `app/services/whatsapp_intelligence/message_reader.py`
- `app/services/whatsapp_intelligence/thread_extractor.py`

## Audit Trail

- EXTRACTED: 67 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*