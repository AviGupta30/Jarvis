# dark_enhancement + dark_video_enhancement

> 23 nodes · cohesion 0.18

## Key Concepts

- **dark_enhancement.py** (15 connections) — `app/services/dark_enhancement.py`
- **dark_video_enhancement.py** (12 connections) — `app/services/dark_video_enhancement.py`
- **get_all_enhancements()** (7 connections) — `app/services/dark_enhancement.py`
- **run_pipeline_b()** (7 connections) — `app/services/dark_enhancement.py`
- **process_video_smartly()** (7 connections) — `app/services/dark_video_enhancement.py`
- **media_enhancement.py** (7 connections) — `app/services/media_enhancement.py`
- **enhance_media()** (7 connections) — `app/services/media_enhancement.py`
- **_path_2_wavelet()** (4 connections) — `app/services/dark_enhancement.py`
- **run_pipeline_a()** (4 connections) — `app/services/dark_enhancement.py`
- **_enhance_frame()** (4 connections) — `app/services/dark_video_enhancement.py`
- **Flow** (4 connections) — `docs/features/media-enhancement.md`
- **_apply_gamma()** (3 connections) — `app/services/dark_enhancement.py`
- **_path_1_retinex()** (3 connections) — `app/services/dark_enhancement.py`
- **_reencode_to_h264()** (3 connections) — `app/services/dark_video_enhancement.py`
- **cv2** (3 connections)
- **_fusion_and_polish()** (2 connections) — `app/services/dark_enhancement.py`
- **_normalize_to_8bit()** (2 connections) — `app/services/dark_enhancement.py`
- **_get_ffmpeg_binary()** (2 connections) — `app/services/dark_video_enhancement.py`
- **_apply_hsv_brightening()** (1 connections) — `app/services/dark_enhancement.py`
- **ndarray** (1 connections)
- **Re-encode a video to H.264 MP4 so browsers can play it.** (1 connections) — `app/services/dark_video_enhancement.py`
- **Enhance a dark image or video using the dark enhancement pipeline. It returns a…** (1 connections) — `app/services/media_enhancement.py`
- **pywt** (1 connections)

## Relationships

- [acoustic_tripwire](acoustic_tripwire.md) (2 shared connections)
- [benchmark + download_kokoro](benchmark_+_download_kokoro.md) (2 shared connections)
- [task_ledger + test_task_resumption](task_ledger_+_test_task_resumption.md) (1 shared connections)
- [dump_wa_ui + test_wa](dump_wa_ui_+_test_wa.md) (1 shared connections)
- [dag_executor](dag_executor.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [media-enhancement](media-enhancement.md) (1 shared connections)

## Source Files

- `app/services/dark_enhancement.py`
- `app/services/dark_video_enhancement.py`
- `app/services/media_enhancement.py`
- `docs/features/media-enhancement.md`

## Audit Trail

- EXTRACTED: 50 (91%)
- INFERRED: 5 (9%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*