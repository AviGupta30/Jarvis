# Web UI (React/Vite)

## Purpose
React 19 + Vite + Tailwind 4 chat UI. Run: `cd frontend && npm run dev`.

## Key behaviour (App.jsx)
- `API_BASE` from `src/config.js` (`VITE_API_URL`, default `http://127.0.0.1:8000`).
- `handleSendMessage`: POST `/chat`, reads the stream; the first chunk starting with `data: {` → DAG mode (`handleDagEvent` → `DagPlanPanel`), else raw text is appended to the last assistant message.
- `handleFileUpload`: POST `/upload` → inserts `[ATTACHED_FILE: path]` (optionally `| DESCRIPTION: …`) into the prompt. `isPPTRequest` + theme image → POST `/ppt/create`.
- Tripwire toggle/calibrate → `/tripwire/*`.
- `[OPEN_AIR_DRAWING]` in a reply → opens `AirDrawing/AirDrawingApp` overlay (marker stripped).
- `ChatMessage.jsx`: react-markdown + GFM + syntax highlighting. `MemorySidebar.jsx`: POST `/memory/ingest` (checks JSON `status`).

## Gotchas
- `3D/` and `AirDrawer_ref*/` are old copies; edit `frontend/src/AirDrawing`.
- Build check without touching the repo: `npx vite build --outDir <temp dir>`.

## Graphify
`graphify explain "App"` (component-level only; handlers nested inside App, like handleSendMessage, are not graph nodes, so use the line table below)

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `frontend/src/App.jsx` (933 lines)
  L8 App · L44 handleTripwireToggle · L55 handleTripwireCalibrate · L105 handleFileUpload · L167 isResumeRequest · L174 isPPTRequest · L182 appendMsg · L191 handleSendMessage · L376 handleDagEvent
- `frontend/src/DagPlanPanel.jsx` (259 lines)
  L16 DagPlanPanel · L33 getDisplayWaves · L67 getNodeStatus · L102 toolIcon
- `frontend/src/MemorySidebar.jsx` (157 lines)
  L5 MemorySidebar · L10 handleIngest
- `frontend/src/ChatMessage.jsx` (127 lines)
  L7 ChatMessage
- `frontend/src/config.js` (2 lines)
<!-- AUTO:END -->
