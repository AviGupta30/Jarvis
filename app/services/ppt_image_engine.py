"""
ppt_image_engine.py — Semantic Image-Slide Matcher for JARVIS PPT Engine
=========================================================================
Isolated per Architecture Rule #4. Zero imports from other tool modules.

Matches user-uploaded images to the best-fit content slides using:
  1. Explicit slide references in user hints (e.g. "slide 3", "for the intro slide")
  2. Keyword overlap between user hint + filename and slide title + visual_suggestion
  3. Aspect-ratio reading via PIL for fluid geometry decisions

Public API:
    build_image_descriptors(paths, hints) -> list[ImageDescriptor]
    match_images_to_slides(descriptors, slides) -> (image_map, overflow_images)
    get_aspect_ratio(path) -> float
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ─── Data Model ───────────────────────────────────────────────────────────────

@dataclass
class ImageDescriptor:
    """All metadata about one uploaded image."""
    path: str
    hint: str                       # User-provided description (may be empty)
    keywords: list[str] = field(default_factory=list)
    aspect_ratio: float = 1.78      # width / height (defaults to 16:9)
    width: int = 1920
    height: int = 1080
    target_slide: Optional[int] = None  # Explicit 1-based slide number if user said "slide 3"


# ─── Helpers ──────────────────────────────────────────────────────────────────

_STOP_WORDS = frozenset({
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "may", "might", "shall", "of", "in", "on", "at",
    "to", "for", "with", "by", "from", "this", "that", "these", "those",
    "and", "or", "but", "not", "so", "if", "as", "into", "about", "image",
    "photo", "picture", "photograph", "img", "screenshot", "slide", "slides",
    "put", "use", "show", "place", "add", "include", "attach",
})

# Layout names that support an image slot (used when slide reference points
# to a text-only layout that needs to be adapted)
_IMAGE_CAPABLE_LAYOUTS = {
    "aesthetic_split", "aesthetic_showcase", "aesthetic_flow",
    "aesthetic_grid", "aesthetic_pitch", "aesthetic_metrics",
}


def _extract_keywords(text: str) -> list[str]:
    """Extract meaningful 3+ character alpha tokens, filtering stop-words."""
    words = re.findall(r"\b[a-zA-Z]{3,}\b", text.lower())
    return [w for w in words if w not in _STOP_WORDS]


def _parse_slide_ref(hint: str) -> Optional[int]:
    """
    Detect explicit slide assignment in the user hint.

    Recognised patterns (case-insensitive):
        "slide 3", "slide #3", "for slide 3", "3rd slide",
        "slide3", "s3", "on slide 5"
    Returns 1-based slide number, or None if not detected.
    """
    hint_l = hint.lower().strip()

    # "slide 3", "slide#3", "slide-3"
    m = re.search(r"\bslide\s*[#\-]?\s*(\d+)\b", hint_l)
    if m:
        return int(m.group(1))

    # "3rd slide", "2nd slide"
    m = re.search(r"\b(\d+)\s*(?:st|nd|rd|th)?\s+slide\b", hint_l)
    if m:
        return int(m.group(1))

    # "s3", "s12" (shorthand)
    m = re.match(r"^s(\d+)$", hint_l.strip())
    if m:
        return int(m.group(1))
        
    # Explicit title/cover slide references
    if any(kw in hint_l for kw in ["title slide", "cover slide", "first slide", "intro slide"]):
        return 1

    return None


def _parse_slide_ref_by_title(hint: str, slides: list[dict]) -> Optional[int]:
    """
    Try to match vague slide references like "intro slide", "conclusion",
    "the market slide" against slide titles using keyword overlap.
    Returns 0-based slide index, or None.
    """
    hint_kws = set(_extract_keywords(hint))
    if not hint_kws:
        return None

    best_idx, best_score = None, 0
    for i, s in enumerate(slides):
        title_kws = set(_extract_keywords(s.get("title", "")))
        score = len(hint_kws & title_kws)
        if score > best_score:
            best_score = score
            best_idx = i

    # Only use title-based matching if there's at least 1 keyword overlap
    return best_idx if best_score >= 1 else None


def get_aspect_ratio(path: str) -> tuple[float, int, int]:
    """
    Return (aspect_ratio, width_px, height_px) for an image.
    Falls back to (1.78, 1920, 1080) if PIL is unavailable or file is unreadable.
    """
    try:
        from PIL import Image
        with Image.open(path) as img:
            w, h = img.size
            return w / max(h, 1), w, h
    except Exception:
        return 1.78, 1920, 1080


# ─── Public API ───────────────────────────────────────────────────────────────

def build_image_descriptors(
    paths: list[str],
    hints: list[str],
) -> list[ImageDescriptor]:
    """
    Build an ImageDescriptor for each uploaded image.

    Args:
        paths: Absolute file paths of uploaded images.
        hints: Parallel list of user-provided descriptions (may contain empty strings).
               Shorter than paths → trailing images get empty hints.

    Returns:
        List of ImageDescriptor objects with keywords, aspect ratio, and any
        explicit slide target already resolved.
    """
    descriptors: list[ImageDescriptor] = []

    for i, path in enumerate(paths):
        hint = (hints[i] if i < len(hints) else "") or ""

        # Explicit slide number check
        target_slide = _parse_slide_ref(hint)

        # Keywords: user hint + filename stem (underscores/dashes → spaces)
        stem = Path(path).stem.replace("_", " ").replace("-", " ")
        combined = f"{hint} {stem}"
        keywords = _extract_keywords(combined)

        # Physical dimensions
        ratio, w, h = get_aspect_ratio(path)

        descriptors.append(ImageDescriptor(
            path=path,
            hint=hint,
            keywords=keywords,
            aspect_ratio=ratio,
            width=w,
            height=h,
            target_slide=target_slide,
        ))

    return descriptors


def _slide_score(img_keywords: list[str], slide: dict) -> float:
    """
    Score relevance of an image to a slide using keyword overlap.
    Returns a float in [0, 1+] — higher is more relevant.
    """
    slide_text = (
        f"{slide.get('title', '')} "
        f"{slide.get('visual_suggestion', '')} "
        f"{slide.get('description', '')}"
    ).lower()
    slide_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", slide_text)) - _STOP_WORDS

    if not img_keywords or not slide_words:
        return 0.0

    img_set = set(img_keywords)
    overlap = img_set & slide_words

    # Jaccard-style score biased toward image keyword coverage
    return len(overlap) / max(len(img_set), 1)


def match_images_to_slides(
    descriptors: list[ImageDescriptor],
    slides: list[dict],
) -> tuple[dict, list[ImageDescriptor]]:
    """
    Assign images to slides intelligently.

    Assignment priority:
      1. Explicit slide number in user hint ("slide 3")
      2. Title-keyword match in user hint ("intro slide", "market overview")
      3. Keyword overlap score between image keywords and slide content
      4. Round-robin fallback among remaining eligible slides

    Multiple images can be assigned to the same slide if the user explicitly
    requests it (e.g. two images both say "slide 3"). The first image is the
    primary; subsequent ones are stored in "extra_image_paths" on the slide.

    Returns:
        image_map:  { slide_index (0-based): ImageDescriptor }  (primary image only)
        overflow:   [ImageDescriptor] that could not be matched to any slide
    """
    n = len(slides)

    # Collect which slides are EXPLICITLY requested by any image hint
    explicit_targets = set()
    for desc in descriptors:
        if desc.target_slide is not None:
            explicit_targets.add(desc.target_slide - 1)  # 0-based

    # Slides eligible for auto-assignment:
    #   • Skip the title slide (index 0) UNLESS explicitly targeted
    #   • Skip the conclusion slide (last slide) UNLESS explicitly targeted
    #   • Skip slides already assigned an image
    eligible: list[int] = [
        i for i in range(0, n)
        if not slides[i].get("image_path")
        and (i in explicit_targets or (i != 0 and i != n - 1))
    ]

    image_map: dict[int, ImageDescriptor] = {}
    used_slides: set[int] = set()
    overflow: list[ImageDescriptor] = []
    remaining: list[ImageDescriptor] = []

    # ── Pass 1: Explicit numeric slide references ──────────────────────────────
    for desc in descriptors:
        if desc.target_slide is not None:
            idx = desc.target_slide - 1  # convert to 0-based
            if 0 <= idx < n:
                if idx not in used_slides:
                    # Primary image for this slide
                    image_map[idx] = desc
                    used_slides.add(idx)
                    if idx in eligible:
                        eligible.remove(idx)
                else:
                    # Secondary image for same slide — store on slide dict directly
                    extra = slides[idx].setdefault("extra_image_paths", [])
                    extra.append(desc.path)
            else:
                # Slide number out of range → treat as remaining
                remaining.append(desc)
        else:
            remaining.append(desc)

    # ── Pass 2: Title-keyword matching for hints that name a slide ─────────────
    still_remaining: list[ImageDescriptor] = []
    for desc in remaining:
        if not desc.hint:
            still_remaining.append(desc)
            continue

        stem_kws = set(_extract_keywords(
            Path(desc.path).stem.replace("_", " ").replace("-", " ")
        ))
        hint_only_kws = set(desc.keywords) - stem_kws
        if not hint_only_kws:
            still_remaining.append(desc)
            continue

        hint_only = " ".join(hint_only_kws)
        idx = _parse_slide_ref_by_title(hint_only, slides)

        if idx is not None and idx not in used_slides and idx in eligible:
            image_map[idx] = desc
            used_slides.add(idx)
            eligible.remove(idx)
        else:
            still_remaining.append(desc)

    # ── Pass 3: Keyword-overlap scoring ───────────────────────────────────────
    final_overflow: list[ImageDescriptor] = []
    for desc in still_remaining:
        if not eligible:
            final_overflow.append(desc)
            continue

        best_idx, best_score = None, -1.0
        for idx in eligible:
            s = _slide_score(desc.keywords, slides[idx])
            if s > best_score:
                best_score = s
                best_idx = idx

        if best_idx is not None and best_score >= 0.0:
            # Accept even score=0 (round-robin fallback) when eligible slides exist
            image_map[best_idx] = desc
            used_slides.add(best_idx)
            eligible.remove(best_idx)
        else:
            final_overflow.append(desc)

    return image_map, final_overflow
