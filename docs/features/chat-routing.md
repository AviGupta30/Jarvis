# Chat pipeline & routing (/chat)

## Purpose
Single entry point for UI, voice agent and prompt overlay: `POST /chat {prompt}` → streamed reply. Decides *which* tool/agent handles a message.

## Flow (`chat_endpoint`, order matters, first hit wins)
1. `[ATTACHED_FILE: path | DESCRIPTION: …]` → text files read via `file_ops.read_file` and appended.
2. Pending state machines (module globals): `api_note_flow`, `api_whatsapp_call_flow`, `api_whatsapp_flow`. Then **YouTube mode** (`youtube_control.youtube_session_active()` + `parse_youtube_followup()`, state in `app/memory/youtube_session.json`); see `os-control.md`.
3. New note / WhatsApp call / send intents → start those flows.
4. Resume detection (`task_ledger` + `resume_detector`) → prepends prior-task context.
5. `dag_executor.is_dag_task` → multi-intent DAG, SSE JSON events.
6. `keyword_detect_tool()` regex cascade (returns None early if `planner.is_complex_task`).
7. `llm.check_for_tool_intent()` LLM router (JSON mode, `TOOL_ROUTER_PROMPT`).
7b. No tool + `is_complex_task` → stream `planner.run_agentic_plan`.
8. Run `TOOL_REGISTRY[name](**args)`: generators streamed raw; some tools return directly; result logged to task ledger.
9. No tool + automation words → `dynamic_skill.run_dynamic_skill`.
10. Context (tool result, pgvector RAG, screen description, ledger) → `llm.generate_chat_response` stream.

## Response formats
Plain text tokens for normal replies. `data: {json}\n\n` SSE for DAG (`thinking|plan|node_start|node_done|node_failed|narration|aggregate|error|fallback|done`). The frontend decides by the first chunk.

## Change recipes
- New keyword phrase: add a branch inside `keyword_detect_tool` **above** any broader pattern that would catch it first (e.g. the generic "open X" and "play X" handlers).
- New tool for the LLM router: add one line to `TOOL_ROUTER_PROMPT` (personality.py). Keep it terse, since the prompt costs tokens on every message (Groq TPM limit 8k/min).

## Gotchas
- `conversation_history` + flow dicts are shared by all clients (by design).
- The yes/no confirm lists include Hindi words (`haan`, `nahi`, `kar do`).
- `scripts/test_routing.py` is a manual keyword-router check.

## Graphify
`graphify explain "chat_endpoint"` · `graphify explain "keyword_detect_tool"` · `graphify affected "check_for_tool_intent"`
Related: tool-registry.md, agents.md, llm-personality.md

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/api/chat.py` (1929 lines)
  L24 class ChatRequest · L36 _clean_yt_query() · L46 detect_whatsapp_call() · L74 detect_whatsapp_send() · L95 detect_note_intent() · L109 _named_app() · L118 _media_target() · L143 keyword_detect_tool() · L1242 _run_media() · L1247 _run_direct_tool() · L1263 _media_intent_for() · L1281 _explicit_platform() · L1293 _to_platform() · L1320 _media_compound() · L1379 _run_direct_tools() · L1398 chat_endpoint() · L1925 clear_history()
- `app/services/llm.py` (366 lines): llm.py — Jarvis LLM Brain  *(filtered to this feature)*
  L182 check_for_tool_intent()
- `app/services/personality.py` (264 lines): personality.py — Jarvis Character & Personality Engine
  L13 JARVIS_SYSTEM_PROMPT · L72 TOOL_ROUTER_PROMPT · L212 get_context_aware_prompt()
- `app/main.py` (273 lines)
  L42 read_root() · L47 upload_file() · L81 _on_screen_alert() · L94 startup_event() · L182 shutdown_event() · L204 get_alerts() · L226 tripwire_status() · L236 tripwire_enable() · L250 tripwire_disable() · L261 tripwire_calibrate()
<!-- AUTO:END -->
