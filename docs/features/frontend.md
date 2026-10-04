# Web UI (React/Vite)

## Purpose
React 19 + Vite + Tailwind 4 + framer-motion chat UI (redesigned 2026-10-04: dark aurora theme, Geist/Instrument Serif fonts, sidebar + floating composer). Run: `cd frontend && npm run dev`.

## Layout
- `App.jsx`: state + streaming. `components/Sidebar.jsx` (modes, Air Drawing, Memory, resume editor link, acoustic-wake toggle/calibrate, backend online dot), `components/Composer.jsx` (attachments tray, `+` upload menu, Tools/mode chip, option pills, mic, send/stop), `components/EmptyState.jsx` (orb + greeting + per-mode suggestion cards), `components/MemoryPanel.jsx` (right drawer: `/memory/stats`, `/memory/recall`, `/memory/forget`, `/memory/ingest`), `components/Toasts.jsx`, `components/Orb.jsx`.
- Theme colours are CSS variables (`--accent`, `--accent-2`, `--accent-soft`) set from the active mode, so the orb, glow, focus ring and buttons recolour per mode. Design tokens/classes (`glass`, `glass-strong`, `menu-surface`, `ring-gradient`, `prose-jarvis`, `caret`) live in `src/index.css`.

## Modes (`src/modes.js`, like Gemini's Deep Research / Image modes)
Each entry in `MODES` defines `uploads` (what the `+` menu offers), `options` (pill dropdowns), `suggestions`, `placeholder`, `accent`. **Resume/PPT inputs only appear in their mode**; Chat mode's `+` menu offers general files and links to the other modes. `buildRequest()` turns text + attachments + options into `{route: 'chat'|'ppt', body, display}`:
- **Resume Creator** → `/chat`. Uploads: design reference (`DESCRIPTION: resume design reference`), photo, logo, details docs (plain tag so `/chat` reads the text). Options: template (`in the <name> template`), pages (`single page` / `2 pages`). Text that looks like details (email/phone/newline/>160 chars or uploads) → `Create my resume … using these details: …`; a short instruction → `Update my resume: …`.
- **PPT Generator** → `/ppt/create` with `style` (13 `ppt_designer.THEMES`), `purpose`, `N slides` in the prompt, `theme_image_path`, `image_paths` + captions. A `.pptx/.potx` template or a source document → `/chat` instead (only chat.py reads those); the theme image is skipped then (a note shows). After a deck is made (`hasDeck`, persisted), edit-like text ("change the title of slide 2…") goes to `/chat` → `ppt_edit`.
- **Deep Research** → `search the web: …` (`agentic_web_action`). **Humanizer** → `humanize this text: …`. **Assignment** → `do my assignment from <uploaded filename>` (no tag, see Gotchas).
- **Chat** keeps the old auto-routing: `isPPTRequest` text → `/ppt/create` (images become slide images/theme). While typing, `suggestMode()` offers a "Switch to …" chip.

## Key behaviour (App.jsx)
- `API_BASE` from `src/config.js` (`VITE_API_URL`, default `http://127.0.0.1:8000`).
- `runRequest`: POST, reads the stream; first chunk starting `data: {` → DAG mode (`handleDagEvent`), else text appended to the last assistant message. **DAG state is stored on the assistant message** (`msg.dag`), so earlier plans stay visible; `DagPlanPanel` folds itself when complete. AbortController → Stop button (`_Stopped._`). Each assistant message keeps its `request`, so Regenerate re-sends it.
- `handleFileUpload(files, kind)`: POST `/upload` per file with an uploading chip; single-kind uploads (design/photo/logo/theme/template/assignment) replace the previous one. Drag-and-drop anywhere and pasting files into the textarea use `kindForFile()` to pick the kind for the current mode. Switching mode drops attachments the new mode doesn't accept.
- Polls `/tripwire/status` every 5 s (also the backend-online heartbeat) and `/alerts?clear=true` every 6 s (screen-watcher alerts → toasts).
- Browser dictation (Web Speech API, Chrome/Edge) on the mic button. Shortcuts: Enter send, Shift+Enter newline, Ctrl+Shift+O new chat (also `DELETE /chat/history`), Ctrl+B sidebar, `/` focus input.
- Messages, mode, mode options and `hasDeck` persist in `localStorage['jarvis.ui.v2']` (attachment blob URLs are dropped, so old image thumbnails show as file chips).
- `[OPEN_AIR_DRAWING]` in a reply → opens `AirDrawing/AirDrawingApp` overlay (marker stripped).
- `ChatMessage.jsx`: react-markdown + GFM; code blocks with copy button; links to `.pptx/.pdf/.docx/…` render as file chips, `/resume/editor` links as a button; images/videos get a download bar.

## Gotchas
- `3D/` and `AirDrawer_ref*/` are old copies; edit `frontend/src/AirDrawing`. AirDrawing still relies on `.glass-meta` in `index.html` and the Outfit/JetBrains Mono/Pacifico fonts.
- Popovers sit inside the composer's `backdrop-filter`, so they can't blur what's behind them: use `menu-surface` (opaque), not `glass-strong`.
- `.glass*`/`.menu-surface` are unlayered CSS, so they beat Tailwind utilities (which are in `@layer utilities`); override their background in CSS, not with a `bg-*` class.
- Assignment: chat.py's `is_complex_task()` sends "do my assignment from x.pdf" to the planner as soon as anything else is in the prompt (extra words, "ppt", or the PDF text that `/chat` appends for an `[ATTACHED_FILE]` tag). So Assignment mode sends only the bare command, and there is no PPT-output option. See KNOWN_ISSUES.
- Build check without touching the repo: `npx vite build --outDir <temp dir>`. Visual check: run `npx vite --port 5199` and screenshot with Playwright, mocking `**/chat` and `**/upload` with `page.route` to avoid side effects.

## Graphify
`graphify explain "buildRequest"` · `graphify explain "Composer"` · `graphify explain "App"` (handlers nested inside App, like runRequest, are listed in the line table below)

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `frontend/src/App.jsx` (571 lines)
  L17 load · L18 save · L19 uid · L22 useSpeech · L26 toggle · L49 App · L80 dismissToast · L126 handleTripwireToggle · L140 handleTripwireCalibrate · L185 onScroll · L196 patchLast · L203 appendMsg · L206 handleDagEvent · L237 runRequest · L299 handleSendMessage · L318 handleRegenerate · L325 handleStop · L327 handleNewChat · L338 handleModeChange · L346 setOption · L349 handleFileUpload · L369 addFilesAuto
- `frontend/src/DagPlanPanel.jsx` (145 lines)
  L23 toolIcon · L36 NodeCard · L61 DagPlanPanel · L80 getDisplayWaves · L97 getNodeStatus
- `frontend/src/modes.js` (312 lines)
  L22 cap · L139 kindForFile · L141 has · L169 isResumeRequest · L176 isPPTRequest · L184 isPPTEdit · L189 suggestMode · L198 fwd · L199 tag · L200 withTags · L201 pick · L207 buildRequest
- `frontend/src/components/Composer.jsx` (319 lines)
  L10 Popover · L36 MenuItem · L56 OptionPill · L86 AttachmentChip · L119 Composer · L141 pickUpload · L150 submit
- `frontend/src/components/EmptyState.jsx` (59 lines)
  L5 greeting · L16 EmptyState
- `frontend/src/components/MemoryPanel.jsx` (185 lines)
  L6 Stat · L15 MemoryPanel · L23 loadStats · L39 handleRecall · L57 handleForget · L74 handleIngest
- `frontend/src/components/Orb.jsx` (12 lines)
  L3 Orb
- `frontend/src/components/Sidebar.jsx` (137 lines)
  L9 Section · L18 Item · L41 Sidebar
- `frontend/src/components/Toasts.jsx` (40 lines)
  L12 Toasts
- `frontend/src/ChatMessage.jsx` (193 lines)
  L12 useCopy · L14 copy · L20 CodeBlock · L97 Attachments · L125 ChatMessage
- `frontend/src/config.js` (2 lines)
<!-- AUTO:END -->
