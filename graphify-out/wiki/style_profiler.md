# style_profiler

> 28 nodes · cohesion 0.12

## Key Concepts

- **style_profiler.py** (21 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_load_profile()** (9 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_save_profile()** (8 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **build_style_profile()** (7 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **record_sent_reply()** (6 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_compute_profile_stats()** (5 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **get_profile()** (5 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **add_deflection_phrase()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_empty_profile()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **mark_contact_formal()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_now()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_safe_filename()** (4 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **build_style_profile()** (3 connections) — `app/services/tools.py`
- **get_profile_summary()** (3 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **_parse_whatsapp_export()** (3 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **One-time training: parse a WhatsApp .txt chat export to build your personal…** (1 connections) — `app/services/tools.py`
- **style_profiler.py — Jarvis WhatsApp Intelligence: Style Profiler…** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Saves the profile to the correct path. Returns True on success.** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Converts a contact name to a safe filename.** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Parses a WhatsApp .txt chat export and extracts YOUR messages paired with the…** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Computes statistical features from your reply examples.** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Called every time you send a reply through Jarvis. Appends the example to your…** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Marks a contact as formal so replies use a more professional tone.** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Adds a personal deflection phrase to your style profile. e.g. "dekh lete hai",…** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- **Tool-registry entry point. One-time training: parses a WhatsApp .txt export and…** (1 connections) — `app/services/whatsapp_intelligence/style_profiler.py`
- *... and 3 more nodes in this community*

## Relationships

- [reply_generator](reply_generator.md) (5 shared connections)
- [tools + window_layout](tools_+_window_layout.md) (2 shared connections)
- [jarvis_overlay + prompt_overlay](jarvis_overlay_+_prompt_overlay.md) (2 shared connections)
- [server + persistence](server_+_persistence.md) (2 shared connections)
- [assignment_assembler + smart_navigator](assignment_assembler_+_smart_navigator.md) (1 shared connections)
- [calendar_tool + email-calendar](calendar_tool_+_email-calendar.md) (1 shared connections)

## Source Files

- `app/services/tools.py`
- `app/services/whatsapp_intelligence/style_profiler.py`

## Audit Trail

- EXTRACTED: 57 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*