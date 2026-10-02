"""
resume_router.py — FastAPI router for the visual resume editor
================================================================
Registered in main.py.

GET  /resume/editor   The current resume (app/memory/resume_state.json) rendered with every text
                      value editable, plus a toolbar (template, colour, photo, add section, AI edit, export).
POST /resume/save     Body: {content, op?, add_section?, template?, color?, photo?, remove_photo?,
                      instruction?, export?}. Applies the edits, saves the state and, with export=true,
                      re-renders the PDF/PNGs. Sync handlers, so FastAPI runs them in its threadpool
                      (Playwright's sync API needs a thread without an event loop).
"""

from fastapi import APIRouter, Body
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/resume", tags=["resume"])


@router.get("/editor", response_class=HTMLResponse)
def resume_editor():
    from app.services.resume_builder import editor_page
    return HTMLResponse(editor_page(), headers={"Cache-Control": "no-store"})


@router.post("/save")
def resume_save(payload: dict = Body(...)):
    from app.services.resume_builder import editor_save
    return editor_save(payload or {})
