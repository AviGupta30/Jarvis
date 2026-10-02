# chat + KNOWN_ISSUES

> 25 nodes · cohesion 0.08

## Key Concepts

- **Fixed on 2026-09-28** (16 connections) — `docs/KNOWN_ISSUES.md`
- **_media_compound()** (11 connections) — `app/api/chat.py`
- **_media_target()** (9 connections) — `app/api/chat.py`
- **get_last()** (9 connections) — `app/services/media_state.py`
- **Open** (9 connections) — `docs/KNOWN_ISSUES.md`
- **agentic_web_action()** (8 connections) — `app/services/agentic_web.py`
- **Known issues** (8 connections) — `docs/KNOWN_ISSUES.md`
- **_media_intent_for()** (7 connections) — `app/api/chat.py`
- **_get_calendar_service()** (6 connections) — `app/services/calendar_tool.py`
- **_to_platform()** (4 connections) — `app/api/chat.py`
- **_explicit_platform()** (3 connections) — `app/api/chat.py`
- **_last_media()** (3 connections) — `app/services/youtube_control.py`
- **_worker()** (2 connections) — `app/services/agentic_web.py`
- **Fixed on 2026-10-01 (voice, round 2)** (2 connections) — `docs/KNOWN_ISSUES.md`
- **_is_open()** (1 connections) — `app/api/chat.py`
- **_plat()** (1 connections) — `app/api/chat.py`
- **Which player an ambiguous media command ("pause it", "next song") is for: named…** (1 connections) — `app/api/chat.py`
- **Media tool intent for one clause (YouTube-mode parser first, then keyword…** (1 connections) — `app/api/chat.py`
- **youtube' / 'spotify' if the text names one platform (song/music are neutral).** (1 connections) — `app/api/chat.py`
- **Re-target an unspecific media intent (pause/next/play X) to the given platform.** (1 connections) — `app/api/chat.py`
- **"close this song and play shape of you", "pause the video then open mrbeast's…** (1 connections) — `app/api/chat.py`
- **Generator that streams progress and final answer.** (1 connections) — `app/services/agentic_web.py`
- **Authenticate and return a Google Calendar API service object.** (1 connections) — `app/services/calendar_tool.py`
- **Last media app used within max_age seconds, else None.** (1 connections) — `app/services/media_state.py`
- **KNOWN_ISSUES.md** (1 connections) — `docs/KNOWN_ISSUES.md`

## Relationships

- [youtube_control](youtube_control.md) (12 shared connections)
- [chat + llm](chat_+_llm.md) (9 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (5 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (4 shared connections)
- [tool-registry + memory](tool-registry_+_memory.md) (3 shared connections)
- [spotify_service + media_sessions](spotify_service_+_media_sessions.md) (3 shared connections)
- [ppt_content](ppt_content.md) (3 shared connections)
- [youtube_control + youtube_player](youtube_control_+_youtube_player.md) (2 shared connections)
- [agentic_web](agentic_web.md) (2 shared connections)
- [smart_navigator + rag_memory](smart_navigator_+_rag_memory.md) (2 shared connections)
- [voice](voice.md) (2 shared connections)
- [youtube_player](youtube_player.md) (2 shared connections)

## Source Files

- `app/api/chat.py`
- `app/services/agentic_web.py`
- `app/services/calendar_tool.py`
- `app/services/media_state.py`
- `app/services/youtube_control.py`
- `docs/KNOWN_ISSUES.md`

## Audit Trail

- EXTRACTED: 51 (61%)
- INFERRED: 33 (39%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*