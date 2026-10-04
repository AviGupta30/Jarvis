# voice_agent

> 6 nodes · cohesion 0.40

## Key Concepts

- **stream_chat()** (9 connections) — `scripts/voice_agent.py`
- **on_event()** (4 connections) — `scripts/voice_agent.py`
- **say_text()** (4 connections) — `scripts/voice_agent.py`
- **AsyncClient** (1 connections)
- **POST /chat with the spoken language, speak the reply into `ch` as it streams.…** (1 connections) — `scripts/voice_agent.py`
- **pusher()** (1 connections) — `scripts/voice_agent.py`

## Relationships

- [voice_agent](voice_agent.md) (4 shared connections)
- [main](main.md) (2 shared connections)
- [voice](voice.md) (1 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (1 shared connections)

## Source Files

- `scripts/voice_agent.py`

## Audit Trail

- EXTRACTED: 13 (93%)
- INFERRED: 1 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*