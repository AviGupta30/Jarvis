"""
ppt_router.py — FastAPI router for the PPT AI build endpoint
============================================================
Registered in main.py.

POST /ppt/build
  Body: { plan: { ...slide plan JSON from Puter.js Gemini... } }
  Streams live progress lines as text/event-stream.
  Builds the PPTX and saves it to the Desktop.

This endpoint is used by the frontend's Puter.js integration.
The /chat route continues to use Groq for voice + fallback.
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Any
import json

router = APIRouter(prefix="/ppt", tags=["ppt"])


class PPTBuildRequest(BaseModel):
    plan: dict                    # Full slide plan JSON from Puter.js
    output_path: Optional[str] = None  # Override save path (optional)


@router.post("/build")
async def build_ppt(request: PPTBuildRequest):
    """
    Build a PPTX from a pre-generated slide plan (JSON).
    Streams live per-slide progress back to the client.

    The frontend calls Puter.js (Gemini 3.1 Pro free) to generate the plan,
    then POSTs it here. This keeps content generation on the free Puter.js tier
    while python-pptx rendering stays fast and local.
    """
    plan = request.plan
    output_path = request.output_path

    def generate():
        try:
            from app.services.ppt_tool import PresentationBuilder, PERSONALITIES, _pick
            import re, time
            from pathlib import Path

            # Resolve / validate personality
            personality = plan.get("personality")
            if not personality or personality not in PERSONALITIES:
                # Auto-detect from title
                title = plan.get("presentation_title", "")
                personality = _pick(title)
                plan["personality"] = personality

            P = PERSONALITIES[personality]
            deck_title = plan.get("presentation_title", "Presentation")
            n_slides = len(plan.get("slides", []))

            yield f"🎨 Style: **{P['name']}**\n\n"
            yield f"📋 **\"{deck_title}\"** — {n_slides} slides\n\n"
            yield "─" * 44 + "\n\n"

            if not output_path:
                desktop = Path.home() / "Desktop"
                desktop.mkdir(exist_ok=True)
                safe = re.sub(r"[^\w\s\-]", "", deck_title)
                safe = re.sub(r"\s+", "_", safe)[:40]
                out = str(desktop / f"{safe}_{int(time.time())}.pptx")
            else:
                out = output_path

            builder = PresentationBuilder(plan, out)
            for status in builder.build_with_progress():
                yield status + "\n\n"

            yield "─" * 44 + "\n\n"
            yield f"✅ **Done!** \"{deck_title}\" — {n_slides} slides in {P['name']} style\n\n"
            yield f"📂 Saved to: `{out}`\n\n"

        except Exception as e:
            yield f"❌ Build failed: {e}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


class PPTCreateRequest(BaseModel):
    prompt: str
    style: Optional[str] = None
    purpose: Optional[str] = None
    output_path: Optional[str] = None
    theme_image_path: Optional[str] = None  # Path to a reference PPT screenshot

@router.post("/create")
async def create_ppt_backend(request: PPTCreateRequest):
    """
    End-to-end PPT generation using Groq on the backend.
    Optionally accepts a theme_image_path to extract and apply colors from a reference screenshot.
    """
    from app.services.ppt_tool import ppt_create
    
    def generate():
        try:
            for chunk in ppt_create(
                request.prompt,
                request.style,
                request.output_path,
                request.theme_image_path,
                None,  # research_data
                request.purpose
            ):
                yield chunk + "\n\n"
        except Exception as e:
            yield f"❌ Backend Fallback Error: {str(e)}\n\n"
            
    return StreamingResponse(generate(), media_type="text/event-stream")


class PPTExtractThemeRequest(BaseModel):
    image_path: str

@router.post("/extract-theme")
async def extract_theme(request: PPTExtractThemeRequest):
    """
    Extract color theme from a PPT screenshot image.
    Returns the custom_theme dict with hex color codes.
    """
    from app.services.ppt_tool import extract_theme_from_image
    try:
        theme = extract_theme_from_image(request.image_path)
        return {"status": "success", "theme": theme}
    except Exception as e:
        return {"status": "error", "error": str(e)}


class PPTStylesResponse(BaseModel):
    styles: dict
    count: int

@router.get("/styles")
def get_styles():
    """Return all available design personalities."""
    from app.services.ppt_tool import ppt_styles
    return ppt_styles()
