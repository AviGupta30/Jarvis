# dark_video_enhancement + media_enhancement

> 14 nodes · cohesion 0.26

## Key Concepts

- **dark_video_enhancement.py** (12 connections) — `app/services/dark_video_enhancement.py`
- **get_all_enhancements()** (7 connections) — `app/services/dark_enhancement.py`
- **process_video_smartly()** (7 connections) — `app/services/dark_video_enhancement.py`
- **media_enhancement.py** (7 connections) — `app/services/media_enhancement.py`
- **enhance_media()** (7 connections) — `app/services/media_enhancement.py`
- **run_pipeline_a()** (4 connections) — `app/services/dark_enhancement.py`
- **_enhance_frame()** (4 connections) — `app/services/dark_video_enhancement.py`
- **Flow** (4 connections) — `docs/features/media-enhancement.md`
- **_reencode_to_h264()** (3 connections) — `app/services/dark_video_enhancement.py`
- **cv2** (3 connections)
- **_get_ffmpeg_binary()** (2 connections) — `app/services/dark_video_enhancement.py`
- **ndarray** (1 connections)
- **Re-encode a video to H.264 MP4 so browsers can play it.** (1 connections) — `app/services/dark_video_enhancement.py`
- **Enhance a dark image or video using the dark enhancement pipeline. It returns a…** (1 connections) — `app/services/media_enhancement.py`

## Relationships

- [dark_enhancement](dark_enhancement.md) (8 shared connections)
- [social_content_manager + ui_inspector](social_content_manager_+_ui_inspector.md) (2 shared connections)
- [acoustic_tripwire](acoustic_tripwire.md) (1 shared connections)
- [message_reader + reply_generator](message_reader_+_reply_generator.md) (1 shared connections)
- [chat + youtube_control](chat_+_youtube_control.md) (1 shared connections)
- [tools](tools.md) (1 shared connections)
- [media-enhancement](media-enhancement.md) (1 shared connections)

## Source Files

- `app/services/dark_enhancement.py`
- `app/services/dark_video_enhancement.py`
- `app/services/media_enhancement.py`
- `docs/features/media-enhancement.md`

## Audit Trail

- EXTRACTED: 34 (87%)
- INFERRED: 5 (13%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*