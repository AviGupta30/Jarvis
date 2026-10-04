"""
renderer.py — Browser rendering and output verification for replica resumes.

Handles:
- Rendering compiled HTML to PDF and PNG using Playwright (same as resume_builder.py)
- Basic fidelity verification (does the output look reasonable?)
- Fit loop for page targets
"""
from __future__ import annotations
import os
import time
import json


def render_replica(
    html: str,
    output_stem: str,
    out_dir: str,
    target_pages: int | None = None
) -> dict:
    """
    Renders the compiled HTML to PDF + PNG previews.
    Uses Playwright Chromium (or msedge fallback), same as resume_builder._render_files.

    Returns:
    {
        "pdf": str,          # absolute path to PDF
        "html": str,         # absolute path to saved HTML
        "pngs": [str, ...],  # paths to PNG previews (one per page, max 3)
        "pages": int,        # total page count
        "fit_scale": float   # the scale that was used (1.0 or lower if shrunk)
    }

    Fit loop:
    - Render at scale 1.0
    - If more pages than target: return the result (the compile step already set scale)
    - If only 1 page needed and output has multiple pages: note it but don't re-render
      (the compiler's scale was set by the orchestrator)

    This function does NOT do content condensation (that's the orchestrator's job).
    It DOES do the browser launch, page.pdf(), and PyMuPDF PNG extraction.
    """
    os.makedirs(out_dir, exist_ok=True)
    html_path = os.path.join(out_dir, f"{output_stem}.html")
    pdf_path  = os.path.join(out_dir, f"{output_stem}.pdf")

    # Save HTML to disk (data-URIs are embedded so no external refs needed)
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html)

    pdf_bytes: bytes = b""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = _launch_browser(pw)
            try:
                page = browser.new_page()
                page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle", timeout=30000)
                pdf_bytes = page.pdf(
                    format="A4",
                    print_background=True,
                    margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"},
                )
                page.close()
            finally:
                browser.close()
    except Exception as e:
        print(f"[replica/renderer] Playwright render failed: {e}")
        return {
            "pdf": "",
            "html": html_path,
            "pngs": [],
            "pages": 0,
            "fit_scale": 1.0,
        }

    with open(pdf_path, "wb") as fh:
        fh.write(pdf_bytes)

    n_pages, _fill = _count_pages_and_fill(pdf_bytes)

    if target_pages and n_pages > target_pages:
        print(f"[replica/renderer] {n_pages} pages exceeds target {target_pages}; caller should re-compile at lower scale")

    pngs = _save_pngs(pdf_path, max_pages=3)

    return {
        "pdf": pdf_path,
        "html": html_path,
        "pngs": pngs,
        "pages": n_pages,
        "fit_scale": 1.0,
    }


def render_to_screenshot(html: str) -> bytes | None:
    """
    Renders the HTML to a PNG screenshot (full page).
    Used by the repair loop to compare against the reference.
    Returns PNG bytes or None if rendering failed.
    """
    import tempfile
    tmp_html = os.path.join(tempfile.gettempdir(), f"replica_shot_{int(time.time()*1000)}.html")
    try:
        with open(tmp_html, "w", encoding="utf-8") as fh:
            fh.write(html)

        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = _launch_browser(pw)
            try:
                page = browser.new_page(viewport={"width": 794, "height": 1123})
                page.goto(f"file:///{tmp_html.replace(os.sep, '/')}", wait_until="networkidle", timeout=30000)
                png_bytes = page.screenshot(full_page=True)
                page.close()
                return png_bytes
            finally:
                browser.close()
    except Exception as e:
        print(f"[replica/renderer] screenshot failed: {e}")
        return None
    finally:
        try:
            os.remove(tmp_html)
        except Exception:
            pass


def _launch_browser(pw):
    """
    Launches Chromium (or msedge fallback). Same as resume_builder._launch.
    """
    try:
        return pw.chromium.launch(headless=True)
    except Exception:
        return pw.chromium.launch(headless=True, channel="msedge")


def _count_pages_and_fill(pdf_bytes: bytes) -> tuple[int, float]:
    """
    Uses PyMuPDF (fitz) to count pages and measure fill of last page.
    Returns (n_pages, last_page_fill_ratio).
    """
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        n_pages = doc.page_count
        if n_pages == 0:
            doc.close()
            return 0, 0.0
        last_page = doc[n_pages - 1]
        # Measure fill: render the last page to a small pixmap and check
        # how many pixels are non-white (content area coverage)
        mat = fitz.Matrix(0.5, 0.5)  # 50% scale for speed
        pix = last_page.get_pixmap(matrix=mat, alpha=False)
        import struct
        samples = pix.samples
        total_px = pix.width * pix.height
        non_white = 0
        stride = 3  # RGB
        for i in range(0, len(samples), stride):
            r, g, b = samples[i], samples[i + 1], samples[i + 2]
            if not (r > 240 and g > 240 and b > 240):
                non_white += 1
        fill = non_white / max(total_px, 1)
        doc.close()
        return n_pages, fill
    except Exception as e:
        print(f"[replica/renderer] page count failed: {e}")
        return 1, 1.0


def _save_pngs(pdf_path: str, max_pages: int = 3) -> list[str]:
    """
    Extracts PNG previews from the PDF using PyMuPDF.
    Returns list of PNG file paths.
    """
    pngs: list[str] = []
    try:
        import fitz
        doc = fitz.open(pdf_path)
        n = min(doc.page_count, max_pages)
        stem = os.path.splitext(pdf_path)[0]
        for i in range(n):
            page = doc[i]
            mat = fitz.Matrix(2.0, 2.0)  # 2× scale for crisp preview
            pix = page.get_pixmap(matrix=mat, alpha=False)
            png_path = f"{stem}_p{i + 1}.png"
            pix.save(png_path)
            pngs.append(png_path)
        doc.close()
    except Exception as e:
        print(f"[replica/renderer] PNG extraction failed: {e}")
    return pngs


def verify_render_basic(html: str) -> tuple[bool, str]:
    """
    Performs basic sanity checks on the rendered HTML before sending to browser.
    Checks:
    - HTML is non-empty
    - Contains expected structural elements (body, at least one section)
    - No obvious broken elements
    Returns (is_valid, reason_if_invalid).
    """
    if not html or not html.strip():
        return False, "HTML is empty"

    lower = html.lower()

    if "<body" not in lower:
        return False, "HTML missing <body> element"

    if "<html" not in lower:
        return False, "HTML missing <html> element"

    # Must contain at least one meaningful content block
    has_section = any(marker in lower for marker in (
        'class="sec', 'class="cols', "<aside", "<main", "<section",
    ))
    if not has_section:
        return False, "HTML has no recognisable content sections"

    # Rough check: the file should be at least 500 bytes of meaningful content
    if len(html) < 500:
        return False, f"HTML suspiciously short ({len(html)} bytes)"

    # Check for broken template placeholders
    if "{{" in html or "}}" in html:
        return False, "HTML contains unresolved template placeholders"

    return True, ""
