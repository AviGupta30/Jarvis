# dark_enhancement + dark_video_enhancement

> 24 nodes · cohesion 0.17

## Key Concepts

- **dark_enhancement.py** (15 connections) — `app/services/dark_enhancement.py`
- **numpy** (14 connections)
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

- [benchmark + server](benchmark_+_server.md) (4 shared connections)
- [nlp_extractor + download_kokoro](nlp_extractor_+_download_kokoro.md) (1 shared connections)
- [whatsapp + dump_wa_ui](whatsapp_+_dump_wa_ui.md) (1 shared connections)
- [chat + chat-routing](chat_+_chat-routing.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [media-enhancement](media-enhancement.md) (1 shared connections)
- [content_humanizer](content_humanizer.md) (1 shared connections)
- [ppt_chart_engine](ppt_chart_engine.md) (1 shared connections)
- [fontmatch + fonts](fontmatch_+_fonts.md) (1 shared connections)
- [ingest](ingest.md) (1 shared connections)
- [measure](measure.md) (1 shared connections)
- [pipeline](pipeline.md) (1 shared connections)

## Source Files

- `app/services/dark_enhancement.py`
- `app/services/dark_video_enhancement.py`
- `app/services/media_enhancement.py`
- `docs/features/media-enhancement.md`

## Audit Trail

- EXTRACTED: 62 (93%)
- INFERRED: 5 (7%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*