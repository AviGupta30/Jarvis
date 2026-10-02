# Reusable task prompt (copy everything inside the box)

Replace `<<TASK>>` and `<<FEATURE>>`. The feature slugs are listed in `docs/FEATURES.md` (e.g. `ppt`, `whatsapp`, `memory`, `chat-routing`). For a cross-cutting task, list two slugs separated by a comma; if unsure, write `unknown`.

```
TASK: <<TASK>>
FEATURE: <<FEATURE>>

You have full access to this repo and my machine for this task. Don't ask for permission or confirmation. Make the changes, run what you need, and report at the end.

Work token-efficiently:
1. Read docs/features/<<FEATURE>>.md first (if FEATURE is "unknown", pick it from docs/FEATURES.md). Don't read other docs unless that one points you there.
2. Locate code with graphify before opening files: `graphify explain "<symbol>"`, `graphify affected "<symbol>"`, `graphify query "<question>" --budget 800`. If a name is ambiguous, use `path::symbol`.
3. Open source files only by line range, using the line numbers in the feature doc. Never read whole big files (ppt_tool.py, chat.py, tools.py, syllabus_auditor.py). Don't re-read files you've already seen, and don't spawn subagents.
4. Make the change following the project rules in CLAUDE.md, then verify it (run the relevant script/test, or a quick python -c check).
5. Keep the docs and graph in sync:
   - run `python scripts/refresh_docs.py`
   - update the hand-written sections of docs/features/<<FEATURE>>.md if behaviour, flow or gotchas changed
   - update docs/TOOLS.md if you added/renamed a tool, and docs/KNOWN_ISSUES.md if you found or fixed a bug
6. Final reply: 3–6 lines covering what changed (file:line), how you verified it, and anything left open. No code dumps.
```

## Notes
- The line "Don't ask for permission" tells Claude not to stop and ask *you* questions. Whether tool calls need approval is decided by Claude Code's permission mode (auto mode, or `/permissions` allow rules), not by prompt text.
- Example: `TASK: add a "neon_green" palette to the PPT engine` / `FEATURE: ppt`.
