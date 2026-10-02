# Dark image/video enhancement

## Purpose
Brighten dark photos/videos.

## Flow
Upload in UI → `[ATTACHED_FILE: path]` + "enhance/fix … image/video/dark" (chat.py keyword) or router `enhance_media(file_path)` → `media_enhancement.enhance_media`:
- Image (png/jpg/jpeg/webp): `dark_enhancement.get_all_enhancements` (pipeline A: HSV brightening + gamma; pipeline B: Retinex path + wavelet path → fusion/polish).
- Video: `dark_video_enhancement.process_video_smartly` (frame-sampled enhancement) → ffmpeg (imageio-ffmpeg) H.264 re-encode for browser playback.
- Output goes to `data/uploads/enhanced_*` (served at `/media/...`). It returns markdown that the UI renders with a download button, streamed directly (no LLM rephrase).

## Graphify
`graphify explain "enhance_media"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/media_enhancement.py` (61 lines)
  L6 enhance_media()
- `app/services/dark_enhancement.py` (159 lines)
  L6 _apply_hsv_brightening() · L21 _normalize_to_8bit() · L24 _apply_gamma() · L29 run_pipeline_a() · L43 _path_1_retinex() · L67 _path_2_wavelet() · L90 _fusion_and_polish() · L126 run_pipeline_b() · L133 get_all_enhancements()
- `app/services/dark_video_enhancement.py` (116 lines)
  L7 _enhance_frame() · L14 _get_ffmpeg_binary() · L21 _reencode_to_h264() · L41 process_video_smartly()
<!-- AUTO:END -->
