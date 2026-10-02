# ppt_tool + tools

> 6 nodes · cohesion 0.33

## Key Concepts

- **ppt_edit()** (9 connections) — `app/services/ppt_tool.py`
- **Fixed on 2026-09-30 (PPT v6)** (5 connections) — `docs/KNOWN_ISSUES.md`
- **Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`)** (4 connections) — `docs/features/ppt.md`
- **_ppt_edit()** (3 connections) — `app/services/tools.py`
- **Follow-up edit of the last deck (generator). See ppt_studio.edit.** (1 connections) — `app/services/ppt_tool.py`
- **Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…** (1 connections) — `app/services/tools.py`

## Relationships

- [ppt_studio](ppt_studio.md) (3 shared connections)
- [tools](tools.md) (2 shared connections)
- [ppt_content](ppt_content.md) (2 shared connections)
- [ppt_tool](ppt_tool.md) (1 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (1 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)
- [ppt](ppt.md) (1 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (1 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (1 shared connections)

## Source Files

- `app/services/ppt_tool.py`
- `app/services/tools.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 8 (44%)
- INFERRED: 10 (56%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*