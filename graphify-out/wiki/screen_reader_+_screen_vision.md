# screen_reader + screen_vision

> 4 nodes · cohesion 0.50

## Key Concepts

- **describe_screen_for_llm()** (8 connections) — `app/services/screen_reader.py`
- **describe_screen_vlm()** (5 connections) — `app/services/screen_vision.py`
- **Returns a clean, LLM-optimized description of the current screen. Used as…** (1 connections) — `app/services/screen_reader.py`
- **Lightweight passive description — used as context injection in chat.py. Always…** (1 connections) — `app/services/screen_vision.py`

## Relationships

- [screen_reader](screen_reader.md) (3 shared connections)
- [chat](chat.md) (2 shared connections)
- [tools](tools.md) (1 shared connections)
- [dag_executor + planner](dag_executor_+_planner.md) (1 shared connections)
- [screen_vision](screen_vision.md) (1 shared connections)
- [voice_agent + acoustic_tripwire](voice_agent_+_acoustic_tripwire.md) (1 shared connections)

## Source Files

- `app/services/screen_reader.py`
- `app/services/screen_vision.py`

## Audit Trail

- EXTRACTED: 9 (75%)
- INFERRED: 3 (25%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*