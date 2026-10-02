# Agents: DAG executor, linear planner, dynamic skills

## Purpose
Multi-step execution when one tool isn't enough.

| Agent | Trigger | Behaviour |
|---|---|---|
| DAG (`dag_executor`) | `is_dag_task`: ≥5 words + conjunction + ≥2 domains (email/calendar/messaging/file/web/system) or multi-branch regex; excludes assignment/PPT/search | LLM plans nodes with `depends_on`; Kahn topo-sort into waves; `MAX_PARALLEL=2`; per-node retry (`RETRY_BACKOFF`) + `fallback_tool`; AGGREGATE node summarises; SSE events |
| Linear planner (`planner`) | chat.py step 7b (`is_complex_task`, no tool) and DAG fallback on plan failure/cycle | plan → execute step → on failure replan (max 2) → summary; yields plain sentences |
| Dynamic skill (`dynamic_skill`) | chat.py step 9 (automation words like rename/compress/batch) or `DYNAMIC` plan steps | reuse a saved skill from ChromaDB, else LLM writes Python → `safe_executor` AST sandbox → up to 3 self-fix retries → save on success |

## Data
Step results are referenced as `$var` in later step args (`store_result_as`). Learned skills live in ChromaDB `data/jarvis_memory/` (see memory.md).

## Gotchas
- Planner/DAG prompts list tools by hand (`PLANNER_PROMPT`, DAG prompt). Keep them in sync with the registry.
- Tools run via `tool_runner.run_tool`, so generator tools are fully consumed, which can be slow (PPT and assignment steps take minutes).
- The sandbox blocks deletes, exec/eval and system paths; see the `safe_executor.py` docstring.

## Graphify
`graphify explain "run_dag_plan"` · `graphify explain "run_agentic_plan"` · `graphify path "run_dynamic_skill" "execute_safe"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/dag_executor.py` (628 lines): dag_executor.py — Jarvis DAG-Based Multi-Step Agent Planner
  L48 MAX_PARALLEL · L49 RETRY_BACKOFF · L50 AGGREGATE_MODEL · L56 class DAGNode · L76 DAG_PLANNER_PROMPT · L154 AGGREGATE_PROMPT · L169 _call_dag_planner() · L188 _topological_sort() · L238 _resolve_args() · L257 _execute_node() · L307 _run_node_with_retry() · L340 _DAG_MULTI_BRANCH_PATTERNS · L349 _DAG_COMPOUND_VERBS · L360 _EXCLUDED_FROM_DAG · L372 is_dag_task() · L441 run_dag_plan() · L625 _sse()
- `app/services/planner.py` (464 lines): Jarvis Agentic Planner — The Brain for Complex Multi-Step Tasks
  L35 PLANNER_PROMPT · L143 REPLANNER_PROMPT · L159 _call_planner() · L186 _call_replanner() · L215 _execute_step() · L256 run_agentic_plan() · L350 is_complex_task()
- `app/services/dynamic_skill.py` (167 lines): Dynamic Skill Engine for Jarvis 2.0
  L25 SKILL_REUSE_THRESHOLD · L27 SKILL_WRITER_PROMPT · L69 SKILL_FIXER_PROMPT · L91 _llm_write_code() · L103 _llm_fix_code() · L115 _strip_fences() · L123 run_dynamic_skill()
- `app/services/safe_executor.py` (185 lines): Safe Code Executor for Jarvis
  L46 BLOCKED_SYSTEM_PATHS · L54 class SecurityError · L59 class SafetyVisitor · (L62 .visit_Call, L75 .visit_Import, L81 .visit_ImportFrom) · L87 _validate_code() · L96 execute_safe() · L169 _safe_open() · L179 _safe_import()
- `app/services/tool_runner.py` (43 lines): tool_runner.py — Async execution of TOOL_REGISTRY entries for orchestrators
  L19 _call_sync() · L26 run_tool()
<!-- AUTO:END -->
