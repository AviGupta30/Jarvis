# chat

> 8 nodes · cohesion 0.25

## Key Concepts

- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_to_platform()** (4 connections) — `app/api/chat.py`
- **_explicit_platform()** (3 connections) — `app/api/chat.py`
- **_is_open()** (1 connections) — `app/api/chat.py`
- **_plat()** (1 connections) — `app/api/chat.py`
- **youtube' / 'spotify' if the text names one platform (song/music are neutral).** (1 connections) — `app/api/chat.py`
- **Re-target an unspecific media intent (pause/next/play X) to the given platform.** (1 connections) — `app/api/chat.py`
- **"close this song and play shape of you", "pause the video then open mrbeast's…** (1 connections) — `app/api/chat.py`

## Relationships

- [planner + dynamic_skill](planner_+_dynamic_skill.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [youtube_control](youtube_control.md) (1 shared connections)
- [tool-registry + vector_store](tool-registry_+_vector_store.md) (1 shared connections)

## Source Files

- `app/api/chat.py`

## Audit Trail

- EXTRACTED: 12 (75%)
- INFERRED: 4 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*