"""
ppt_studio.py — Orchestrator for the PPT v6 engine (create / follow-up edit / undo)
==================================================================================
create(): request → profile (purpose + density) → content (the user's own content is
          used VERBATIM; the LLM only fills what is missing) → images assigned to
          slides → theme (or the user's .pptx template) → render → persist.
edit():   loads the last deck spec, applies the change (ppt_content.apply_edit),
          re-renders to the same file, keeps a 10-step undo history.

State lives in data/ppt_decks/state.json (not module globals), so follow-ups work
across restarts and from both UI and voice.
"""
from __future__ import annotations

import base64
import json
import queue
import re
import threading
import time
from pathlib import Path
from typing import Optional

from app.services import ppt_content as pc
from app.services.ppt_designer import DeckRenderer, THEMES, resolve_theme, theme_from_palette, prepare_image

_ROOT = Path(__file__).resolve().parents[2]
_STATE_DIR = _ROOT / "data" / "ppt_decks"
_STATE = _STATE_DIR / "state.json"
_IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff")
_TPL_EXT = (".pptx", ".potx", ".pptm", ".potm")


# ══════════════════════════════════════════════════════════════════════════════
#  STATE
# ══════════════════════════════════════════════════════════════════════════════
def _load_state() -> dict:
    try:
        return json.loads(_STATE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_state(state: dict):
    _STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = _STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(_STATE)


def has_active_deck(max_age_hours: Optional[float] = None) -> bool:
    cur = _load_state().get("current") or {}
    if not cur.get("deck"):
        return False
    if max_age_hours is not None and time.time() - float(cur.get("time") or 0) > max_age_hours * 3600:
        return False
    return True


def current_deck() -> Optional[dict]:
    return _load_state().get("current")


def _push(state: dict, entry: dict):
    hist = state.get("history", [])
    if state.get("current"):
        hist.append(state["current"])
    state["history"] = hist[-10:]
    state["current"] = entry


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def _with_progress(fn, *args, **kwargs):
    """Run fn(progress=cb) in a thread, yield progress strings live; result in holder['v']."""
    q: queue.Queue = queue.Queue()
    holder: dict = {}

    def work():
        try:
            holder["v"] = fn(*args, progress=q.put, **kwargs)
        except Exception as e:
            holder["e"] = e
        finally:
            q.put(None)

    threading.Thread(target=work, daemon=True).start()
    while True:
        m = q.get()
        if m is None:
            break
        yield m
    if "e" in holder:
        raise holder["e"]
    return holder.get("v")


def _desktop() -> Path:
    for p in (Path.home() / "Desktop", Path.home() / "OneDrive" / "Desktop"):
        if p.exists():
            return p
    return Path.home()


def _out_path(title: str, output_path: Optional[str]) -> str:
    if output_path:
        return output_path
    safe = re.sub(r"[^\w\- ]+", "", title or "Presentation").strip().replace(" ", "_")[:60] or "Presentation"
    p = _desktop() / f"{safe}.pptx"
    k = 2
    while p.exists():
        p = _desktop() / f"{safe}_{k}.pptx"
        k += 1
    return str(p)


def _topic_from_command(cmd: str) -> str:
    t = re.sub(r"(?i)^\s*(jarvis[,\s]+)?(please\s+)?(can you\s+)?(make|create|build|generate|design|prepare|do)\s+"
               r"(me\s+)?(a|an|the)?\s*(\d+[\s-]*slides?\s*)?(ppt|powerpoint|presentation|deck|slides?|slide deck|pitch deck)"
               r"\s*(of\s+\d+\s+slides?\s*)?(on|about|for|regarding|covering)?\s*", "", cmd or "").strip()
    return t or cmd


def _caption(path: str) -> str:
    """Short vision caption for an image with no user description (best effort)."""
    try:
        from groq import Groq
        from app.core.config import settings
        p, _ = prepare_image(path)
        if not p:
            return ""
        from PIL import Image
        import io
        with Image.open(p) as im:
            im = im.convert("RGB")
            im.thumbnail((768, 768))
            buf = io.BytesIO()
            im.save(buf, "JPEG", quality=80)
        b64 = base64.b64encode(buf.getvalue()).decode()
        r = Groq(api_key=settings.GROQ_API_KEY).chat.completions.create(
            model=settings.GROQ_VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "text", "text": "In at most 14 words, say what this image shows so it can be placed on the "
                                         "right presentation slide. Start with its type: photo, logo, chart, diagram, "
                                         "screenshot, team photo, product, or illustration."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}]}],
            max_tokens=60, temperature=0.2)
        txt = (r.choices[0].message.content or "").strip()
        txt = re.sub(r"<think>.*?</think>", "", txt, flags=re.S).strip()
        return txt[:140]
    except Exception as e:
        print(f"[ppt_studio] caption failed for {path}: {e}")
        return ""


def _collect_attachments(req: dict, image_paths, image_descriptions, template_path, theme_image_path):
    imgs, tpl, theme_img = [], template_path, theme_image_path
    seen = set()
    pairs = list(zip(image_paths or [], (image_descriptions or []) + [""] * len(image_paths or [])))
    pairs += [(a["path"], a["desc"]) for a in req["attachments"]]
    for p, d in pairs:
        p = (p or "").strip().strip('"')
        if not p or p in seen or not Path(p).exists():
            continue
        seen.add(p)
        low = p.lower()
        if low.endswith(_TPL_EXT):
            tpl = tpl or p
        elif low.endswith(_IMG_EXT):
            if re.search(r"\b(theme|colou?r scheme|colou?rs|palette|style reference|design reference|reference design|reference|like this|same (?:design|style|look)|similar|inspiration|design like|make it look)\b",
                         (d or "").lower()) and not theme_img:
                theme_img = p
            else:
                imgs.append({"path": p, "desc": d or ""})
    return imgs, tpl, theme_img


def _images_per_slide(ins: dict, imgs: list[dict], n: int) -> dict:
    """How many images each slide will get (from explicit instructions / descriptions) — told to the designer."""
    per: dict[int, int] = {}
    if ins.get("images_only_on") and 1 <= ins["images_only_on"] <= n:
        return {ins["images_only_on"]: len(imgs)}
    for i, im in enumerate(imgs):
        k = ins.get("image_slides", {}).get(i)
        if not k and not im.get("auto"):
            m = re.search(r"slide\s*(?:no\.?|number|#)?\s*(\d{1,2})", (im["desc"] or "").lower())
            k = int(m.group(1)) if m else None
        if k and 1 <= k <= n:
            per[k] = per.get(k, 0) + 1
    return per


def _reference_theme(t: dict) -> dict:
    """A design-reference image gives the accents; keep the canvas clean (white/near-white) like the reference."""
    from app.services.ppt_designer import _lum, _finish_theme
    t = dict(t)
    if _lum(t["bg"]) > 0.55:
        t.update(bg="FFFFFF", surface="F5F7FA", surface2="EDF1F6", text="111827", muted="4B5563", line="E3E8EF")
    t.update(head_font="Segoe UI Semibold", body_font="Segoe UI")
    t.pop("series", None)
    return _finish_theme(t)


def _assign_images(deck: dict, imgs: list[dict], count_locked: bool, ins: Optional[dict] = None):
    """Put each image on its best slide. Explicit instructions win. Mutates deck; returns notes."""
    slides = deck["slides"]
    notes = []
    n = len(slides)
    free = []
    ins = ins or {}
    if ins.get("images_only_on") and 1 <= ins["images_only_on"] <= n:
        target = slides[ins["images_only_on"] - 1]
        logo_like = [im for im in imgs if re.search(r"(^|[_\- ])logo([_\- ]|$)", Path(im["path"]).stem.lower())]
        for im in logo_like:
            deck["logo"] = im["path"]
        target["images"] = [im["path"] for im in imgs if im not in logo_like]
        if ins.get("image_section", {}).get(ins["images_only_on"]):
            target["image_section"] = ins["image_section"][ins["images_only_on"]]
        if target.get("kind") not in ("sections", "content", "gallery", "image"):
            target["kind"] = "sections" if target.get("sections") else "content"
        return [f"all on slide {ins['images_only_on']} as you asked"]
    for i, im in enumerate(imgs):
        k = ins.get("image_slides", {}).get(i)
        if k and 1 <= k <= n:
            slides[k - 1].setdefault("images", []).append(im["path"])
            if ins.get("image_section", {}).get(k):
                slides[k - 1]["image_section"] = ins["image_section"][k]
            continue
        d = "" if im.get("auto") else (im["desc"] or "").lower()
        name = Path(im["path"]).stem.lower()
        if re.search(r"\blogo\b", d) or re.search(r"(^|[_\- ])logo([_\- ]|$)", name) or \
                (im.get("auto") and re.match(r"^\W*logo\b", (im["desc"] or "").lower())):
            deck["logo"] = im["path"]
            notes.append("logo → every slide")
            continue
        m = re.search(r"slide\s*(?:no\.?|number|#)?\s*(\d{1,2})", d) or re.search(r"\b(\d{1,2})(?:st|nd|rd|th)\s+slide", d)
        if m and 1 <= int(m.group(1)) <= n:
            slides[int(m.group(1)) - 1].setdefault("images", []).append(im["path"])
            continue
        if re.search(r"\b(cover|title slide|first slide|hero|banner|background|opening)\b", d):
            slides[0].setdefault("images", []).append(im["path"])
            continue
        if re.search(r"\b(last|closing|final|thank)\b.*\bslide\b", d):
            slides[-1].setdefault("images", []).append(im["path"])
            continue
        free.append((i, im))
    # strict content hints ("Image: team photo")
    still = []
    for i, im in free:
        words = set(re.findall(r"[a-z]{3,}", (im["desc"] + " " + Path(im["path"]).stem.replace("_", " ")).lower()))
        best, best_k = 0, None
        for k, s in enumerate(slides):
            hint = (s.get("image_hint") or "").lower()
            if not hint:
                continue
            if Path(im["path"]).name.lower() in hint or re.search(rf"\b(image|img|photo|picture)\s*{i + 1}\b", hint):
                best, best_k = 99, k
                break
            sc = len(words & set(re.findall(r"[a-z]{3,}", hint)))
            if sc > best:
                best, best_k = sc, k
        if best_k is not None and best > 0:
            slides[best_k].setdefault("images", []).append(im["path"])
        else:
            still.append((i, im))
    # LLM outline assignment
    rest = []
    for i, im in still:
        k = next((k for k, s in enumerate(slides) if s.get("_image_idx") == i), None)
        if k is not None:
            slides[k].setdefault("images", []).append(im["path"])
        else:
            rest.append(im)
    # keyword overlap, then round-robin over text slides without images
    def eligible(s):
        return s.get("kind") in ("content", "cards", "stats", "quote", "process", "section") and not s.get("images") \
            and (s.get("kind") != "stats" or len(s.get("stats") or []) <= 3)
    for im in rest:
        words = set(re.findall(r"[a-z]{3,}", (im["desc"] + " " + Path(im["path"]).stem.replace("_", " ")).lower()))
        cands = [k for k, s in enumerate(slides) if eligible(s)]
        if not cands:
            if not count_locked and len(slides) > 1:
                gal = next((s for s in slides if s.get("kind") == "gallery"), None)
                if gal is None:
                    gal = {"kind": "gallery", "title": "Gallery", "images": []}
                    slides.insert(len(slides) - 1, gal)
                gal["images"].append(im["path"])
            else:
                target = max(range(1, len(slides) - 1) or [0], key=lambda k: -len(slides[k].get("images") or []))
                slides[target].setdefault("images", []).append(im["path"])
            continue

        def score(k):
            s = slides[k]
            txt = " ".join([s.get("title", ""), s.get("body", "")] +
                           [b.get("head", "") + " " + b.get("text", "") for b in s.get("bullets") or []]).lower()
            return len(words & set(re.findall(r"[a-z]{3,}", txt))) * 10 - abs(k - n / 2) * 0.01
        k = max(cands, key=score)
        slides[k].setdefault("images", []).append(im["path"])
        if slides[k].get("kind") == "cards":
            slides[k]["kind"] = "content"
    for s in slides:
        s.pop("_image_idx", None)
    _rebalance(slides, count_locked)
    return notes


# how many images each layout can show well
_CAPACITY = {"title": 1, "closing": 1, "quote": 1, "image": 1, "stats": 1, "section": 1, "cards": 1, "process": 1,
             "content": 3, "sections": 4, "gallery": 8, "table": 0, "chart": 0, "timeline": 0, "comparison": 0, "agenda": 0}


def _rebalance(slides: list[dict], count_locked: bool):
    """Move images off slides whose layout can't show them (or has too many) onto slides that can."""
    spill = []
    for s in slides:
        cap = _CAPACITY.get(s.get("kind"), 1)
        if s.get("kind") == "stats" and len(s.get("stats") or []) > 3:
            cap = 0
        imgs = s.get("images") or []
        if len(imgs) > cap:
            s["images"], extra = imgs[:cap], imgs[cap:]
            spill += extra
    for p in spill:
        free = [s for s in (slides[1:-1] or slides) if not s.get("images") and _CAPACITY.get(s.get("kind"), 1) >= 1
                and not (s.get("kind") == "stats" and len(s.get("stats") or []) > 3)]
        pref = [s for s in free if s.get("kind") in ("content", "cards", "process")] or free
        if pref:
            pref[len(pref) // 2 if len(pref) > 2 else 0]["images"] = [p]
            continue
        gal = next((s for s in slides if s.get("kind") == "gallery"), None)
        if gal is None and not count_locked and len(slides) > 1:
            gal = {"kind": "gallery", "title": "Gallery", "images": []}
            slides.insert(len(slides) - 1, gal)
        if gal is not None:
            gal["images"].append(p)
        else:
            multi = [s for s in slides if s.get("kind") == "content" and len(s.get("images") or []) < 3]
            if multi:
                multi[0].setdefault("images", []).append(p)


def _theme_from_text(clause: str, deck: dict) -> Optional[dict]:
    low = clause.lower()
    try:
        from app.services.ppt_tool import PERSONALITIES
    except Exception:
        PERSONALITIES = {}
    for k in list(THEMES) + list(PERSONALITIES):
        if k in low or k.replace("_", " ") in low or (k in THEMES and THEMES[k]["name"].lower() in low):
            return resolve_theme(k, legacy_palettes=PERSONALITIES)
    cur_dark = bool(deck.get("theme", {}).get("dark"))
    want_dark = True if re.search(r"\b(dark|black|night)\b", low) else False if re.search(r"\b(light|white|bright)\b", low) else cur_dark
    colours = {"blue": ("midnight", "ocean_light"), "navy": ("midnight", "slate_corporate"),
               "green": ("emerald_dark", "forest"), "teal": ("emerald_dark", "medical"),
               "purple": ("cosmic", "lavender"), "violet": ("cosmic", "lavender"), "pink": ("cosmic", "lavender"),
               "orange": ("ember", "editorial"), "red": ("ember", "editorial"), "warm": ("ember", "editorial"),
               "brown": ("ember", "editorial"), "neon": ("neon_pitch", "mono_bold"), "lime": ("neon_pitch", "mono_bold"),
               "mono": ("neon_pitch", "mono_bold"), "minimal": ("midnight", "minimal_light"),
               "corporate": ("midnight", "slate_corporate"), "professional": ("midnight", "slate_corporate")}
    for word, (dk, lt) in colours.items():
        if re.search(rf"\b{word}\b", low):
            return resolve_theme(dk if want_dark else lt)
    if re.search(r"\b(dark|black|night|light|white|bright)\b", low):
        return resolve_theme(None, prompt=("dark " if want_dark else "light ") + deck.get("title", ""),
                             purpose=deck.get("purpose", "general"))
    if re.search(r"\b(different|another|new|change)\b.*\b(theme|colou?rs?|look|style)\b", low):
        pool = [k for k in THEMES if (k in ("midnight", "neon_pitch", "cosmic", "ember", "emerald_dark")) == cur_dark
                and THEMES[k]["name"] != deck.get("theme", {}).get("name")]
        if pool:
            return resolve_theme(pool[int(time.time()) % len(pool)])
    return None


def _render(deck: dict, out: str, template: Optional[str]):
    if template and Path(template).exists():
        from app.services.ppt_template import TemplateFiller
        yield from TemplateFiller(template, deck, out).build()
    else:
        yield from DeckRenderer(deck, out).render()


def _render_safely(deck, out, template):
    """Render; if the file is open in PowerPoint, save as a new version instead."""
    try:
        for m in _render(deck, out, template):
            yield m
        return out
    except PermissionError:
        p = Path(out)
        base = re.sub(r"_v\d+$", "", p.stem)
        k = 2
        while (p.parent / f"{base}_v{k}.pptx").exists():
            k += 1
        alt = str(p.parent / f"{base}_v{k}.pptx")
        yield f"⚠️ `{p.name}` is open in PowerPoint — saving as `{Path(alt).name}` instead."
        for m in _render(deck, alt, template):
            yield m
        return alt


# ══════════════════════════════════════════════════════════════════════════════
#  CREATE
# ══════════════════════════════════════════════════════════════════════════════
def create(prompt: str, style: str = None, output_path: str = None, theme_image_path: str = None,
           research_data: dict = None, purpose: str = None, image_paths: list = None,
           image_descriptions: list = None, template_path: str = None):
    req = pc.split_request(prompt)
    imgs, template, theme_img = _collect_attachments(req, image_paths, image_descriptions, template_path, theme_image_path)
    # 1) understand the request: repair pasted text, separate instructions from content
    req["body"], instr = pc.split_instructions(pc.repair_text(req["body"]))
    req["attached_text"], instr2 = pc.split_instructions(pc.repair_text(req["attached_text"]))
    purpose, density = pc.detect_profile(req["command"] + " " + req["full"][:600],
                                         purpose if purpose == "hackathon" else None)
    blocks = pc.raw_slide_blocks(req["body"]) or pc.raw_slide_blocks(req["attached_text"])
    titles = [h for _, h, _ in blocks]
    ins = pc.parse_instructions([req["command"]] + instr + instr2, len(imgs), titles)
    if imgs and ins["image_sentences"] and not ins["images_only_on"] and not ins["image_slides"]:
        # phrasing the patterns couldn't resolve → let the model read the instruction (titles give it context)
        for rule in pc.interpret_image_instructions(ins["image_sentences"], titles, len(imgs),
                                                    [im["desc"] for im in imgs]):
            if rule["images"] == "all":
                ins["images_only_on"] = rule["slide"]
            else:
                for i in rule["images"]:
                    ins["image_slides"][i] = rule["slide"]
            if rule["section"]:
                ins["image_section"][rule["slide"]] = rule["section"]
    architect = bool(blocks) and pc.needs_architect(blocks)
    strict = [] if architect else (pc.parse_user_slides(req["body"]) or pc.parse_user_slides(req["attached_text"]))
    count = ins["count"] or pc.slide_count(req["command"] if (strict or blocks) else req["command"] + " " + req["body"][:300])
    count_locked = bool(count) or bool(strict) or bool(blocks)
    yield (f"🎯 Deck profile: {purpose} · {'minimal' if density == 'light' else density} text"
           + (f" · {count} slides" if count else "") + (" · your template" if template else "")
           + (f" · design reference: {Path(theme_img).name}" if theme_img else ""))
    if instr or instr2:
        yield "📝 Your instructions: " + " | ".join((instr + instr2)[:4])
    if ins["images_only_on"]:
        sec = ins["image_section"].get(ins["images_only_on"])
        yield (f"🖼️ All {len(imgs)} image(s) → slide {ins['images_only_on']}" + (f", “{sec}” section" if sec else "")
               + " (as you asked).")
    elif ins["image_slides"]:
        yield "🖼️ Image placement: " + ", ".join(f"image {i + 1} → slide {k}" for i, k in sorted(ins["image_slides"].items()))

    # ── captions for images without a description (helps placement) ──────
    need = [] if ins.get("images_only_on") else [im for im in imgs if not im["desc"]][:6]
    if need:
        yield f"👁️ Looking at {len(need)} image(s) to place them well…"
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=4) as ex:
            for im, cap in zip(need, ex.map(lambda x: _caption(x["path"]), need)):
                im["desc"] = cap or Path(im["path"]).stem.replace("_", " ")
                im["auto"] = True          # machine caption: used for matching only, never as an instruction

    # ── fixed-format template (e.g. SIH idea PPT): keep every section, answer its prompts ──
    fmt = None
    if template:
        try:
            from app.services.ppt_template import analyze_format
            fmt = analyze_format(template)
        except Exception as e:
            print(f"[ppt_studio] format analysis failed: {e}")
    if fmt:
        yield from _create_format(req, fmt, strict, purpose, template, output_path)
        return

    # ── content ──────────────────────────────────────────────────────────
    source = ""
    if not strict:
        extra = "\n".join(x for x in (req["body"], req["attached_text"]) if x)
        if len(extra) > 150:
            source = extra
    if research_data:
        facts = "\n- ".join(research_data.get("verified_facts", []))
        stats = "\n- ".join(f"{s['label']}: {s['value']}" for s in research_data.get("statistics", []))
        source = (source + f"\nVERIFIED FACTS:\n- {facts}\nSTATISTICS:\n- {stats}\nSOURCES: "
                  + ", ".join(research_data.get("sources", []))).strip()
        yield f"📚 Using {len(research_data.get('verified_facts', []))} researched facts."
    image_descs = [im["desc"] or Path(im["path"]).stem for im in imgs]
    if architect:
        per_slide = _images_per_slide(ins, imgs, len(blocks))
        yield (f"📌 Using YOUR content for {len(blocks)} slides — reading it and designing each slide around it "
               f"(your wording is kept; nothing is invented).")
        all_content = "\n".join(f"{h}\n{b}" for _, h, b in blocks)
        slides = yield from _with_progress(pc.architect_slides, blocks, purpose, per_slide, all_content,
                                           image_sections=ins["image_section"])
        title = next((s["title"] for s in slides if s.get("kind") == "title"), "") or slides[0].get("title", "")
        subs = [s.get("subtitle") for s in slides if s.get("subtitle")]
        for s_ in slides:                           # an event name repeated on every slide is noise
            if s_.get("kind") != "title" and s_.get("subtitle") and subs.count(s_["subtitle"]) > 1:
                s_["subtitle"] = ""
        deck = {"title": title, "slides": slides, "source_text": all_content, "facts": []}
        density = "dense" if purpose == "hackathon" or sum(len(b.split()) for _, _, b in blocks) / len(blocks) > 90 \
            else "balanced"
    elif strict and all(pc.slide_has_content(s) for s in strict):
        yield f"📌 Using YOUR content for all {len(strict)} slides — verbatim, only the design is automatic."
        slides = []
        for i, s in enumerate(strict):
            k = pc.infer_kind(s, i, len(strict))
            s2 = pc.apply_structure(s, k)
            s2["kind"] = k
            slides.append(s2)
        title = strict[0].get("title") or _topic_from_command(req["command"])
        deck = {"title": title, "slides": slides}
    else:
        if strict:
            yield (f"📌 Using your {len(strict)} slide titles/content as-is; writing only the "
                   f"{sum(1 for s in strict if not pc.slide_has_content(s))} empty slide(s).")
        else:
            yield "🧠 Planning the story and writing the slides…"
        request = req["command"] if (strict or source) else (req["full"][:1500] or req["command"])
        # ground the AI-written slides in real sources (skipped when the user gave the material themselves,
        # or asked for no research)
        facts = []
        if research_data:
            facts = [{"id": f"F{i + 1}", "fact": f, "source": "web research", "url": ""}
                     for i, f in enumerate(research_data.get("verified_facts", []))]
            facts += [{"id": f"F{len(facts) + i + 1}", "fact": f"{s['label']}: {s['value']}", "source": "web research",
                       "url": ""} for i, s in enumerate(research_data.get("statistics", []))]
        elif not source and not re.search(r"\b(no|without|skip|don'?t)\s+(web\s+)?(research|search|internet)\b|\boffline\b",
                                          req["full"], re.I):
            topic = _topic_from_command(req["command"]) or req["command"]
            facts = yield from _with_progress(pc.research_facts, topic, purpose, count or 10)
        deck = yield from _with_progress(pc.generate_deck, request, purpose, density, count, source, strict or None,
                                         image_descs, facts=facts, grounded=True)
        deck["source_text"] = source or ""
    if strict and all(pc.slide_has_content(s) for s in strict):
        # the user's own words decide how dense the design is, not the purpose keyword
        wc = [len(json.dumps({k: s.get(k) for k in ("bullets", "body", "stats", "steps", "columns", "table")},
                             ensure_ascii=False).split()) for s in deck["slides"][1:] or deck["slides"]]
        avg = sum(wc) / max(len(wc), 1)
        density = "light" if avg < 30 else "balanced" if avg < 70 else "dense"
    deck["purpose"], deck["density"] = purpose, density
    deck["slides"] = pc.finalize_slides(deck["slides"])
    if deck["slides"] and deck["slides"][0]["kind"] == "title" and not deck["slides"][0].get("subtitle") \
            and deck.get("subtitle") and not strict:
        deck["slides"][0]["subtitle"] = deck["subtitle"]

    # ── images ───────────────────────────────────────────────────────────
    if imgs:
        notes = _assign_images(deck, imgs, count_locked, ins)
        placed = sum(len(s.get("images") or []) for s in deck["slides"])
        yield f"🖼️ Placed {placed} image(s) on the slides where they fit best" + (f" ({', '.join(notes)})" if notes else "") + "."
        deck["slides"] = pc.finalize_slides(deck["slides"])

    # ── theme ────────────────────────────────────────────────────────────
    try:
        from app.services.ppt_tool import PERSONALITIES, extract_theme_from_image
    except Exception:
        PERSONALITIES, extract_theme_from_image = {}, None
    theme = None
    if theme_img and extract_theme_from_image:
        yield "🎨 Matching colours to your reference image…"
        try:
            theme = _reference_theme(theme_from_palette(extract_theme_from_image(theme_img), "From your image"))
        except Exception as e:
            yield f"⚠️ Couldn't read the reference image colours ({e}); picking a theme instead."
    if theme is None:
        theme = resolve_theme(style, req["command"] + " " + ins["text"] + " " + deck.get("title", ""), purpose,
                              PERSONALITIES)
    deck["theme"] = theme
    if template:
        yield f"🧩 Filling your template `{Path(template).name}` — its design stays exactly as it is."
    else:
        yield f"🎨 Theme: {theme.get('name')} · layouts chosen per slide from the content and image shapes."

    out = _out_path(deck.get("title", "Presentation"), output_path)
    final = yield from _render_safely(deck, out, template)
    st = _load_state()
    _push(st, {"deck": deck, "path": final, "template": template, "time": time.time()})
    _save_state(st)
    kinds = sorted({s["kind"] for s in deck["slides"]})
    yield (f"✅ Saved to: `{final}`\n"
           f"{len(deck['slides'])} slides · layouts used: {', '.join(kinds)}.\n"
           "💬 Want changes? Just say e.g. “on slide 3 change the title to …”, “make slide 5 a timeline”, "
           "“add a slide after 4 about pricing”, “use a dark theme”, or “undo”.")


# ══════════════════════════════════════════════════════════════════════════════
#  FIXED-FORMAT TEMPLATES
# ══════════════════════════════════════════════════════════════════════════════
def _user_value(label: str, text: str) -> str:
    m = re.search(rf"{re.escape(label)}\s*(?:is|=|:|-|–|—)\s*([^\n;.\[]+?)(?=\s*(?:[\n;.\[]|,\s*[A-Z][\w ]{{1,25}}\s*[:\-–]|$))", text, re.I)
    return m.group(1).strip(" .") if m else ""


def _create_format(req: dict, fmt: dict, strict: list, purpose: str, template: str, output_path: Optional[str]):
    from app.services.ppt_template import _label
    sections = [s for s in fmt["sections"] if not s["skip"]]
    skipped = [s["title"] for s in fmt["sections"] if s["skip"]]
    yield (f"📐 Your template is a fixed format with {len(sections)} sections — keeping every heading and position, "
           f"filling each section" + (f" (dropping the '{skipped[0]}' slide)" if skipped else "") + ".")
    full = req["full"] + "\n" + req["attached_text"]
    fields = {f: _user_value(f, full) for s in sections for f in s["fields"]}
    slots = {sl: _user_value(sl.replace("Your ", ""), full) or _user_value(sl, full) for s in sections for sl in s["slots"]}
    idea_title = ""
    per_section: dict[int, dict] = {}
    if strict:
        yield f"📌 Using your content verbatim for {min(len(strict), len(sections))} section(s)."
        for k, (sec, us) in enumerate(zip(sections, strict)):
            items = [((b["head"] + ": ") if b.get("head") else "") + b.get("text", "") for b in us.get("bullets") or []]
            if us.get("body"):
                items = us["body"].split("\n") + items
            per_section[sec["idx"]] = {"title": us.get("title", ""), "answers": [{"prompt": "", "points": items}]}
        idea_title = strict[0].get("title", "")
    missing = [s for s in sections if s["idx"] not in per_section and s["prompts"]]
    if missing:
        yield f"🧠 Writing content for {len(missing)} section(s) following the format's own prompts…"
        spec = "\n".join(f"[{s['idx'] + 1}] heading: \"{s['title']}\""
                         + (" (placeholder heading → give a real title)" if s["title_is_placeholder"] else "")
                         + (f" | fields: {s['fields']}" if s["fields"] else "")
                         + " | prompts: " + json.dumps(s["prompts"], ensure_ascii=False) for s in missing)
        user = "\n\n".join([
            f"REQUEST: {req['command']}\n{req['body'][:3000]}",
            ("SOURCE MATERIAL:\n" + req["attached_text"][:6000]) if req["attached_text"] else "",
            f"KNOWN VALUES (never invent IDs, names, team names, emails): fields={json.dumps(fields)} slots={json.dumps(slots)}",
            "REFERENCES: cite only well-known real sources by name and year (e.g. 'FAO, The State of Food and "
            "Agriculture 2020'); NEVER invent URLs, DOIs or paper titles — if unsure, omit the link.",
            "FORMAT SECTIONS TO FILL (answer EVERY prompt, keep prompts exactly as given):\n" + spec,
            pc._DENSITY_RULES["dense" if purpose == "hackathon" else "balanced"],
            'Return JSON: {"idea_title": "max 7 words", "fields": {"<field label>": "value or empty if unknown"}, '
            '"sections": [{"n": <section number>, "title": "only when the heading is a placeholder", '
            '"answers": [{"prompt": "<exact prompt text>", "points": ["2-4 specific points, max 22 words each"]}]}]}',
        ])
        data = pc._llm_json("You fill fixed presentation formats (hackathon/college submissions) with sharp, "
                            "specific content. You never change the format. Output valid JSON only.", user, 6000, 0.5)
        idea_title = idea_title or pc._s(data.get("idea_title"))
        for f, v in (data.get("fields") or {}).items():
            if f in fields and not fields[f] and v and not re.search(r"unknown|n/?a|tbd|<", str(v), re.I):
                fields[f] = pc._s(v)
        for s in data.get("sections") or []:
            if isinstance(s, dict) and isinstance(s.get("n"), int):
                per_section[s["n"] - 1] = {"title": pc._s(s.get("title")), "answers": s.get("answers") or []}
    slides = []
    for sec in sections:
        got = per_section.get(sec["idx"], {})
        answers = []
        for a in got.get("answers") or []:
            if not isinstance(a, dict):
                continue
            prompt = str(a.get("prompt") or "").strip()
            match = next((p for p in sec["prompts"] if p.strip() == prompt), None) or \
                next((p for p in sec["prompts"] if prompt and (prompt[:30].lower() in p.lower() or p[:30].lower() in prompt.lower())), prompt)
            answers.append({"prompt": match, "label": _label(match) if match else "",
                            "points": [pc._s(p if not isinstance(p, dict) else (p.get("text") or "")) for p in a.get("points") or []]})
        heading = sec["title"]
        new_title = got.get("title") or (idea_title if sec["title_is_placeholder"] else "")
        slides.append({"kind": "content", "tpl": sec["idx"], "title": new_title or heading,
                       "replace_title": bool(new_title and sec["title_is_placeholder"]),
                       "sections": answers, "form_fields": {f: fields.get(f, "") for f in sec["fields"]},
                       "idea_title": idea_title,
                       "slots": {sl: slots.get(sl, "") for sl in sec["slots"]}})
    deck = {"title": idea_title or req["command"][:60], "purpose": purpose, "density": "dense", "format_mode": True,
            "theme": resolve_theme("minimal_light"), "slides": slides}
    empty_f = [f for f, v in fields.items() if not v]
    out = _out_path(deck["title"], output_path)
    final = yield from _render_safely(deck, out, template)
    st = _load_state()
    _push(st, {"deck": deck, "path": final, "template": template, "time": time.time()})
    _save_state(st)
    yield (f"✅ Saved to: `{final}`\n{len(slides)} sections filled in your exact format."
           + (f"\n✍️ Still blank (tell me and I'll fill them): {', '.join(empty_f)}" if empty_f else "")
           + "\n💬 Follow-ups work as usual, e.g. “on slide 3 add Redis to the tech stack”.")


# ══════════════════════════════════════════════════════════════════════════════
#  EDIT
# ══════════════════════════════════════════════════════════════════════════════
_UNDO = re.compile(r"^\s*(undo|revert|go back|restore)\b.*$|\bundo (the )?(last )?(change|edit)\b|"
                   r"\b(previous|earlier|old) version\b", re.I)


def edit(instruction: str, image_paths: list = None):
    st = _load_state()
    cur = st.get("current")
    if not cur or not cur.get("deck"):
        yield "I don't have a presentation to edit yet — ask me to make one first."
        return
    req = pc.split_request(instruction)
    text = req["full"]
    if _UNDO.search(text) and len(text.split()) <= 10:
        if not st.get("history"):
            yield "Nothing to undo — this is the first version."
            return
        prev = st["history"].pop()
        final = yield from _render_safely(prev["deck"], cur["path"], prev.get("template"))
        prev["path"] = final
        st["current"] = prev
        _save_state(st)
        yield f"↩️ Reverted to the previous version.\n✅ Saved to: `{final}`"
        return
    imgs, _tpl, _ = _collect_attachments(req, image_paths, None, None, None)
    new_images = [im["path"] for im in imgs]
    if req["attached_text"]:
        text += "\n\nUse this content (verbatim):\n" + req["attached_text"][:6000]
    if req["body"] and req["body"] not in text:
        text += "\n" + req["body"]
    yield "✏️ Applying your change…"
    deck, notes = yield from _with_progress(pc.apply_edit, cur["deck"], text, new_images, _theme_from_text)
    if not notes:
        yield "🤔 I couldn't tell what to change. Try e.g. “on slide 2 replace 'X' with 'Y'”."
        return
    for n in notes:
        yield f"  • {n}"
    final = yield from _render_safely(deck, cur["path"], cur.get("template"))
    _push(st, {"deck": deck, "path": final, "template": cur.get("template"), "time": time.time()})
    _save_state(st)
    yield f"✅ Updated: `{final}` ({len(deck['slides'])} slides). Say “undo” to revert."
