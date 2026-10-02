# tools

> 7 nodes · cohesion 0.33

## Key Concepts

- **api/tools.py** (9 connections) — `app/api/tools.py`
- **fastapi** (5 connections)
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **pydantic** (4 connections)
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **BaseModel** (1 connections)
- **post** (1 connections)

## Relationships

- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (2 shared connections)
- [main](main.md) (2 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (2 shared connections)
- [memory](memory.md) (2 shared connections)
- [ppt_router + ppt_tool](ppt_router_+_ppt_tool.md) (2 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [tool_runner](tool_runner.md) (1 shared connections)

## Source Files

- `app/api/tools.py`

## Audit Trail

- EXTRACTED: 20 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*