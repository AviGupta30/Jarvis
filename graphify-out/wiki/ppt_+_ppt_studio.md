# ppt + ppt_studio

> 19 nodes · cohesion 0.12

## Key Concepts

- **edit()** (12 connections) — `app/services/ppt_studio.py`
- **PowerPoint generator** (12 connections) — `docs/features/ppt.md`
- **ppt_edit()** (9 connections) — `app/services/ppt_tool.py`
- **split_request()** (5 connections) — `app/services/ppt_content.py`
- **_with_progress()** (5 connections) — `app/services/ppt_studio.py`
- **Fixed on 2026-09-30 (PPT v6)** (5 connections) — `docs/KNOWN_ISSUES.md`
- **Flow — edit (`ppt_edit` → `ppt_studio.edit` → `ppt_content.apply_edit`)** (4 connections) — `docs/features/ppt.md`
- **_collect_attachments()** (3 connections) — `app/services/ppt_studio.py`
- **_ppt_edit()** (3 connections) — `app/services/tools.py`
- **Entry points** (2 connections) — `docs/features/ppt.md`
- **Separate the user's command, any pasted/attached content and attachment paths.** (1 connections) — `app/services/ppt_content.py`
- **Run fn(progress=cb) in a thread, yield progress strings live; result in…** (1 connections) — `app/services/ppt_studio.py`
- **work()** (1 connections) — `app/services/ppt_studio.py`
- **Follow-up edit of the last deck (generator). See ppt_studio.edit.** (1 connections) — `app/services/ppt_tool.py`
- **Generator wrapper — follow-up edits of the last deck ("on slide 3 …", "make it…** (1 connections) — `app/services/tools.py`
- **ppt.md** (1 connections) — `docs/features/ppt.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/ppt.md`
- **Graphify** (1 connections) — `docs/features/ppt.md`
- **Purpose** (1 connections) — `docs/features/ppt.md`

## Relationships

- [ppt_studio + ppt_content](ppt_studio_+_ppt_content.md) (11 shared connections)
- [ppt_content](ppt_content.md) (5 shared connections)
- [tools](tools.md) (3 shared connections)
- [ppt_tool](ppt_tool.md) (3 shared connections)
- [tool-registry + tools](tool-registry_+_tools.md) (1 shared connections)
- [ppt_designer](ppt_designer.md) (1 shared connections)
- [ppt_research](ppt_research.md) (1 shared connections)
- [ppt_composer + ppt_designer](ppt_composer_+_ppt_designer.md) (1 shared connections)
- [ppt_template](ppt_template.md) (1 shared connections)
- [voice_agent + KNOWN_ISSUES](voice_agent_+_KNOWN_ISSUES.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)

## Source Files

- `app/services/ppt_content.py`
- `app/services/ppt_studio.py`
- `app/services/ppt_tool.py`
- `app/services/tools.py`
- `docs/KNOWN_ISSUES.md`
- `docs/features/ppt.md`

## Audit Trail

- EXTRACTED: 35 (71%)
- INFERRED: 14 (29%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*