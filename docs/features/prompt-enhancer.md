# Prompt enhancer (chat + floating Enhance button + Ctrl+Space overlay)

## Purpose
Rewrite a rough prompt into a clearer, stronger one for another AI (ChatGPT, Claude, Gemini, Copilot, coding agents) **without adding things the user didn't ask for**: no tech stack, no implementation steps, no invented features/numbers. The receiving AI decides the "how".

## Entry points
- **Floating "✦ Enhance" pill** (`prompt_enhancer_button.py`). It follows keyboard focus via UI Automation (polls `GetFocusedControl` every 200 ms): when the focused element is an editable prompt box in a target app, the pill appears just above the box's top-right corner (below / inside when there's no room) and follows it; it hides when focus leaves. Nothing happens until it is clicked.
  - **Targets** (`classify_app`): browsers matched by the address-bar URL (`AI_SITES`; ChatGPT tabs are titled by conversation, so titles are only a fallback), IDEs by exe (`IDE_EXES`: VS Code, Antigravity, Cursor, Windsurf, ...), AI desktop apps by exe (`AI_APP_EXES`) or exact product-name titles. `JARVIS_ENHANCER_SCOPE=all` = every text box in every app (terminals/password managers still excluded). Extra targets: `JARVIS_ENHANCER_APPS="foo.exe,some-site.com"`.
  - **Prompt box** (`is_prompt_box`): writable `EditControl`, or a focusable Group/Document with a TextPattern (Chromium contenteditable), never password fields, browser address bars or terminals. In IDEs (`_ide_allows`) only chat/agent inputs qualify: own name/class has a chat hint (Claude Code's webview input is `EditControl "Message input"`), or an ancestor class does, or it sits in a nested webview document. The Monaco code editor (`inputarea`, ancestor `editor-instance`) and xterm terminals never qualify.
  - **Click**: Ctrl+A/Ctrl+C in the box → `enhance_prompt_text()` → Ctrl+A/Ctrl+V → read the box back through UIA; if the text isn't there, fall back to `ValuePattern.SetValue`; if that fails too, the result is left on the clipboard ("Copied – press Ctrl+V"). Otherwise the user's clipboard is restored.
  - **Lifecycle**: spawned by `app/main.py` startup with `--parent-pid` (exits with the backend; disable with `JARVIS_ENHANCER_BUTTON=0`), and optionally at Windows login via `python -m app.services.prompt_enhancer_button --install-autostart` (Startup-folder shortcut → `pythonw`, no console; `--uninstall-autostart` removes it). A named mutex `Local\JarvisPromptEnhancerButton` keeps one instance (a second one waits 8 s, then exits). Calls Groq directly, so it works without the backend. Log: `app/memory/enhancer_button.log`.
  - Left-drag moves it (offset per site/app saved in `app/memory/enhancer_button.json`). Right-click: undo last enhance, copy last result, hide for this site/app (session), reset position.
- Chat: a message starting with "enhance " / "refine " is handled in `keyword_detect_tool`, which calls `enhance_prompt` and streams the result directly (no LLM rephrase).
- Router tool `enhance_prompt(raw_prompt)`.
- Popup (legacy, optional): `python -m app.services.prompt_overlay` (tkinter). **Ctrl+Space** toggles it; it posts "enhance …" to `{JARVIS_API_URL}/chat`.

## Pipeline (`skill_prompt_enhancer.enhance_prompt_text`)
`protect_blocks` (``` fenced code/logs → `[[BLOCK_n]]`, never paraphrased) → one Groq call (`gpt-oss-120b`, falls back to `gpt-oss-20b`; `reasoning_effort="low"`, `max_tokens=2048` because reasoning tokens count) with `ENHANCEMENT_SYSTEM_PROMPT` (DO / DO NOT ADD rules + few-shot examples) → `clean_output` (labels, quotes, non-breaking hyphens) → guards `check_for_hallucination` (chatbot/answer signals not present in the input) + `is_bloated` → one stricter retry (`RETRY_REMINDER`) → else return the **original** prompt → `restore_blocks`. `enhance_prompt()` wraps it with the `**ENHANCED PROMPT (DOMAIN)**:` header for chat and never raises; `enhance_prompt_text()` raises on API failure (the button shows "✗ Enhance failed"). `PROJECT_CONTEXT` is added only when the prompt says "jarvis".

## Gotchas
- "how do I…" prompts must never become "build…" commands (intent preservation; a note is added to the user message for how-to prompts).
- To change what the enhancer adds/omits, edit `ENHANCEMENT_SYSTEM_PROMPT` + its examples in `prompt_enhancement_library.py`. The 20b/120b models follow examples much more than rules.
- Verified live (2026-09-30): ChatGPT (`EditControl "Chat with ChatGPT"`, ProseMirror), Gemini (`"Enter a prompt for Gemini"`, ql-editor), Claude.ai (`"Write your prompt to Claude"`, tiptap), VS Code Claude Code (`"Message input"`). Not verified live: Copilot web (needed sign-in), Antigravity (wouldn't open a window from an automated session), Copilot Chat in VS Code (Monaco input, relies on the `chat`/`interactive` ancestor-class hint).
- UIA reports an empty box's **placeholder** as its value (e.g. Claude Code "Queue another message…"), so reading the value can't test emptiness; emptiness is detected by Ctrl+C not changing the clipboard sequence number.
- The pill window is `WS_EX_NOACTIVATE` and is shown/moved only with `SetWindowPos(... SWP_NOACTIVATE)`; Tk `deiconify()` would steal focus from the prompt box. `SetWindowPos` needs explicit ctypes argtypes (HWND_TOPMOST=-1 is pointer-sized on x64), otherwise it silently fails.
- Browser URL reads cost ~0.2 s, so `classify_app` is cached per window and re-run on title change at most once a second (Jarvis's own YouTube bridge rewrites the Edge title every second).
- Process is DPI-aware (`SetProcessDpiAwareness(2)`) so UIA rects, `GetWindowRect` and Tk coordinates match.
- Windows Store Python: `Popen([sys.executable, ...]).terminate()` may only kill the alias stub. The button relies on `--parent-pid` + the mutex, not on being killed by its parent. Testing scripts that send keys must verify the foreground window first (a new Edge window launched from a background process often doesn't get focus).

## Graphify
`graphify explain "enhance_prompt_text"` · `graphify explain "EnhanceButton"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/skill_prompt_enhancer.py` (125 lines): skill_prompt_enhancer.py
  L38 _call_groq() · L61 _is_how_to() · L69 _build_messages() · L88 enhance_prompt_text() · L117 enhance_prompt()
- `app/services/prompt_enhancement_library.py` (217 lines): prompt_enhancement_library.py
  L23 PROJECT_CONTEXT · L34 ENHANCEMENT_SYSTEM_PROMPT · L88 RETRY_REMINDER · L102 protect_blocks() · L113 restore_blocks() · L134 clean_output() · L150 CHATBOT_START_SIGNALS · L154 CHATBOT_SIGNALS · L162 check_for_hallucination() · L172 is_bloated() · L182 DOMAIN_KEYWORDS · L208 detect_domain()
- `app/services/prompt_enhancer_button.py` (932 lines): prompt_enhancer_button.py
  L72 AI_SITES · L83 AI_TITLE_WORDS · L110 EXTRA_URL_PARTS · L120 GAP · L121 MAX_BROWSER_CHARS · L125 KEY_COLOR · L126 PILL_BG · L127 PILL_HOVER · L128 ACCENT · L129 TEXT · L130 OK_GREEN · L131 ERR_RED · L144 _set_dpi_aware() · L154 _window_rect() · L166 _ctrl() · L173 _clip_get() · L188 _clip_set() · L204 _focus() · L216 _site_match() · L237 _title_match() · L245 _app_title_match() · L255 _browser_url() · L271 _exe_name() · L280 classify_app() · L302 _has_pattern() · L309 _is_editable() · L334 _hint_text() · L339 _ide_allows() · L372 is_prompt_box() · L385 _norm() · L389 _focused_text() · L407 _box_contains() · L419 _box_set_value() · L436 _load_state() · L443 _save_state() · L451 class EnhanceButton · (L474 .build, L511 ._render, L537 ._set_hover, L541 ._set_label, L550 ._move, L558 ._hide, L564 ._watch_loop, L580 ._set_target, L586 ._detect, L634 ._tick, L646 ._anchor, L664 ._update_position, L682 ._on_press, L686 ._on_motion, L693 ._on_release, L705 ._on_menu, L712 ._undo, L720 ._copy_last, L727 ._hide_here, L732 ._reset_pos, L738 ._click, L745 ._animate, L752 ._done, L756 ._enhance_worker, L808 ._paste_into, L838 .run) · L850 _acquire_single_instance() · L865 _startup_shortcut() · L869 install_autostart() · L882 uninstall_autostart() · L890 _setup_logging() · L902 main()
- `app/services/prompt_overlay.py` (362 lines): prompt_overlay.py
  L32 HOTKEY · L35 BG_DARK · L36 BG_CARD · L37 BG_INPUT · L38 BG_RESULT · L39 ACCENT · L40 ACCENT_HOVER · L41 ACCENT_2 · L42 TEXT_PRIMARY · L43 TEXT_MUTED · L44 BORDER · L45 SUCCESS · L46 FONT_FAMILY · L49 class PromptOverlay · (L57 ._build_window, L194 ._drag_start, L198 ._drag_motion, L204 .show, L220 .hide, L224 .toggle, L231 ._on_enter, L237 ._start_enhance, L250 ._call_backend, L273 ._append_result, L279 ._set_result, L286 ._enhance_done, L294 ._enhance_error, L299 ._extract_prompt, L308 ._copy_result, L317 ._inject_result, L340 .run) · L355 main()
<!-- AUTO:END -->
