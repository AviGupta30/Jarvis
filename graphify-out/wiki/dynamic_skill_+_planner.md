# dynamic_skill + planner

> 20 nodes · cohesion 0.12

## Key Concepts

- **config.py** (20 connections) — `app/core/config.py`
- **planner.py** (19 connections) — `app/services/planner.py`
- **dynamic_skill.py** (18 connections) — `app/services/dynamic_skill.py`
- **groq** (11 connections)
- **get_task_ledger_for_prompt()** (8 connections) — `app/services/task_ledger.py`
- **_call_planner()** (4 connections) — `app/services/planner.py`
- **_llm_fix_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_llm_write_code()** (3 connections) — `app/services/dynamic_skill.py`
- **_strip_fences()** (3 connections) — `app/services/dynamic_skill.py`
- **_call_replanner()** (3 connections) — `app/services/planner.py`
- **app_memory** (2 connections)
- **Settings** (1 connections) — `app/core/config.py`
- **Dynamic Skill Engine for Jarvis 2.0 ------------------------------------- When…** (1 connections) — `app/services/dynamic_skill.py`
- **Ask the LLM to fix a broken script.** (1 connections) — `app/services/dynamic_skill.py`
- **Remove accidental markdown code fences if LLM adds them.** (1 connections) — `app/services/dynamic_skill.py`
- **Ask the LLM to write Python code for a given task.** (1 connections) — `app/services/dynamic_skill.py`
- **Jarvis Agentic Planner — The Brain for Complex Multi-Step Tasks…** (1 connections) — `app/services/planner.py`
- **Ask the LLM to produce a step-by-step plan.** (1 connections) — `app/services/planner.py`
- **Ask the LLM to replan after a failure.** (1 connections) — `app/services/planner.py`
- **Returns a compact, LLM-friendly summary of recent tasks for injection into…** (1 connections) — `app/services/task_ledger.py`

## Relationships

- [dag_executor + planner](dag_executor_+_planner.md) (13 shared connections)
- [voice_agent + download_kokoro](voice_agent_+_download_kokoro.md) (8 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (6 shared connections)
- [rag_memory + tool_runner](rag_memory_+_tool_runner.md) (3 shared connections)
- [task_ledger + rag_memory](task_ledger_+_rag_memory.md) (3 shared connections)
- [assignment_answers](assignment_answers.md) (2 shared connections)
- [repair + assignment_humanizer](repair_+_assignment_humanizer.md) (2 shared connections)
- [assignment_tool](assignment_tool.md) (2 shared connections)
- [content_humanizer + content-tools](content_humanizer_+_content-tools.md) (2 shared connections)
- [llm + llm-personality](llm_+_llm-personality.md) (2 shared connections)
- [ppt_tool](ppt_tool.md) (2 shared connections)
- [prompt_enhancement_library + skill_prompt_enhancer](prompt_enhancement_library_+_skill_prompt_enhancer.md) (2 shared connections)

## Source Files

- `app/core/config.py`
- `app/services/dynamic_skill.py`
- `app/services/planner.py`
- `app/services/task_ledger.py`

## Audit Trail

- EXTRACTED: 81 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*