from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router
from app.api.tools import router as tools_router
from app.api.ppt_router import router as ppt_router
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Jarvis AI Assistant")

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(chat_router)
app.include_router(memory_router)
app.include_router(tools_router)
app.include_router(ppt_router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Jarvis AI Assistant API!"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file to the data/uploads folder for Jarvis to process."""
    try:
        import time
        import pathlib
        
        # Save to Jarvis/data/uploads to avoid Desktop permission/lock issues
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(base_dir, "data", "uploads")
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Make filename unique to avoid 'file in use' errors
        safe_filename = file.filename.replace(" ", "_")
        name, ext = os.path.splitext(safe_filename)
        unique_filename = f"{name}_{int(time.time())}{ext}"
        
        file_path = os.path.join(uploads_dir, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"filename": unique_filename, "path": file_path, "status": "success"}
    except Exception as e:
        return {"filename": file.filename, "error": str(e), "status": "error"}


# ── Background Screen Watcher ─────────────────────────────────────────────────
# Starts a passive thread on startup that monitors the screen every ~8 seconds.
# Only triggers VLM API calls when a significant pixel change is detected.
# Zero API cost during idle screen time.

_watcher_alerts: list[str] = []   # in-memory alert queue for the frontend to poll


def _on_screen_alert(alert_text: str) -> None:
    """
    Callback fired by the background watcher when something notable is detected.
    Stores the alert for frontend polling and logs it.
    """
    logger.info(f"[watcher-alert] {alert_text}")
    _watcher_alerts.append(alert_text)
    # Keep the queue bounded to the last 20 alerts
    if len(_watcher_alerts) > 20:
        _watcher_alerts.pop(0)


@app.on_event("startup")
async def startup_event():
    """Start background screen watcher when the server boots."""
    try:
        from app.services.screen_vision import start_background_watcher
        from app.core.config import settings
        # Only start if a Gemini key is configured
        if settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "YOUR_FREE_GEMINI_KEY_HERE":
            start_background_watcher(_on_screen_alert)
            logger.info("✅ Jarvis screen watcher started (VLM passive mode active).")
        else:
            logger.warning(
                "⚠️  GEMINI_API_KEY not set — background screen watcher disabled. "
                "Add your key to .env to enable proactive JARVIS alerts."
            )
    except Exception as e:
        logger.error(f"Screen watcher startup failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Stop watcher cleanly on server shutdown."""
    try:
        from app.services.screen_vision import stop_background_watcher
        stop_background_watcher()
    except Exception:
        pass


# ── Alert polling endpoint ────────────────────────────────────────────────────

@app.get("/alerts")
def get_alerts(clear: bool = True):
    """
    Frontend polls this endpoint to receive proactive JARVIS screen alerts.
    e.g. "Sir, your build just failed. Want me to fix it?"

    Query params:
        clear (bool): If true (default), drain the queue after returning.
    """
    global _watcher_alerts
    alerts = list(_watcher_alerts)
    if clear:
        _watcher_alerts.clear()
    return {"alerts": alerts}
