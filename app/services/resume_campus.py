"""
resume_campus.py — campus / placement-cell resume format (renderer helper of resume_builder, not a tool)
=========================================================================================================
The single-page academic format colleges hand out: institute logo + name + contact lines, grey-band section
headings with a rule, an education TABLE (Year · Degree · Institute · CGPA/%), "Project | tech" headers with
bullets, skills in bold categories, achievements and a one-line courses list.

• render(c, d, scale) → full HTML. Same editor anchors as the other renderers (section.sec.sec-<key>, h2 title
  via _f("section_titles.<key>"), data-f fields, data-item rows), so the visual editor and the fit loop work.
• detect(image_path) → design overrides when a reference image is this format (an education table header row:
  "Year … Degree/Institute … CGPA/%/Grade"), with its section order/titles and the logo cropped from the image.
The logo lives in design["logo"] (a file path); the editor's 🏛 Logo button replaces it, and in the editor an
empty logo slot shows a dashed "Upload logo" placeholder (never printed).
"""

from __future__ import annotations

import os
import re

PRESET = {
    "layout": "single_column", "header": "left_plain", "photo": "none", "font": "serif", "name_case": "upper",
    "heading_style": "underline", "skills_style": "chips", "competency_style": "list", "timeline": False,
    "colors": {"primary": "#111111", "accent": "#111111", "heading": "#111111", "text": "#111111",
               "sidebar_bg": "#ffffff", "page_bg": "#ffffff", "header_text": "#111111",
               "skill_colors": ["#444444", "#666666", "#888888"]},
    "sidebar_sections": [],
    "main_sections": ["education", "profile", "experience", "projects", "skills", "achievements", "certifications",
                      "highlights", "competencies", "languages", "interests", "references"],
    "campus": {"band": "#e9ecf2", "rule": "#1f2933"},
}
BLURB = "campus / placement-cell format: college logo, education table, grey-band headings, one page"

TITLES = {"education": "Education", "profile": "Summary", "experience": "Experience", "projects": "Projects",
          "skills": "Skills", "achievements": "Achievements", "certifications": "Courses and Certifications",
          "highlights": "Highlights", "competencies": "Core Competencies", "languages": "Languages",
          "interests": "Interests", "references": "References", "contact": "Contact"}

_CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box}
html{background:#fff}
body{margin:0;width:210mm;min-height:297mm;padding:7mm 9mm 8mm;font-family:'Tinos','Times New Roman',Times,serif;
 color:%(text)s;font-size:calc(10.4pt * var(--s,1));line-height:1.22;background:#fff;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.c-head{display:flex;align-items:center;gap:4mm;margin-bottom:2.2mm}
.c-logo{width:calc(23mm * var(--s,1));height:calc(23mm * var(--s,1));flex:none;display:flex;align-items:center;justify-content:center}
.c-logo img{max-width:100%%;max-height:100%%;object-fit:contain}
.c-logo.ph{border:1.5px dashed #94a3b8;border-radius:50%%;color:#64748b;font:9pt Arial;text-align:center}
.c-name{font-size:calc(24pt * var(--s,1));font-weight:700;line-height:1.05;letter-spacing:.2pt}
.c-name.up{text-transform:uppercase}
.c-line{font-size:calc(10pt * var(--s,1));margin-top:1mm}
.c-line.b{font-weight:700}
.c-sep{margin:0 1.6mm}
.sec{margin-top:calc(2mm * var(--s,1))}
.sec h2{margin:0 0 1.2mm;padding:.4mm 2mm;font-size:calc(11.6pt * var(--s,1));font-weight:700;text-transform:uppercase;
 letter-spacing:.3pt;background:%(band)s;border-bottom:1px solid %(rule)s;line-height:1.2}
table.c-edu{width:100%%;border-collapse:collapse;font-size:calc(10pt * var(--s,1))}
.c-edu th,.c-edu td{border:1px solid #555;padding:.5mm 1.6mm;vertical-align:top}
.c-edu th{font-weight:700;text-align:center}
.c-edu td.c{text-align:center}.c-edu td.y{text-align:center;font-weight:700}
.c-p{text-align:justify;margin:0}
.c-it{margin-top:calc(1.4mm * var(--s,1))}
.c-it:first-of-type{margin-top:0}
.c-ih{font-weight:700;display:flex;justify-content:space-between;gap:3mm}
.c-ih .r{font-weight:400;white-space:nowrap}
.c-sub{font-style:italic}
ul.c-ul{margin:.3mm 0 0;padding-left:5.5mm}
ul.c-ul li{text-align:justify;margin:.15mm 0}
.c-sk{margin:.2mm 0}
"""


def _uri(path: str) -> str:
    from app.services.resume_builder import _data_uri
    return _data_uri(path) if path and os.path.isfile(path) else ""


def render(c: dict, d: dict, scale: float = 1.0) -> str:
    from app.services import resume_builder as rb
    f, it, e = rb._f, rb._it, rb._e
    edit = rb._EDIT.get() is True
    camp = d.get("campus") if isinstance(d.get("campus"), dict) else {}
    colors = d.get("colors") or {}
    css = _CSS % {"text": colors.get("text") or "#111111", "band": camp.get("band") or "#e9ecf2",
                  "rule": camp.get("rule") or "#1f2933"}
    titles = {**TITLES, **(camp.get("titles") or {}), **(d.get("section_titles") or {}), **(c.get("section_titles") or {})}
    hidden = set(d.get("hidden_sections") or [])

    def sec(key, inner):
        return (f'<section class="sec sec-{key}"><h2>{f("section_titles." + key, titles.get(key) or key.title(), "section title")}'
                f'</h2>{inner}</section>') if inner else ""

    def bullets(path, items):
        return ('<ul class="c-ul">' + "".join(f'<li{it(f"{path}.{j}")}>{f(f"{path}.{j}", b)}</li>' for j, b in enumerate(items))
                + "</ul>") if items else ""

    # header: logo · name · contact · links
    logo = _uri(d.get("logo") or "")
    if logo:
        logo_html = f'<div class="c-logo"><img src="{logo}" alt="logo"></div>'
    elif edit:
        logo_html = '<div class="c-logo ph edit-only" title="Toolbar → 🏛 Logo">Upload<br>logo</div>'
    else:
        logo_html = ""
    ct = c.get("contact") or {}
    sep = '<span class="c-sep">|</span>'
    line1 = sep.join(f(f"contact.{k}", ct[k], k) for k in ("email", "phone", "location") if ct.get(k))
    line2 = sep.join(f(f"contact.{k}", ct[k], k) for k in ("linkedin", "website") if ct.get(k))
    head = (f'<header class="c-head">{logo_html}<div><div class="c-name nm{' up' if camp.get('name_upper', True) else ''}">{f("name", c.get("name") or "Your Name", "name")}</div>'
            + (f'<div class="c-line">{line1}</div>' if line1 else "")
            + (f'<div class="c-line b">{line2}</div>' if line2 else "")
            + (f'<div class="c-line ttl">{f("title", c["title"], "headline")}</div>' if c.get("title") and camp.get("show_title") else "")
            + "</div></header>")

    blocks = {}
    edu = c.get("education") or []
    if edu:
        rows = "".join(
            f'<tr{it(f"education.{i}")}><td class="y">{f(f"education.{i}.period", x.get("period", ""), "year")}</td>'
            f'<td>{f(f"education.{i}.degree", x.get("degree", ""), "degree")}</td>'
            f'<td>{f(f"education.{i}.institution", x.get("institution", ""), "institute")}</td>'
            f'<td class="c">{f(f"education.{i}.details", x.get("details", ""), "CGPA / %")}</td></tr>'
            for i, x in enumerate(edu))
        hd = camp.get("edu_head") or ["Year", "Degree/Certificate", "Institute", "CGPA/%"]
        blocks["education"] = (f'<table class="c-edu"><colgroup><col style="width:13%"><col style="width:20%"><col>'
                               f'<col style="width:15%"></colgroup><tr>{"".join(f"<th>{e(h)}</th>" for h in hd[:4])}</tr>{rows}</table>')
    prof = c.get("profile") or []
    if prof:
        blocks["profile"] = "".join(f'<p class="c-p"{it(f"profile.{i}")}>{f(f"profile.{i}", p, "summary")}</p>' for i, p in enumerate(prof))
    exp = c.get("experience") or []
    if exp:
        blocks["experience"] = "".join(
            f'<div class="c-it"{it(f"experience.{i}")}><div class="c-ih"><span>{f(f"experience.{i}.role", x.get("role", ""), "role")}'
            + (f' | {f(f"experience.{i}.company", x["company"], "company")}' if x.get("company") else "")
            + f'</span><span class="r">{f(f"experience.{i}.period", x.get("period", ""), "period")}</span></div>'
            + bullets(f"experience.{i}.bullets", x.get("bullets") or []) + "</div>" for i, x in enumerate(exp))
    projs = c.get("projects") or []
    if projs:
        out = []
        for i, x in enumerate(projs):
            hdr = f(f"projects.{i}.name", x.get("name", ""), "project")
            if x.get("tech"):
                hdr += f' | {f(f"projects.{i}.tech", x["tech"], "tech stack")}'
            per = f'<span class="r">{f(f"projects.{i}.period", x["period"], "period")}</span>' if x.get("period") else ""
            body = (f'<p class="c-p">{f(f"projects.{i}.description", x["description"], "description")}</p>'
                    if x.get("description") and not x.get("bullets") else "")
            out.append(f'<div class="c-it"{it(f"projects.{i}")}><div class="c-ih"><span>{hdr}</span>{per}</div>{body}'
                       f'{bullets(f"projects.{i}.bullets", x.get("bullets") or [])}</div>')
        blocks["projects"] = "".join(out)
    groups = c.get("skill_groups") or []
    if groups:
        blocks["skills"] = "".join(
            f'<div class="c-sk"{it(f"skill_groups.{i}")}><b>{f(f"skill_groups.{i}.label", g.get("label", ""), "category")}:</b> '
            f'{f(f"skill_groups.{i}.items", g.get("items", ""), "skills")}</div>' for i, g in enumerate(groups))
    elif c.get("skills") or c.get("additional_skills"):
        names = [f(f"skills.{i}.name", s["name"], "skill") for i, s in enumerate(c.get("skills") or [])]
        names += [f(f"additional_skills.{i}", s, "skill") for i, s in enumerate(c.get("additional_skills") or [])]
        blocks["skills"] = f'<div class="c-sk"><b>Skills:</b> {", ".join(names)}</div>'
    for key in ("achievements", "highlights", "interests", "references"):
        if c.get(key):
            blocks[key] = bullets(key, c[key])
    certs = c.get("certifications") or []
    if certs:
        if sum(len(x) for x in certs) <= 150:      # short courses: one line, as the format does
            blocks["certifications"] = ('<ul class="c-ul"><li>' + sep.join(f'<span{it(f"certifications.{j}")}>'
                                        f'{f(f"certifications.{j}", x)}</span>' for j, x in enumerate(certs)) + "</li></ul>")
        else:
            blocks["certifications"] = bullets("certifications", certs)
    comps = c.get("competencies") or []
    if comps:
        blocks["competencies"] = bullets("competencies", [x["title"] + (f": {x['description']}" if x.get("description") else "")
                                                          for x in comps]) if not edit else (
            '<ul class="c-ul">' + "".join(f'<li{it(f"competencies.{j}")}>{f(f"competencies.{j}.title", x["title"])}'
                                          + (f': {f(f"competencies.{j}.description", x["description"])}' if x.get("description") else "")
                                          + "</li>" for j, x in enumerate(comps)) + "</ul>")
    langs = c.get("languages") or []
    if langs:
        blocks["languages"] = '<div class="c-sk">' + ", ".join(f(f"languages.{i}.name", x["name"]) for i, x in enumerate(langs)) + "</div>"
    for cs in c.get("custom_sections") or []:
        if cs.get("id") in hidden:
            continue
        items = cs.get("items") or []
        titles[cs["id"]] = cs.get("title") or "Section"
        blocks[cs["id"]] = bullets(f'custom_sections.{(c.get("custom_sections") or []).index(cs)}.items', items) or (
            '<p class="c-p edit-only">Click to add…</p>' if edit else "")

    order = list(dict.fromkeys((camp.get("order") or []) + list(d.get("main_sections") or []) + PRESET["main_sections"]
                               + [cs["id"] for cs in c.get("custom_sections") or []]))
    body = "".join(sec(k, blocks.get(k, "")) for k in order if k not in hidden)
    title = e(c.get("name") or "Resume")
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title} — Resume</title>'
            f'<link href="https://fonts.googleapis.com/css2?family=Tinos:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">'
            f'<style>{css}</style></head><body class="campus lay-single_column" style="--s:{scale}">{head}'
            f'<div class="cols"><main>{body}</main></div>{rb._free_html(d, edit)}</body></html>')


# ── detection from a reference image ─────────────────────────────────────────────────────────────────

_YEAR_H = re.compile(r"(?i)^\s*(year|session|batch|duration|period)\s*$")
_DEG_H = re.compile(r"(?i)degree|certificate|qualification|course|exam|class|programme|program|board")
_INST_H = re.compile(r"(?i)institut|college|school|university|board")
_SCORE_H = re.compile(r"(?i)cgpa|gpa|%|percent|grade|marks|score|result")


def detect(image_path: str, out_dir: str) -> dict | None:
    """Design overrides if the image is a campus-format resume (education table header row), else None."""
    try:
        import cv2
        import numpy as np
        from app.services.resume_replica.ingest import load_reference
        from app.services.resume_replica.measure import ocr_lines, title_key
        ref = load_reference(image_path)
        img = ref["img"]
        lines = ocr_lines(img)
        if not lines:
            return None
        H, W = img.shape[:2]
        # the table header: ≥3 header words on one row, incl. a year column and a score column
        rows: list[list[dict]] = []
        for l in sorted(lines, key=lambda l: (l["box"][1] + l["box"][3]) / 2):
            cy = (l["box"][1] + l["box"][3]) / 2
            for r in rows:
                if abs((r[0]["box"][1] + r[0]["box"][3]) / 2 - cy) < 0.5 * (r[0]["box"][3] - r[0]["box"][1]):
                    r.append(l)
                    break
            else:
                rows.append([l])
        head = None
        for r in rows:
            txt = [l["text"].strip() for l in sorted(r, key=lambda l: l["box"][0])]
            if len(txt) >= 2 and all(len(t) <= 24 for t in txt) and any(_SCORE_H.search(t) for t in txt)                     and any(_DEG_H.search(t) or _INST_H.search(t) for t in txt):
                # header cells by meaning (OCR may miss one): year · degree · institute · score
                slots = ["Year", "Degree/Certificate", "Institute", "CGPA/%"]
                for t in txt:
                    if _YEAR_H.match(t):
                        slots[0] = t
                    elif _SCORE_H.search(t):
                        slots[3] = t
                    elif _INST_H.search(t) and not _DEG_H.search(t):
                        slots[2] = t
                    elif _DEG_H.search(t):
                        slots[1] = t
                head = slots
                break
        if not head:
            return None
        # section order + titles as written (upper-case heading lines naming a section)
        order, titles = [], {}
        for l in sorted(lines, key=lambda l: l["box"][1]):
            t = l["text"].strip(" :|-")
            letters = re.sub(r"[^A-Za-z]", "", t)
            if len(letters) >= 4 and t.upper() == t and len(t) <= 40:
                k = title_key(t)
                if k and k not in order:
                    order.append(k)
                    titles[k] = t.title().replace(" And ", " and ").replace(" & ", " & ")
        # heading band colour: the light fill behind the first heading
        band = "#e9ecf2"
        hl = next((l for l in lines if title_key(l["text"].strip(" :|-")) in order[:1]), None)
        if hl:
            x0, y0, x1, y1 = hl["box"]
            strip = img[max(0, y0 - 2):y1 + 2, max(0, x1 + 6):min(W, x1 + int(0.25 * W))].reshape(-1, 3)
            if len(strip):
                c = np.median(strip, axis=0)
                if 200 < c.mean() < 252:
                    band = "#%02x%02x%02x" % (int(c[2]), int(c[1]), int(c[0]))
        # the logo: the picture left of the name (largest top line)
        logo = ""
        top = [l for l in lines if l["box"][1] < 0.2 * H]
        if top:
            name = max(top, key=lambda l: l["box"][3] - l["box"][1])
            nx0, ny0, nx1, ny1 = name["box"]
            if nx0 > 0.08 * W:
                heads = [l["box"][1] for l in lines if l["box"][1] > ny0 and title_key(l["text"].strip(" :|-"))
                         and l["text"].upper() == l["text"]]
                y_end = max(ny1, min(heads) - 3) if heads else int(0.2 * H)     # stop above the first section
                reg = img[0:y_end, 0:nx0 - 4]
                ink = (np.abs(reg.astype(int) - 255).sum(-1) > 60).astype(np.uint8)
                n, cc, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
                big = [i for i in range(1, n) if st[i, 4] > 0.002 * reg.shape[0] * reg.shape[1]]
                if big:
                    x0 = min(st[i, 0] for i in big); y0 = min(st[i, 1] for i in big)
                    x1 = max(st[i, 0] + st[i, 2] for i in big); y1 = max(st[i, 1] + st[i, 3] for i in big)
                    if x1 - x0 > 0.04 * W and y1 - y0 > 0.04 * W:
                        crop = img[max(0, y0 - 3):y1 + 3, max(0, x0 - 3):x1 + 3]
                        alpha = (np.abs(crop.astype(int) - 255).sum(-1) > 18).astype(np.uint8) * 255
                        os.makedirs(out_dir, exist_ok=True)
                        logo = os.path.join(out_dir, f"logo_{os.path.splitext(os.path.basename(image_path))[0][:40]}.png")
                        cv2.imencode(".png", np.dstack([crop, alpha]))[1].tofile(logo)
        name_upper = bool(top) and (lambda t: t.upper() == t and len(re.sub(r"[^A-Za-z]", "", t)) >= 3)(
            max(top, key=lambda l: l["box"][3] - l["box"][1])["text"])
        return {"order": order, "titles": titles, "band": band, "edu_head": head, "logo": logo, "name_upper": name_upper}
    except Exception as e:
        print(f"[resume] campus detect failed: {e}")
        return None
