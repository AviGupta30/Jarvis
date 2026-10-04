# social_content_manager + tools

> 15 nodes · cohesion 0.18

## Key Concepts

- **typing** (30 connections)
- **api/tools.py** (9 connections) — `app/api/tools.py`
- **social_content_manager.py** (9 connections) — `app/services/social_content_manager.py`
- **generate_social_content()** (6 connections) — `app/services/social_content_manager.py`
- **refine_social_content()** (5 connections) — `app/services/social_content_manager.py`
- **execute_tool()** (4 connections) — `app/api/tools.py`
- **build_prompt()** (4 connections) — `app/services/social_content_manager.py`
- **call_llm()** (4 connections) — `app/services/social_content_manager.py`
- **ToolExecuteRequest** (3 connections) — `app/api/tools.py`
- **BaseModel** (1 connections)
- **post** (1 connections)
- **Refine an existing piece of social media content based on user instructions.…** (1 connections) — `app/services/social_content_manager.py`
- **Calls Groq Llama 3.3 70B directly for maximum speed. No slow fallbacks.** (1 connections) — `app/services/social_content_manager.py`
- **Generate professional, multi-version social media content.** (1 connections) — `app/services/social_content_manager.py`
- **google_generativeai** (1 connections)

## Relationships

- [benchmark + server](benchmark_+_server.md) (5 shared connections)
- [rag_memory + mysql_db](rag_memory_+_mysql_db.md) (3 shared connections)
- [tools](tools.md) (3 shared connections)
- [dag_executor + dynamic_skill](dag_executor_+_dynamic_skill.md) (3 shared connections)
- [ppt_router](ppt_router.md) (2 shared connections)
- [resume_router](resume_router.md) (1 shared connections)
- [main + screen_vision](main_+_screen_vision.md) (1 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [web_search](web_search.md) (1 shared connections)
- [content-tools](content-tools.md) (1 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (1 shared connections)
- [memory + CLAUDE](memory_+_CLAUDE.md) (1 shared connections)

## Source Files

- `app/api/tools.py`
- `app/services/social_content_manager.py`

## Audit Trail

- EXTRACTED: 56 (92%)
- INFERRED: 5 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*