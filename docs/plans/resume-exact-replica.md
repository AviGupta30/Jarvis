# Plan: exact design replication for the resume creator

Status (2026-10-03): **implemented as v1** in `app/services/resume_replica/` (ingest, measure, plate, fonts, fontmatch, pipeline, exact_render, integrate) and wired into `create_resume`; how it works is in `docs/features/resume-creator.md` → *Exact replica engine*. Built as planned: pixel measurement (no VLM), the "reference is the template" background plate with content erased, heading/icon/bullet/node assets cut from the reference, local font identification against ~456 Google families + Windows fonts, measured rhythm, PDF references, visible fallback + low-dpi warning, `scripts/replica_eval.py`. **Not built yet** (later milestones): the numeric calibration loop / fidelity score (§Step 4, §3), Set-of-Marks VLM labelling (rules alone are used), AI super-resolution, icon-library vector matching, DOCX references, horizontal contact strips, the PDF lossless text/vector path (PDFs are rasterised at 200 dpi instead). The orphaned scene-graph modules (`analyzer.py`, `compiler.py`, `repair.py`, `orchestrator.py`, `schema.py`, `bindings.py`, `storage.py`, `renderer.py`) are unused by v1.

Goal: any uploaded resume design (image, screenshot, phone photo, PDF) comes back as a resume with the **same design**: same page geometry, shapes, colours, fonts, sizes, spacing, heading treatment, skill graphics, icons and photo frame, filled with the user's own content. "Same" is defined by numbers (see *Fidelity contract*), not by eye.

---

## 1. Why the current creator can't do it (evidence)

The problem is the architecture. More vocabulary or prompt tweaks won't fix it.

| # | Root cause | Where | Evidence |
|---|---|---|---|
| 1 | **Describe-then-pick.** A VLM describes the image as ~60 enum choices (`layout`, `header`, `heading_style`, `skills_style`, `font: sans/serif/modern…`), and HTML is then built from a fixed template for each choice. Anything outside the vocabulary gets snapped to the nearest option. | `resume_builder._analyse_design` / `_merge_design`; the uncommitted `resume_replica/analyzer.py` does the same with a bigger enum list (`_REPLICA_DESIGN_PROMPT`) | Aanchal Gupta ref (`data/uploads/Screenshot_2026-10-03_120914_*.png`): headings are **white text on navy filled boxes**. Output `resume_avi_gupta_1791009596_p1.png` drew them as a left bar + coloured text. The job-title line and letter-spaced name were also lost. |
| 2 | **The small VLM is asked for geometry and typography.** A qwen-27B looking at a 1400px JPEG has to guess hexes, widths and font *categories*. Fonts can only ever be Roboto/Montserrat/Poppins/Playfair/Cormorant/JetBrains. | `_VISION_PROMPT`, `_FONTS` | A local probe on that same ref (2026-10-03, RapidOCR + pixel sampling) read `CONTACT` as bg `#0a3064` / fg `#fdfeff` at ~14pt in 12 s, with no LLM. The measurement is easy; the system just doesn't do it. |
| 3 | **Preset merge.** The analysis is merged over the "closest preset", so preset traits the reference doesn't have leak in. | `_closest_preset`, `_merge_design` | |
| 4 | **No numeric check.** Nothing measures whether the output matches the reference. The replica `repair.py` asks a VLM for a list of differences (an opinion, not a measurement), and it isn't wired in anywhere. | `resume_replica/repair.py`; `grep resume_replica app/` finds no importers | |
| 5 | **The fit loop rewrites the design after analysis.** It moves sections between columns, rebalances columns, and shrinks type to 0.74–0.8. | `_render_files`, `_balance_columns`, `_fit_render` | |
| 6 | **Silent preset fallback.** When vision fails (quota, error), the user gets a stock preset with no warning. | `_resolve_design` | Harper Russo ref (`Screenshot_2026-10-03_135251_*.png`, beige left sidebar) → `resume_siddharth_sharma_1791017087.pdf` is the blue `wave` preset; saved state shows `source: "wave"`. |
| 7 | **Low-resolution inputs are accepted silently.** | `_image_b64` | The Harper Russo ref is **220×320 px** (≈27 dpi for A4). |

The next output in that session (`1791009976`, new photo) had a dark full-width header and a right sidebar. If that run used the same reference, the analysis is also non-deterministic.

## 2. The new approach: measure, label, calibrate, transfer, verify

Treat the reference as a picture of a laid-out page and **reverse-engineer it**. Pixels give geometry, colour and typography. The VLM is used only for *semantics* (what each measured box *is*). A render-and-compare loop then tunes the replica until it numerically matches the reference, using the reference's **own text** so the two images are directly comparable. Only after that is the user's content poured in, with the design locked.

```
reference (png/jpg/pdf/docx)
  │  0 ingest: deskew, crop page, mm scale, DPI check, super-res if tiny; PDF → lossless path
  ▼
  1 MEASURE (local, deterministic)   regions+vector shapes · text runs+styles · graphics · icons · photo frame · fonts
  ▼
  2 LABEL (VLM on numbered boxes + rule fallback)   roles · sections · repeated item prototypes
  ▼
  3 SYNTHESISE → Replica IR v2 (scene graph)   fixed layer (absolute mm) + flow layer (columns, components, tokens)
  ▼
  4 CALIBRATE (render ghost content ↔ reference, optimise until the fidelity contract passes)
  ▼
  5 TRANSFER user content (design locked; overflow → condense content / page-2 master, never re-layout)
  ▼
  6 VERIFY (round-trip re-measure of our output, side-by-side + score in the reply)
```

### Step 0: Ingest and harden the input
- **PDF reference = lossless.** PyMuPDF `page.get_text("rawdict")` returns exact font names, sizes, colours and positions per span. `page.get_drawings()` returns exact vector fills and paths. `page.get_images()` returns the photo and icons. This skips OCR and guessing entirely and is the "truly exact" path. **DOCX** → PDF via Word COM (same pattern as the PowerPoint COM export), then the same path.
- **Images:** find the page quad (extend `_measure_frame`; add `cv2.findContours` + `warpPerspective` for phone photos of paper). Compute mm/px from the page height.
- **DPI gate:** effective dpi = page px height / 11.69. Below ~100 dpi, super-resolve ×4 for analysis only (Real-ESRGAN ONNX; `onnxruntime` is installed) and **tell the user** that thin rules and exact sizes are approximate, asking for a larger image or the PDF. Below ~40 dpi (e.g. 220×320), warn clearly before proceeding.
- Multi-page references: analyse page 1 as the master and page 2 (if given) as the continuation master.

### Step 1: Measure (local CV, no LLM)
All modules are local: `opencv-contrib`, `rapidocr-onnxruntime`, `numpy`, `scikit-learn`, `fonttools`, `torch` are already installed.

1. **Colour quantisation** in Lab (k-means, extend `_palette`), then connected components per colour cluster.
2. **Background regions and shapes:** large components → `path` nodes with exact geometry. Use `findContours` → `approxPolyDP` for straight edges, and least-squares cubic Bézier fitting for waves/curves (wave headers, diagonal banners, blobs, circles). **Gradients:** fit colour vs. position along the region's principal axis; low residual → linear/radial gradient with measured stops, otherwise solid.
3. **Text runs:** RapidOCR gives line boxes and text. Per line, measure:
   - font size from cap/x-height
   - weight from stroke width (distance transform of the binarised glyph mask)
   - colour from the glyph pixel cluster, background from the surrounding ring
   - letter spacing from glyph gaps (column projection) vs. the matched font's advance widths
   - case (from the OCR text), alignment (left/centre/right relative to the column edges), italic (shear moment)
4. **Graphics:**
   - rules and dividers (thin long components / Hough lines)
   - dots and nodes (circularity, `HoughCircles`)
   - bars (track + fill run on one row → fill %)
   - rings (annulus + arc coverage → %)
   - chips (rounded-rect outline around a text box → radius, border width, padding)
   - timeline (vertical line + nodes aligned with item titles)
5. **Icons:** small non-text components immediately left of a text line. First try to **match against an icon library** (bundle Lucide + Font Awesome Free SVGs; render candidates and pick the best IoU) to get a crisp vector of the same glyph. If nothing matches above threshold, crop it with alpha (recolourable mask).
6. **Photo frame:** the largest high-entropy region. Get the mask shape (circle-fit residual, rounded-rect corner radius, polygon vertex count → hexagon/diamond), border/ring width and colour from concentric annulus sampling, and exact mm box.
7. **Font identification (WhatTheFont-style, local):** for the name, headings, body and small labels, render the OCR'd string in candidate fonts at the measured size, align to the crop, and score by glyph IoU / chamfer distance. Candidates: ~150 popular Google Fonts plus every font installed in `C:\Windows\Fonts` plus anything the user drops into `data/fonts/`. Pick the top match per role, including weight. If the top score is below threshold (a commercial font we don't have), use the closest by metrics and correct width/height with CSS `@font-face { size-adjust; ascent-override }` and letter-spacing, so line breaks and block heights still match.
8. **Residual background plate.** Anything left that none of the above explains (textures, watercolour, illustrations, complex ornaments) is kept as a raster layer. The plate is the reference with text, photo, content-dependent graphics and already-vectorised regions masked out and inpainted (`cv2.inpaint` Telea; LaMa ONNX for big areas). This is the no-compromise catch-all: nothing visible is dropped just because it isn't in a vocabulary. Vector stays preferred, because it prints crisply.

Output: `measured.json` with regions, paths, text runs (+ styles), graphics, icons, photo, fonts, plate, and confidence per item.

### Step 2: Label (semantics only)
- **Set-of-Marks prompting:** draw numbered boxes over the measured text runs and graphics, send that image plus the OCR text list, and ask only *"what is box N"*: `name`, `job_title`, `section_heading:<key>`, `item_title`, `item_org`, `item_date`, `bullet`, `paragraph`, `contact:<email|phone|…>`, `skill_label`, `chip`, `decor`… Small VLMs are far more reliable at classifying given boxes than at describing a design. One call replaces today's two big calls plus the 3-round diff, which eases the Groq 200k/day cap. Use the strongest available model for this one call; it's cached per design.
- **Rule-based labeller as an always-available fallback**, so the design never depends on the VLM:
  - largest text = name; the line under it = title
  - repeated short uppercase lines with a shared distinct style = headings
  - bullet glyph = bullets; date regex = dates; email/phone/URL regex = contact
- **Structure:** columns (x-clustering of text-run left edges + background regions); sections (heading → following runs until the next heading in that column); **repeated item prototypes** (style-sequence pattern mining, e.g. `[item_title, item_date(right), item_org, bullet+]`); spacing tokens measured from box positions (heading→content gap, item gap, bullet gap, bullet indent, paragraph line-height).

### Step 3: Synthesise the Replica IR v2
Reuse the uncommitted `resume_replica` scene-graph schema (frames with absolute/flow/flex layout, `path`, `image`, `repeat`, `chart`, `style_registry`) and bump to `SCHEMA_VERSION = 2`.
- **Fixed layer** (page master, absolute mm): background regions, vector shapes, decor, rules, the background plate, header blocks, photo frame. Regions touching the page bottom or running full-height become page-spanning so they repeat on page 2 (keep the `_svg_bg` rule: Chromium does not repeat fixed elements with inline `<svg>`).
- **Flow layer:** column frames with measured x, width and padding; each section is a `repeat` of its measured component prototype. Every role gets a text style holding measured values: family, size, weight, colour, letter-spacing, line-height, case, alignment.
- **No preset merge.** Presets remain only for "no image" requests.

### Step 4: Calibrate (the core of "no compromise")
- Build **ghost content**: the reference's own OCR'd text, structured by the labels into the normal content JSON.
- Render the IR + ghost content in a **warm Playwright page** (`set_content` + screenshot at the reference's pixel size, ~0.2–0.3 s per iteration).
- Measure the error against the reference:
  - **Text boxes:** our boxes come straight from the DOM (`getBoundingClientRect` of each `data-f` span, so our side needs no OCR), matched to reference runs by role + text. Gives Δx, Δy, Δwidth and Δheight per run.
  - **Regions:** colour ΔE2000 and mask IoU per region.
  - **Global:** SSIM (greyscale) + Canny-edge IoU for rules and shapes.
- **Optimise** the continuous parameters with per-parameter coordinate descent / Nelder-Mead: font size and letter-spacing per role, line-heights, paddings, gaps, column widths, shape control points. The DOM box errors map almost directly to parameters (Δy of heading k → section gap; width ratio → size/spacing), so this converges in a few rounds. Budget ≤ 60 s, run **once per design**, cached by image SHA-1.
- If the contract still fails, run a semantic pass (the idea from `repair.py`, but given the numeric error heat-map) to catch a *missing kind* of element, e.g. a bracket ornament. Patch the IR and re-calibrate.
- If it still fails, **don't hide it**: return the result with its score and a side-by-side overlay, and point to the editor's Design mode (the uncommitted free-shape layer in `resume_builder.py`) for touch-ups.

### Step 5: Transfer the user's content (design locked)
- Reference sections the user has → same place, same component. User sections the reference lacks → clone the most similar prototype (same heading component) into the column where the reference keeps similar sections. Reference sections the user lacks → dropped (no placeholders), spacing tokens kept.
- **Overflow policy, in order:**
  1. fill the page with the same tokens
  2. continue on page 2 using the page-2 master
  3. if a page target is set, condense *content* (`_condense_content`) before touching the design
  4. only then shrink type, at most −5% from the calibrated sizes

  Never move sections between columns and never switch layout. Disable `_balance_columns`, main→sidebar moves and the 0.74 shrink in replica mode.
- **Photo:** the user's photo, face-centred (`_faces`) into the measured frame mask and aspect. No photo → the same frame with initials in the measured style.
- **Icons:** the reference's matched icons for the same contact types; a type the reference lacks → a library icon at the measured size and colour.

### Step 6: Verify every output
- **Round-trip check:** run Step 1 on our own output PNG and compare the extracted design tokens (region geometry and colours, font per role, sizes, heading treatment, graphics types) with the IR. Any token outside tolerance is a bug and is reported in the reply.
- The reply includes a **side-by-side (reference | replica) preview** and the fidelity score.

## 3. Fidelity contract (acceptance numbers)

These are checked on the ghost-content calibration render, at the reference's resolution.

| Metric | Pass |
|---|---|
| Text-run position error (p90) | ≤ 1.0 mm |
| Text-run height (font size) error (median) | ≤ 0.4 pt |
| Text-run box IoU (median) | ≥ 0.85 |
| Region colour ΔE2000 (every region) | ≤ 3 |
| Region mask IoU (backgrounds, shapes) | ≥ 0.92 |
| Font family per role | top-1 match, or glyph IoU ≥ 0.90 against the reference crop |
| Global SSIM (greyscale) | ≥ 0.90 |
| Element inventory | every measured element has a counterpart (no dropped heading boxes, rules, icons, decor) |
| User-content output | round-trip tokens equal to the IR within the same tolerances |

Honest limits, stated up front:
- **Different content can't be pixel-identical.** A longer name or more bullets moves things. What is guaranteed identical is the design system and component geometry, which is what the contract measures.
- **Fonts we don't have** (commercial faces) get the closest match with metric overrides, so line breaks and heights match while glyph shapes may differ slightly. Dropping the font file into `data/fonts/` makes it exact.
- **Tiny references** (< ~40 dpi) carry too little information for sub-millimetre precision. The user is told and asked for a bigger image or the PDF.

## 4. What to do with the uncommitted work (as of 2026-10-03)
- `app/services/resume_builder.py` (+423 lines, "free design layer" for the editor's Design mode with absolute mm shapes and per-element CSS overrides): keep it. It's the manual touch-up path, and it uses the same absolute-shape model as the fixed layer. Smoke-test it and commit it separately before replica work starts.
- `app/services/resume_replica/`:
  - **keep** `schema.py`, `storage.py`, `bindings.py`, `compiler.py`, `renderer.py` (the IR and render plumbing; extend the compiler with the fixed layer, plate, measured tokens, `@font-face` overrides and editor spans)
  - **replace** `analyzer.py` (enum VLM) with new modules: `ingest.py`, `measure.py`, `fonts.py`, `icons.py`, `label.py`, `structure.py`, `synth.py`, `calibrate.py`, `verify.py`
  - **demote** `repair.py` to the optional semantic pass in Step 4
  - **rewrite** `orchestrator.py` for the new flow
- Move the shared pixel helpers (`_palette`, `_measure_frame`, `_measure_band`, `_pixel_colors`, `_faces`) into `resume_replica/pixels.py` and have `resume_builder` import them from there, instead of the replica package importing private names from `resume_builder`.

## 5. Integration in Jarvis
- `create_resume`: a reference image/PDF goes to `resume_replica.create_replica_resume(...)`. The legacy `_resolve_design` stays only for no-image requests. If replica analysis fails, fall back to legacy **and say so in the reply** ("couldn't analyse the design: <reason>; used the closest preset; say *retry* to try again").
- Behind `RESUME_REPLICA=1` until the golden set passes, then the default.
- `resume_state.json` gets `replica_id`; the IR lives in `app/memory/replica_docs/<sha1>.json`. Follow-up edits ("add AWS to my resume"), the colour change and the visual editor (`editor_page`, `editor_save`, `_apply_op`) must route to the replica compiler when `replica_id` is set. The compiler already has `_REPLICA_EDIT` / `_ef` for `data-f` spans.
- Generator progress lines: "Measuring the layout…", "Matching fonts…", "Calibrating: 81% → 93%…", "Rendering…".
- Project rules: everything wrapped and returning strings; state via `resume_state.json` / `replica_docs`, not module globals (except the warm OCR model and browser, which are caches). Preload the OCR model lazily in a thread.
- Cost/time: first use of a design ≈ 60–90 s (OCR ~3 s warm, fonts ~5 s, calibration ≤ 60 s). A reused design takes normal render time. VLM: 1 labelling call (+ 1 optional semantic pass) instead of 2 + up to 3 diff calls.

## 6. Test harness (makes "exact" measurable and keeps it from regressing)
- **Golden set:** 30–40 references in `tests/resume_replica/golden/`, covering:
  - layouts: left/right sidebars, full-band and wave/diagonal/curve headers, timelines, two-page
  - graphics and type: bars/dots/rings/Venn/chips, serif/minimal, dark themes
  - inputs: phone photos of paper, screenshots with app chrome, tiny images, PDFs

  Start with the 8+ screenshots already in `data/uploads/`.
- `scripts/replica_eval.py`: runs Steps 0–4 on each reference and writes an HTML report (reference | replica | diff heat-map, every contract metric). It also stores a baseline JSON; a run fails if any metric regresses.
- **Synthetic round-trip tests (unlimited data):** generate random IRs, render them, run measure + label + synth, and compare to the source IR. This unit-tests Step 1 and Step 3 without hand labelling.
- Unit tests for the deterministic parts: gradient fit, Bézier fit, ring %, font matcher top-k on rendered samples, DPI gate.

## 7. Milestones (each ends with a measurable exit check)

| M | Work | Exit check |
|---|---|---|
| 0 | Stop silent compromises: announce fallbacks, DPI warning, accept PDF references (lossless path). Eval-harness skeleton + golden set. | Harper Russo case reports the failure instead of shipping `wave`; PDF refs extract exact fonts/colours |
| 1 | `ingest` + `measure` (regions, vector shapes, gradients, text runs + styles, graphics, photo frame, plate) | On 10 hand-checked refs: region ΔE ≤ 3, font size error ≤ 0.5 pt, all heading boxes/rules/icons found |
| 2 | `fonts` (local font matcher + metric overrides) + `icons` (library matching) | Font top-1 ≥ 80 %, top-3 ≥ 95 % on the golden set; icon match ≥ 90 % |
| 3 | `label` (Set-of-Marks VLM + rule fallback) + `structure` (columns, sections, item prototypes, spacing tokens) | Role accuracy ≥ 95 %; works with the VLM disabled at ≥ 85 % |
| 4 | `synth` → IR v2 + compiler extensions (fixed layer, plate, tokens, `@font-face` overrides) | Ghost render before calibration: SSIM ≥ 0.85 |
| 5 | `calibrate` (warm Playwright, DOM-box metrics, optimiser, semantic pass) | Fidelity contract passes on ≥ 90 % of the golden set |
| 6 | Content transfer + overflow policy + editor/edit routing + wiring behind `RESUME_REPLICA=1` | User-content outputs pass the round-trip check; editor round-trips |
| 7 | Round-trip verify + side-by-side in the reply, flip the default, docs (`refresh_docs.py`, feature doc, KNOWN_ISSUES, TOOLS) | Eval report green; the 3 failing cases in §1 visibly fixed |

Build order matters. M0 and the eval harness come first, so every later step is judged by numbers instead of by eye.
