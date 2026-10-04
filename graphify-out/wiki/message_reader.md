# message_reader

> 19 nodes · cohesion 0.15

## Key Concepts

- **message_reader.py** (19 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **read_messages()** (8 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_bring_whatsapp_to_front()** (6 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_ocr()** (5 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_get_whatsapp_window()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_read_via_uia()** (4 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_heuristic_parse_ocr_lines()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **_parse_uia_message_string()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **read_messages_as_string()** (3 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **message_reader.py — Jarvis WhatsApp Intelligence: Message Reader…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Restores and focuses WhatsApp window. Returns True on success.** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Walks the WhatsApp UIA accessibility tree to extract messages. WhatsApp Desktop…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Parses a raw UIA ListItem Name string into a structured message dict.…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Screenshot-based OCR fallback. Crops the right 65% of the WhatsApp window (chat…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Turns raw OCR lines into message dicts. Heuristic: a line ending with a time…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Main entry point. Tries UIA first, falls back to OCR. Args: max_messages: How…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Tool-registry-friendly wrapper. Returns a human-readable string. Called by…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **Finds the WhatsApp Desktop window safely. Mirrors the exact exclusion logic…** (1 connections) — `app/services/whatsapp_intelligence/message_reader.py`
- **pytesseract** (1 connections)

## Relationships

- [thread_extractor](thread_extractor.md) (5 shared connections)
- [dump_wa_ui + find_call_btn](dump_wa_ui_+_find_call_btn.md) (3 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)

## Source Files

- `app/services/whatsapp_intelligence/message_reader.py`

## Audit Trail

- EXTRACTED: 39 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*