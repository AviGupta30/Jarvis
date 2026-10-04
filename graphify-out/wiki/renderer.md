# renderer

> 12 nodes · cohesion 0.23

## Key Concepts

- **renderer.py** (10 connections) — `app/services/resume_replica/renderer.py`
- **render_replica()** (7 connections) — `app/services/resume_replica/renderer.py`
- **render_to_screenshot()** (6 connections) — `app/services/resume_replica/renderer.py`
- **_launch_browser()** (4 connections) — `app/services/resume_replica/renderer.py`
- **_count_pages_and_fill()** (3 connections) — `app/services/resume_replica/renderer.py`
- **_save_pngs()** (3 connections) — `app/services/resume_replica/renderer.py`
- **renderer.py — Browser rendering and output verification for replica resumes.…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Launches Chromium (or msedge fallback). Same as resume_builder._launch.** (1 connections) — `app/services/resume_replica/renderer.py`
- **Uses PyMuPDF (fitz) to count pages and measure fill of last page. Returns…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Extracts PNG previews from the PDF using PyMuPDF. Returns list of PNG file…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Renders the compiled HTML to PDF + PNG previews. Uses Playwright Chromium (or…** (1 connections) — `app/services/resume_replica/renderer.py`
- **Renders the HTML to a PNG screenshot (full page). Used by the repair loop to…** (1 connections) — `app/services/resume_replica/renderer.py`

## Relationships

- [storage + orchestrator](storage_+_orchestrator.md) (4 shared connections)
- [repair](repair.md) (2 shared connections)
- [social_content_manager + content-tools](social_content_manager_+_content-tools.md) (1 shared connections)
- [message_reader + thread_extractor](message_reader_+_thread_extractor.md) (1 shared connections)
- [assignment_humanizer + task_ledger](assignment_humanizer_+_task_ledger.md) (1 shared connections)

## Source Files

- `app/services/resume_replica/renderer.py`

## Audit Trail

- EXTRACTED: 24 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*