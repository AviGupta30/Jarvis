# main

> 6 nodes · cohesion 0.33

## Key Concepts

- **tripwire_status()** (4 connections) — `app/main.py`
- **get_alerts()** (3 connections) — `app/main.py`
- **get** (3 connections)
- **read_root()** (2 connections) — `app/main.py`
- **Frontend polls this endpoint to receive proactive JARVIS screen alerts. e.g.…** (1 connections) — `app/main.py`
- **Return current acoustic tripwire state for the frontend toggle.** (1 connections) — `app/main.py`

## Relationships

- [main + screen_vision](main_+_screen_vision.md) (3 shared connections)
- [main](main.md) (1 shared connections)

## Source Files

- `app/main.py`

## Audit Trail

- EXTRACTED: 9 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*