"""
replica_eval.py — Run the exact-replica engine over reference resumes and write a side-by-side HTML report.

    python scripts/replica_eval.py data/uploads/Screenshot_2026-10-03_120914_*.png ...   # specific references
    python scripts/replica_eval.py --recent 8                                            # newest portrait screenshots
    python scripts/replica_eval.py --force ...                                           # re-analyse (ignore cache)

Content: the saved resume (app/memory/resume_state.json) or a built-in sample. Output:
data/uploads/resumes/replica_eval/index.html (reference | replica page 1 | measured fonts, layout, timings).
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SAMPLE = {
    "name": "Jordan Avery Lee", "title": "Senior Software Engineer",
    "contact": {"phone": "+1 555 010 2030", "email": "jordan.lee@example.com", "location": "Austin, TX",
                "linkedin": "linkedin.com/in/jordanlee", "website": ""},
    "profile": ["Backend engineer with 7 years building distributed systems and developer platforms. Led migrations to "
                "event-driven architectures and mentored teams of five."],
    "experience": [
        {"role": "Senior Software Engineer", "company": "Northwind Labs", "period": "2021 - Present", "location": "",
         "bullets": ["Designed an event pipeline handling 40k messages per second.",
                     "Cut cloud spend by 28% through autoscaling and caching.",
                     "Mentored five engineers; introduced design reviews."]},
        {"role": "Software Engineer", "company": "Contoso Systems", "period": "2017 - 2021", "location": "",
         "bullets": ["Built REST and gRPC services in Go and Python.", "Owned CI/CD for 30 services."]}],
    "education": [{"degree": "B.S. Computer Science", "institution": "State University", "period": "2013 - 2017",
                   "details": "GPA 3.8"}],
    "skills": [{"name": "Python", "level": 90}, {"name": "Go", "level": 80}, {"name": "Kubernetes", "level": 75},
               {"name": "PostgreSQL", "level": 70}],
    "additional_skills": ["Kafka", "Redis", "Terraform", "AWS"],
    "certifications": ["AWS Solutions Architect - Associate"], "languages": [{"name": "English", "level": 5}],
    "achievements": ["Speaker at PyCon 2023"], "interests": ["Climbing", "Chess"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("refs", nargs="*")
    ap.add_argument("--recent", type=int, default=0)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--sample", action="store_true", help="use the built-in sample content")
    a = ap.parse_args()
    refs = [p for r in a.refs for p in glob.glob(r)]
    if a.recent:
        from PIL import Image
        cands = sorted(glob.glob(os.path.join(ROOT, "data", "uploads", "Screenshot_*.png")), key=os.path.getmtime, reverse=True)
        for p in cands:
            with Image.open(p) as im:
                if im.height > im.width * 1.2:
                    refs.append(p)
            if len(refs) >= a.recent:
                break
    if not refs:
        ap.error("no reference images")
    from app.services import resume_builder as rb
    from app.services.resume_replica.integrate import replica_design
    from app.services.resume_replica.pipeline import analyse_reference
    content = SAMPLE
    if not a.sample:
        try:
            with open(os.path.join(ROOT, "app", "memory", "resume_state.json"), encoding="utf-8") as f:
                content = json.load(f).get("content") or SAMPLE
        except Exception:
            pass
    content = rb._normalise_content(content)
    out = os.path.join(ROOT, "data", "uploads", "resumes", "replica_eval")
    os.makedirs(out, exist_ok=True)
    rows = []
    for p in refs:
        t0 = time.time()
        try:
            spec = analyse_reference(p, force=a.force)
        except Exception as e:
            rows.append((p, None, f"analysis failed: {e}", 0))
            continue
        ta = time.time() - t0
        if not spec:
            rows.append((p, None, "not recognised as a resume", ta))
            continue
        stem = "eval_" + spec["sha1"][:10]
        d = replica_design(spec)
        try:
            files = rb._render_files(content, d, "", stem)
            png = files["pngs"][0] if files.get("pngs") else ""
            import shutil
            shutil.copy(png, os.path.join(out, os.path.basename(png)))
            info = (f"{files['pages']} page(s) · analysis {ta:.0f}s (cached={spec.get('analysis_s') and ta < 5}) · "
                    f"fonts: " + ", ".join(f"{k}={v['family']} {v['weight']} {v['size']:.2f}mm" for k, v in spec["styles"].items()))
            rows.append((p, os.path.basename(png), info, ta))
        except Exception as e:
            import traceback
            traceback.print_exc()
            rows.append((p, None, f"render failed: {e}", ta))
        print(f"{os.path.basename(p)}: {rows[-1][2][:120]}")
    import shutil
    body = []
    for p, png, info, _ in rows:
        ref_name = "ref_" + os.path.basename(p)
        shutil.copy(p, os.path.join(out, ref_name))
        body.append(f"<section><h3>{html.escape(os.path.basename(p))}</h3><div class=row><img src='{ref_name}'>"
                    f"{f'<img src={png!r}>' if png else '<div class=fail>no output</div>'}</div>"
                    f"<p>{html.escape(info)}</p></section>")
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8><title>Replica eval</title><style>body{font:14px Segoe UI;margin:20px;"
                "background:#f4f5f7}section{background:#fff;padding:12px;margin:0 0 18px;border-radius:8px}.row{display:flex;"
                "gap:12px}.row img{height:900px;border:1px solid #ccc}.fail{width:600px;height:200px;color:#b00}</style>"
                + "".join(body))
    print("report:", os.path.join(out, "index.html"))


if __name__ == "__main__":
    main()
