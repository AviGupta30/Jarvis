import asyncio
import os
from app.services.ppt_tool import _groq_call, _SYS_OUTLINE, _USR_OUTLINE, _parse, PresentationBuilder, extract_theme_from_image, PERSONALITIES, _SYS_CHUNK, _USR_CHUNK, _SYS_CHART, _USR_CHART

def main():
    # Simulating the pipeline just to generate a quick PPT for testing
    from app.services.ppt_tool import _groq_call, _SYS_OUTLINE, _USR_OUTLINE, _parse, PresentationBuilder
    import time
    from pathlib import Path
    
    enriched_prompt = "Create a presentation on Danmarks Tekniske Universitet (DTU). Focus on academics, student life, rankings, and global impact."
    
    # generate outline
    print("Generating outline...")
    raw_outline = _groq_call(_SYS_OUTLINE, _USR_OUTLINE.format(prompt=enriched_prompt))
    plan = _parse(raw_outline)
    plan["personality"] = "ocean_pro"
    
    slides_outline = plan.get("slides", [])
    total_slides = len(slides_outline)
    print(f"Outline created, testing all {total_slides} slides to ensure zero hallucinations or errors.")
    
    full_slides = []
    chunk_size = 2
    import json
    outline_str = json.dumps([{"slide_number": s.get("slide_number"), "title": s.get("title"), "layout": s.get("layout")} for s in slides_outline])
    
    for i in range(0, total_slides, chunk_size):
        chunk = slides_outline[i:i+chunk_size]
        start_idx = chunk[0].get('slide_number', i+1)
        end_idx = chunk[-1].get('slide_number', i+len(chunk))
        
        print(f"Generating chunk {start_idx}-{end_idx}...")
        raw_chunk = _groq_call(
            _SYS_CHUNK,
            _USR_CHUNK.format(prompt=enriched_prompt, outline=outline_str, start_idx=start_idx, end_idx=end_idx)
        )
        chunk_data = _parse(raw_chunk)
        chunk_slides = chunk_data.get("slides", [])
        full_slides.extend(chunk_slides)
        
    print("Generating charts...")
    chart_ok = 0
    chart_fail = 0
    used_chart_types = []
    
    for si, sd in enumerate(full_slides):
        vs = sd.get("visual_suggestion", "")
        lay = sd.get("layout", "")
        if lay == "aesthetic_title" or not vs:
            continue
            
        content_parts = []
        for b in sd.get("bullets", []):
            if isinstance(b, dict):
                content_parts.append(f"{b.get('bold','')} {b.get('text','')}".strip())
        content_summary = "; ".join(content_parts[:6]) or sd.get("title", "")
        
        try:
            used_str = ", ".join(used_chart_types) if used_chart_types else "None"
            
            # Note: We must format with used_charts when we update the prompt
            raw_chart = _groq_call(
                _SYS_CHART,
                _USR_CHART.format(
                    title=sd.get("title", ""),
                    layout=lay,
                    visual_suggestion=vs,
                    content_summary=content_summary[:500],
                    used_charts=used_str
                ),
                tokens=800
            )
            chart_data = _parse(raw_chart)
            if chart_data and chart_data.get("type"):
                sd["chart_data"] = chart_data
                used_chart_types.append(chart_data.get("type"))
                chart_ok += 1
                print(f"Slide {si+1} chart: {chart_data.get('type')}")
            # Sleep to avoid Groq rate limit
            time.sleep(4)
        except Exception as e:
            chart_fail += 1
            print(f"Slide {si+1} chart fail: {e}")
            
    plan["slides"] = full_slides
    out = "test_ppt.pptx"
    b = PresentationBuilder(plan, out)
    for s in b.build_with_progress():
        pass
    print(f"Done. Saved to {out}. Chart OK: {chart_ok}, Fail: {chart_fail}")

if __name__ == '__main__':
    main()
