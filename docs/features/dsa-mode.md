# DSA / LeetCode enforcer mode

## Purpose
LeetCode discipline mode: Jarvis opens LeetCode and enforces solving N questions.

## Flow
`activate_dsa_mode(num_questions)` → `DSAEnforcer.start_mode` (singleton via `get_dsa_enforcer()`): Selenium Edge with its own profile (`%LOCALAPPDATA%/Jarvis_DSA_Profile`), background `_run_enforcement_loop` thread → `_check_if_solved`, hides topic tags/hints (`_hide_tags`, `_disable_hint_buttons`), `_monitor_tab_switching`. `deactivate_dsa_mode()` → `stop_mode`. `dsa_status()` reads progress from the neural cache.

## Data
State is published to neural cache keys under namespace `dsa_mode` (`active`, `num_questions`, `completed`, TTL 24h). The cache is optional; calls are skipped if the server is down.

## Gotchas
- Needs Edge + webdriver-manager (downloads the driver). LeetCode DOM changes break the selectors.

## Graphify
`graphify explain "DSAEnforcer"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/dsa_enforcer.py` (318 lines)
  L18 _CACHE_NS · L21 _cache_set() · L31 _cache_del() · L40 class DSAEnforcer · (L50 .start_mode, L99 .stop_mode, L115 ._get_problem_slug, L119 ._run_enforcement_loop, L196 ._check_if_solved, L217 ._hide_tags, L237 ._show_tags, L257 ._disable_hint_buttons, L277 ._enable_hint_buttons, L293 ._monitor_tab_switching) · L316 get_dsa_enforcer()
- `app/services/tools.py` (1217 lines): Jarvis Tool Registry — All callable actions Jarvis can perform.  *(filtered to this feature)*
  L930 cache_set() · L956 cache_get() · L979 get_dsa_cache_status()
<!-- AUTO:END -->
