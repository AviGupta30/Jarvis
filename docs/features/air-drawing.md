# Air drawing (webcam hand drawing)

## Purpose
Draw in the air with your hand via the webcam, inside the web UI.

## Flow
"open air drawing" / "draw in the air" → router `open_air_drawing()` → returns the `[OPEN_AIR_DRAWING]` marker → `App.jsx` opens `AirDrawingApp` full-screen.
Pipeline in the browser: `handTracking.js` (MediaPipe Hands) → `gestureInterpreter.js` (landmarks → gestures) → `gestureController.js` → `interactionEngine.js` → `drawingEngine.js` / `strokeManager.js` (capture) / `strokeRefiner.js` (smoothing) / `shapeManager.js` (shape detection) / `transformEngine.js` (move/scale/rotate). UI: `components/` (CameraView, DrawingCanvas, HandSkeleton, ControlPanel, HelpPanel).

## Gotchas
- `3D/`, `AirDrawer_ref/`, `AirDrawer_ref_new/` are older standalone copies (`3D/dist` is still mounted at `/airdrawing` by main.py). The live code is `frontend/src/AirDrawing`.
- `HandSkeleton.jsx` has a parse issue at line ~44 per graphify's extractor (check if you touch it).

## Graphify
`graphify explain "TransformEngine"` · `graphify explain "StrokeManager"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/air_drawing_tool.py` (8 lines)
  L1 open_air_drawing()
- `frontend/src/AirDrawing/AirDrawingApp.jsx` (275 lines)
  L12 AirDrawingApp · L70 handleSave
- `frontend/src/AirDrawing/components/CameraView.jsx` (84 lines)
  L4 CameraView
- `frontend/src/AirDrawing/components/ControlPanel.jsx` (422 lines)
  L76 handlePlaceText · L393 Section
- `frontend/src/AirDrawing/components/DrawingCanvas.jsx` (266 lines)
  L111 saveCurrentPath · L210 _eraseNearShapes
- `frontend/src/AirDrawing/components/HandSkeleton.jsx` (122 lines)
  L30 toScreen
- `frontend/src/AirDrawing/components/HelpPanel.jsx` (129 lines)
  L32 HelpPanel
- `frontend/src/AirDrawing/modules/drawingEngine.js` (335 lines)
  L3 DrawingEngine
- `frontend/src/AirDrawing/modules/gestureController.js` (80 lines)
  L9 GestureController
- `frontend/src/AirDrawing/modules/gestureInterpreter.js` (202 lines)
  L18 GestureInterpreter
- `frontend/src/AirDrawing/modules/handTracking.js` (50 lines)
  L2 getHandsConstructor · L7 HandTracker
- `frontend/src/AirDrawing/modules/interactionEngine.js` (61 lines)
  L1 InteractionEngine
- `frontend/src/AirDrawing/modules/shapeManager.js` (102 lines)
  L5 ShapeManager
- `frontend/src/AirDrawing/modules/strokeManager.js` (161 lines)
  L1 StrokeManager
- `frontend/src/AirDrawing/modules/strokeRefiner.js` (166 lines)
  L8 StrokeRefiner
- `frontend/src/AirDrawing/modules/transformEngine.js` (226 lines)
  L5 TransformEngine
<!-- AUTO:END -->
