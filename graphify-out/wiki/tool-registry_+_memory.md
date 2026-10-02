# tool-registry + memory

> 18 nodes · cohesion 0.12

## Key Concepts

- **recall_memory()** (14 connections) — `app/api/memory.py`
- **Memory: RAG, facts, task ledger, resume, skills** (7 connections) — `docs/features/memory.md`
- **Gotchas** (7 connections) — `docs/features/tool-registry.md`
- **Tool registry & adding tools** (7 connections) — `docs/features/tool-registry.md`
- **_mail_tool()** (6 connections) — `app/services/tools.py`
- **Calling tools from code** (3 connections) — `docs/features/tool-registry.md`
- **Gotchas** (2 connections) — `docs/features/memory.md`
- **Adding a tool (checklist)** (2 connections) — `docs/features/tool-registry.md`
- **Semantic search over all stored conversation turns. Returns the most relevant…** (1 connections) — `app/api/memory.py`
- **Email tools: try the real Gmail API (gmail_tool) first, fall back to opening…** (1 connections) — `app/services/tools.py`
- **memory.md** (1 connections) — `docs/features/memory.md`
- **API** (1 connections) — `docs/features/memory.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/memory.md`
- **Graphify** (1 connections) — `docs/features/memory.md`
- **tool-registry.md** (1 connections) — `docs/features/tool-registry.md`
- **Files & symbols (auto-generated, line numbers are current)** (1 connections) — `docs/features/tool-registry.md`
- **Graphify** (1 connections) — `docs/features/tool-registry.md`
- **Purpose** (1 connections) — `docs/features/tool-registry.md`

## Relationships

- [memory + rag_memory](memory_+_rag_memory.md) (4 shared connections)
- [chat-routing + chat](chat-routing_+_chat.md) (4 shared connections)
- [gmail_tool + memory_tool](gmail_tool_+_memory_tool.md) (3 shared connections)
- [chat + KNOWN_ISSUES](chat_+_KNOWN_ISSUES.md) (3 shared connections)
- [agents + tool_runner](agents_+_tool_runner.md) (2 shared connections)
- [tools + whatsapp_smart](tools_+_whatsapp_smart.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [chat + llm](chat_+_llm.md) (1 shared connections)
- [assignment_pipeline + assignment_tool](assignment_pipeline_+_assignment_tool.md) (1 shared connections)
- [ppt_content](ppt_content.md) (1 shared connections)
- [ppt_tool + tools](ppt_tool_+_tools.md) (1 shared connections)

## Source Files

- `app/api/memory.py`
- `app/services/tools.py`
- `docs/features/memory.md`
- `docs/features/tool-registry.md`

## Audit Trail

- EXTRACTED: 22 (55%)
- INFERRED: 18 (45%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*