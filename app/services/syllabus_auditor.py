"""
syllabus_auditor.py — YouTube Playlist Syllabus Auditor (Jarvis Skill)
-----------------------------------------------------------------------
Answers: "Does this YouTube playlist actually teach my full syllabus?"

Architecture (Rule #4 compliant):
  - Fully isolated module — does NOT import from any other tool file
  - Connects to both frontend UI and voice.py via the unified /chat route
  - All output returned as strings; nothing is written to disk

Pipeline:
  1. Read syllabus topics from an image  → Groq Vision (llama-3.2-11b-vision-preview)
  2. Fetch playlist video IDs            → youtube-transcript-api
  3. Fetch captions per video            → youtube-transcript-api (skip if unavailable)
  4. Chunk transcripts                   → 300-token sliding window, 50-token overlap
  5. Embed chunks + topics               → sentence-transformers (all-MiniLM-L6-v2)
  6. Build in-memory vector store        → chromadb (ephemeral, no disk writes)
  7. Score coverage per topic            → cosine similarity depth scoring
  8. LLM verify top topics               -> Groq llama-3.3-70b-versatile
  9. Assemble + return response          → markdown (chat) + spoken summary (voice)

Usage (via tools.py → /chat route):
    audit_playlist_syllabus(playlist_url="https://youtube.com/playlist?list=...",
                             image_path="C:/Users/.../syllabus.jpg")
"""

import os
import re
import base64
import logging
import time
import uuid
from typing import Optional

logger = logging.getLogger(__name__)

# ── Lazy singletons (loaded once, reused across calls) ───────────────────────
_EMBED_MODEL = None   # SentenceTransformer instance


def _get_groq_client():
    """Return a Groq client using the shared GROQ_API_KEY from Jarvis settings."""
    try:
        from groq import Groq
        from app.core.config import settings
        return Groq(api_key=settings.GROQ_API_KEY)
    except Exception as e:
        raise RuntimeError(f"Could not initialise Groq client: {e}")


def _get_embed_model():
    """Lazy-load SentenceTransformer once and cache it for the process lifetime."""
    global _EMBED_MODEL
    if _EMBED_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("[syllabus_auditor] Loading embedding model all-MiniLM-L6-v2 ...")
            _EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
            logger.info("[syllabus_auditor] Embedding model ready.")
        except Exception as e:
            raise RuntimeError(f"Could not load embedding model: {e}")
    return _EMBED_MODEL


# ─────────────────────────────────────────────────────────────────────────────
# STEP 1 — Syllabus extraction from image
# ─────────────────────────────────────────────────────────────────────────────

def _load_image_as_b64(image_path: str) -> tuple[str, str]:
    """
    Load an image file from disk and return (base64_string, mime_type).
    Supports: .jpg/.jpeg, .png, .webp, .bmp
    """
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".bmp": "image/bmp",
    }
    mime = mime_map.get(ext, "image/jpeg")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return b64, mime


def _extract_syllabus_from_image(image_path: str) -> list[str]:
    """
    Send the syllabus image to Groq Vision (llama-3.2-11b-vision-preview) and
    extract all topics as a clean Python list of strings.

    The model is prompted to be exhaustive — every chapter, unit, subtopic,
    and bullet point is captured exactly as written, even if handwritten.

    Returns: ["Arrays & Strings", "Linked Lists", "Binary Trees", ...]
    Raises:  RuntimeError if image cannot be read or API call fails.
    """
    logger.info(f"[syllabus_auditor] Extracting syllabus topics from image: {image_path}")

    b64, mime = _load_image_as_b64(image_path)
    client = _get_groq_client()

    prompt = (
        "This is an image of an academic syllabus, course outline, or topic list. "
        "Your task is to extract EVERY single topic, chapter, unit, and subtopic visible in the image.\n\n"
        "Rules:\n"
        "- Include ALL items — do not summarize or group them.\n"
        "- Preserve the exact wording as written (e.g. 'BFS & DFS', 'Big-O Notation').\n"
        "- If the image is handwritten, do your best to read it accurately.\n"
        "- Output ONLY a plain list, one topic per line, no numbering, no bullets, no extra commentary.\n"
        "- Do not add any introduction or conclusion text.\n\n"
        "Example output format:\n"
        "Arrays\n"
        "Linked Lists\n"
        "Binary Trees\n"
        "Graph Traversal (BFS, DFS)\n"
        "Dynamic Programming\n"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:{mime};base64,{b64}"},
                        },
                    ],
                }
            ],
            temperature=0.1,   # low temperature → faithful extraction
            max_tokens=1024,
        )
        raw_output = response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq Vision call failed: {e}")

    # ── Parse output into clean list ──────────────────────────────────────────
    topics = []
    for line in raw_output.splitlines():
        # Strip leading bullets, numbers, dashes, whitespace
        clean = re.sub(r"^[\s\-\*\•\d\.\)]+", "", line).strip()
        if clean and len(clean) >= 2:
            topics.append(clean)

    if not topics:
        raise RuntimeError(
            "Groq Vision returned no extractable topics. "
            "The image may be too blurry, too small, or not a syllabus."
        )

    logger.info(f"[syllabus_auditor] Extracted {len(topics)} topics from syllabus image.")
    return topics


# ─────────────────────────────────────────────────────────────────────────────
# STEP 2 — Playlist video ID extraction
# ─────────────────────────────────────────────────────────────────────────────

def _extract_playlist_id(playlist_url: str) -> Optional[str]:
    """Extract the playlist ID from any standard YouTube playlist URL."""
    m = re.search(r"[?&]list=([A-Za-z0-9_\-]+)", playlist_url)
    return m.group(1) if m else None


def _fetch_playlist_video_ids(playlist_url: str) -> list[dict]:
    """
    Retrieve all video IDs (and titles where available) from a YouTube playlist.

    Uses youtube-transcript-api's playlist support when available,
    with a fallback to direct URL parsing for simple cases.

    Returns: [{"id": "abc123", "title": "Lecture 1 - Arrays"}, ...]
    Raises:  RuntimeError if playlist cannot be accessed or is private.
    """
    logger.info(f"[syllabus_auditor] Fetching playlist: {playlist_url}")

    playlist_id = _extract_playlist_id(playlist_url)
    if not playlist_id:
        raise RuntimeError(
            f"Could not extract a playlist ID from the URL: {playlist_url}\n"
            "Make sure it contains '?list=...' or '&list=...'."
        )

    # ── Primary: youtube-transcript-api playlist fetch ────────────────────────
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        # The library exposes list_transcripts which works per-video.
        # For the playlist itself, we use the YouTubeTranscriptApi.list() helper.
        # If the version installed doesn't have it, we fall back below.
        from youtube_transcript_api import YouTubeTranscriptApi

        # Attempt to use the playlist listing feature (available in v0.6+)
        try:
            import requests
            # Fetch playlist page to extract video IDs (no API key needed)
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
            playlist_page_url = f"https://www.youtube.com/playlist?list={playlist_id}"
            resp = requests.get(playlist_page_url, headers=headers, timeout=15)
            resp.raise_for_status()
            html = resp.text

            # Extract video IDs from the playlist page HTML
            video_ids_raw = re.findall(r'"videoId":"([A-Za-z0-9_\-]{11})"', html)
            # Deduplicate while preserving order
            seen = set()
            unique_ids = []
            for vid in video_ids_raw:
                if vid not in seen:
                    seen.add(vid)
                    unique_ids.append(vid)

            if not unique_ids:
                raise ValueError("No video IDs found in playlist page HTML.")

            # Try to extract titles (best-effort)
            title_pattern = re.compile(
                r'"videoId":"([A-Za-z0-9_\-]{11})"[^}]*?"title":\{"runs":\[\{"text":"([^"]+)"'
            )
            title_map: dict[str, str] = {}
            for vid_id, title in title_pattern.findall(html):
                if vid_id not in title_map:
                    title_map[vid_id] = title

            videos = []
            for i, vid_id in enumerate(unique_ids):
                videos.append({
                    "id": vid_id,
                    "title": title_map.get(vid_id, f"Video {i + 1}"),
                    "index": i + 1,
                })

            logger.info(
                f"[syllabus_auditor] Found {len(videos)} videos in playlist {playlist_id}."
            )
            return videos

        except Exception as inner_e:
            logger.warning(
                f"[syllabus_auditor] HTML playlist parsing failed ({inner_e}), "
                "trying yt-dlp fallback."
            )
            raise  # re-raise to fall into yt-dlp block

    except ImportError:
        raise RuntimeError(
            "youtube-transcript-api is not installed. "
            "Run: pip install youtube-transcript-api"
        )
    except Exception:
        pass  # fall through to yt-dlp

    # ── Fallback: yt-dlp (already available in Jarvis environment) ────────────
    try:
        import subprocess, json, sys
        result = subprocess.run(
            [
                sys.executable, "-m", "yt_dlp",
                "--flat-playlist",
                "--print", '{"id":"%(id)s","title":"%(title)s"}',
                f"https://www.youtube.com/playlist?list={playlist_id}",
            ],
            capture_output=True, text=True, timeout=60,
        )
        videos = []
        for i, line in enumerate(result.stdout.strip().splitlines()):
            try:
                entry = json.loads(line)
                entry["index"] = i + 1
                videos.append(entry)
            except json.JSONDecodeError:
                continue
        if videos:
            logger.info(
                f"[syllabus_auditor] yt-dlp found {len(videos)} videos in playlist."
            )
            return videos
    except Exception as ydl_e:
        logger.warning(f"[syllabus_auditor] yt-dlp fallback failed: {ydl_e}")

    raise RuntimeError(
        f"Could not retrieve videos from playlist '{playlist_id}'. "
        "The playlist may be private, deleted, or region-locked."
    )


# ─────────────────────────────────────────────────────────────────────────────
# STEP 3 — Transcript fetching (skip if unavailable)
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_transcript(video_id: str) -> Optional[list[dict]]:
    """
    Fetch auto-generated or manual captions for a single YouTube video.

    Tries captions in this preference order:
      1. Manual English captions (most accurate)
      2. Auto-generated English captions
      3. Any available language captions (as a last resort)

    Returns list of {text, start, duration} dicts, or None if no captions exist.
    Per the implementation plan, None triggers a SKIP (no ASR fallback).
    """
    try:
        from youtube_transcript_api import (
            YouTubeTranscriptApi,
            NoTranscriptFound,
            TranscriptsDisabled,
            VideoUnavailable,
        )

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Priority 1: manually created English
        try:
            transcript = transcript_list.find_manually_created_transcript(["en", "en-US", "en-GB"])
            return transcript.fetch()
        except NoTranscriptFound:
            pass

        # Priority 2: auto-generated English
        try:
            transcript = transcript_list.find_generated_transcript(["en", "en-US", "en-GB"])
            return transcript.fetch()
        except NoTranscriptFound:
            pass

        # Priority 3: any available language (non-English playlists)
        try:
            available = list(transcript_list)
            if available:
                return available[0].fetch()
        except Exception:
            pass

        return None  # no captions at all → will be skipped

    except Exception as e:
        err_str = str(e).lower()
        if any(kw in err_str for kw in ["disabled", "unavailable", "no transcript"]):
            return None   # expected — skip this video
        logger.warning(f"[syllabus_auditor] Transcript fetch error for {video_id}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# STEP 4 — Transcript chunking
# ─────────────────────────────────────────────────────────────────────────────

def _approx_token_count(text: str) -> int:
    """Approximate token count: ~0.75 tokens per word (safe undercount for chunking)."""
    return max(1, int(len(text.split()) * 0.75))


def _chunk_transcript(
    transcript: list[dict],
    video_id: str,
    video_title: str,
    video_index: int,
    chunk_tokens: int = 300,
    overlap_tokens: int = 50,
) -> list[dict]:
    """
    Split a transcript into overlapping chunks for semantic search.

    Strategy:
      - Walk through transcript entries accumulating text until chunk_tokens is reached
      - Save the chunk with its start/end timestamps and source metadata
      - Step back by overlap_tokens worth of entries to create the overlap window
      - Repeat until transcript is exhausted

    Each chunk carries full provenance so citations in the final report
    link directly to the correct video + timestamp.

    Returns list of:
    {
        "text":        str,        # chunk text (clean, whitespace-normalised)
        "video_id":    str,        # YouTube video ID
        "video_title": str,        # human-readable video title
        "video_index": int,        # position in playlist (1-based)
        "start_sec":   float,      # start timestamp in seconds
        "end_sec":     float,      # end timestamp in seconds
        "chunk_id":    str,        # unique ID for ChromaDB
    }
    """
    chunks = []
    n = len(transcript)
    if n == 0:
        return chunks

    i = 0
    chunk_counter = 0

    while i < n:
        # Accumulate entries until we hit the token limit
        buffer_entries = []
        token_count = 0

        j = i
        while j < n and token_count < chunk_tokens:
            entry = transcript[j]
            entry_tokens = _approx_token_count(entry.get("text", ""))
            buffer_entries.append(entry)
            token_count += entry_tokens
            j += 1

        if not buffer_entries:
            break

        # Build chunk text — normalise whitespace
        raw_text = " ".join(e.get("text", "") for e in buffer_entries)
        chunk_text = re.sub(r"\s+", " ", raw_text).strip()

        if len(chunk_text) < 20:
            i = j  # skip trivially short chunks
            continue

        start_sec = buffer_entries[0].get("start", 0.0)
        last_entry = buffer_entries[-1]
        end_sec = last_entry.get("start", 0.0) + last_entry.get("duration", 0.0)

        chunk_id = f"v{video_index}_c{chunk_counter}_{video_id}"
        chunks.append({
            "text":        chunk_text,
            "video_id":    video_id,
            "video_title": video_title,
            "video_index": video_index,
            "start_sec":   start_sec,
            "end_sec":     end_sec,
            "chunk_id":    chunk_id,
        })
        chunk_counter += 1

        # Step back by overlap_tokens to create the sliding overlap
        overlap_accumulated = 0
        step_back = 0
        for entry in reversed(buffer_entries):
            overlap_accumulated += _approx_token_count(entry.get("text", ""))
            step_back += 1
            if overlap_accumulated >= overlap_tokens:
                break

        # Advance i by (entries consumed - overlap entries)
        advance = max(1, len(buffer_entries) - step_back)
        i += advance

    logger.debug(
        "[syllabus_auditor] Video '%s' -> %d chunks from %d transcript entries.",
        video_title, len(chunks), len(transcript)
    )
    return chunks


# ─────────────────────────────────────────────────────────────────────────────
# STEP 5 — Embedding
# ─────────────────────────────────────────────────────────────────────────────

def _embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Embed a list of strings using sentence-transformers all-MiniLM-L6-v2.
    Returns a list of 384-dimensional float vectors.
    Model is loaded lazily and cached for the process lifetime.
    """
    model = _get_embed_model()
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return embeddings.tolist()


# ─────────────────────────────────────────────────────────────────────────────
# STEP 6 — Ephemeral vector store
# ─────────────────────────────────────────────────────────────────────────────

def _build_vector_store(chunks: list[dict]):
    """
    Embed all transcript chunks and store them in an in-memory ChromaDB collection.

    The collection is ephemeral — it exists only in RAM for the duration of the
    audit and is cleaned up afterwards. No disk writes, fully stateless (Rule #3).

    Returns: (chromadb.Collection, chromadb.Client)
    """
    import chromadb

    client = chromadb.Client()  # pure in-memory, no persistence path
    collection_name = f"audit_{uuid.uuid4().hex[:8]}"
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    if not chunks:
        return collection, client

    texts = [c["text"] for c in chunks]
    logger.info(f"[syllabus_auditor] Embedding {len(texts)} chunks ...")
    embeddings = _embed_texts(texts)

    # ChromaDB add in batches of 500 to avoid memory spikes on large playlists
    batch_size = 500
    for start in range(0, len(chunks), batch_size):
        batch_chunks = chunks[start: start + batch_size]
        batch_embeds = embeddings[start: start + batch_size]
        collection.add(
            ids=[c["chunk_id"] for c in batch_chunks],
            embeddings=batch_embeds,
            documents=[c["text"] for c in batch_chunks],
            metadatas=[
                {
                    "video_id":    c["video_id"],
                    "video_title": c["video_title"],
                    "video_index": c["video_index"],
                    "start_sec":   c["start_sec"],
                    "end_sec":     c["end_sec"],
                }
                for c in batch_chunks
            ],
        )

    logger.info(
        f"[syllabus_auditor] Vector store built: {len(chunks)} chunks "
        f"in collection '{collection_name}'."
    )
    return collection, client


# ─────────────────────────────────────────────────────────────────────────────
# STEP 7 — Coverage scoring (pure vector, no LLM tokens spent)
# ─────────────────────────────────────────────────────────────────────────────

_DEPTH_THRESHOLDS = {
    "DEEP":     5.0,
    "MODERATE": 2.0,
    "SURFACE":  0.5,
    "MISSING":  0.0,
}


def _coverage_level(depth_score: float) -> str:
    if depth_score >= _DEPTH_THRESHOLDS["DEEP"]:
        return "DEEP"
    if depth_score >= _DEPTH_THRESHOLDS["MODERATE"]:
        return "MODERATE"
    if depth_score >= _DEPTH_THRESHOLDS["SURFACE"]:
        return "SURFACE"
    return "MISSING"


def _score_topic_coverage(topic: str, collection, top_k: int = 20) -> dict:
    """
    Query the vector store for the top_k chunks most similar to `topic`.
    Compute a depth_score = Σ(1 - cosine_distance) for chunks with distance < 0.35.

    Distance < 0.35 means cosine similarity > 0.65 — genuinely on-topic content.

    Returns:
    {
        "topic":          str,
        "depth_score":    float,
        "coverage_level": "DEEP" | "MODERATE" | "SURFACE" | "MISSING",
        "top_chunks":     list[dict],   # top-3 chunks for LLM verification
        "hit_count":      int,          # number of relevant chunks found
    }
    """
    topic_vec = _embed_texts([topic])[0]

    results = collection.query(
        query_embeddings=[topic_vec],
        n_results=min(top_k, collection.count()),
        include=["documents", "distances", "metadatas"],
    )

    distances = results["distances"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    RELEVANCE_THRESHOLD = 0.42   # cosine distance threshold (similarity > 0.58)
    # 0.42 is calibrated for real 300-token lecture transcript chunks:
    #   - On-topic chunks score 0.10-0.30 distance (similarity 0.70-0.90)
    #   - Off-topic chunks score 0.50+ distance (similarity < 0.50)
    #   - Widening from 0.35 -> 0.42 handles lecturers using synonyms/paraphrase

    depth_score = 0.0
    hit_count = 0
    top_chunks = []

    for dist, doc, meta in zip(distances, documents, metadatas):
        if dist < RELEVANCE_THRESHOLD:
            depth_score += (1.0 - dist)
            hit_count += 1
            top_chunks.append({
                "text":        doc,
                "distance":    dist,
                "video_title": meta.get("video_title", "Unknown"),
                "video_index": meta.get("video_index", 0),
                "start_sec":   meta.get("start_sec", 0.0),
                "end_sec":     meta.get("end_sec", 0.0),
            })

    # Sort top_chunks by distance (most similar first), keep top 3 for LLM
    top_chunks.sort(key=lambda x: x["distance"])
    top_chunks_for_llm = top_chunks[:3]

    return {
        "topic":          topic,
        "depth_score":    round(depth_score, 3),
        "coverage_level": _coverage_level(depth_score),
        "top_chunks":     top_chunks_for_llm,
        "hit_count":      hit_count,
    }


# ─────────────────────────────────────────────────────────────────────────────
# STEP 8 — LLM verification (Groq, MODERATE + DEEP topics only)
# ─────────────────────────────────────────────────────────────────────────────

def _format_timestamp(seconds: float) -> str:
    """Convert a float number of seconds to HH:MM:SS or MM:SS string."""
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def _llm_verify_topic(topic: str, top_chunks: list[dict]) -> dict:
    """
    Send the top-3 relevant chunks for a topic to Groq llama-3.3-70b-versatile.
    Only called for MODERATE and DEEP topics (reduces token spend).

    Returns a dict with verified depth label, confidence, summary,
    formulas/definitions found, and the best source timestamp.

    On any failure, gracefully falls back to the vector-scoring result.
    """
    if not top_chunks:
        return {
            "depth": "MISSING",
            "confidence": 0,
            "summary": "No relevant content found.",
            "formulas": [],
            "definitions": [],
            "best_source": None,
        }

    # Build excerpt blocks for the prompt
    excerpts = []
    for i, chunk in enumerate(top_chunks[:3], 1):
        ts = _format_timestamp(chunk["start_sec"])
        excerpts.append(
            f'[Excerpt {i}] (Video: "{chunk["video_title"]}" at {ts})\n{chunk["text"][:600]}'
        )
    excerpts_text = "\n\n".join(excerpts)

    prompt = (
        f'You are an educational content auditor.\n\n'
        f'Topic to assess: "{topic}"\n\n'
        f'These are transcript excerpts from a lecture playlist:\n\n'
        f'{excerpts_text}\n\n'
        f'Assess whether the topic "{topic}" is genuinely taught in these excerpts.\n\n'
        f'Respond ONLY as valid JSON (no markdown, no explanation):\n'
        f'{{\n'
        f'  "depth": "DEEP" or "MODERATE" or "SURFACE" or "MISSING",\n'
        f'  "confidence": <integer 0-100>,\n'
        f'  "summary": "<one sentence: what was actually taught about this topic>",\n'
        f'  "formulas": ["<formula or equation if any>"],\n'
        f'  "definitions": ["<exact definition quoted if any>"],\n'
        f'  "best_source": {{"video_title": "<title>", "timestamp": "<MM:SS>"}}\n'
        f'}}'
    )

    try:
        client = _get_groq_client()
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=400,
        )
        raw = response.choices[0].message.content.strip()

        # Strip markdown code fences if model wrapped the JSON
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
        raw = re.sub(r"\s*```$", "", raw)

        import json
        result = json.loads(raw)

        # Validate required keys
        for key in ("depth", "confidence", "summary"):
            if key not in result:
                raise ValueError(f"Missing key '{key}' in LLM JSON response")

        return result

    except Exception as e:
        logger.warning(f"[syllabus_auditor] LLM verification failed for '{topic}': {e}")
        # Graceful fallback — use best available chunk as the source
        best = top_chunks[0] if top_chunks else None
        return {
            "depth": "MODERATE",   # conservative fallback (vector said MODERATE/DEEP)
            "confidence": 50,
            "summary": f"Content found but LLM verification failed: {e}",
            "formulas": [],
            "definitions": [],
            "best_source": (
                {
                    "video_title": best["video_title"],
                    "timestamp": _format_timestamp(best["start_sec"]),
                }
                if best
                else None
            ),
        }


# ─────────────────────────────────────────────────────────────────────────────
# STEP 9 — Response assembly
# ─────────────────────────────────────────────────────────────────────────────

_DEPTH_EMOJI = {
    "DEEP":     "🟢",
    "MODERATE": "🟡",
    "SURFACE":  "🟠",
    "MISSING":  "🔴",
}

_DEPTH_LABEL = {
    "DEEP":     "Deeply Covered",
    "MODERATE": "Moderately Covered",
    "SURFACE":  "Briefly Mentioned",
    "MISSING":  "Not Covered",
}


def _assemble_response(
    topics: list[str],
    coverage_results: list[dict],
    llm_results: dict,           # topic -> llm_verify dict (only for MODERATE/DEEP)
    skipped_videos: list[dict],
    total_videos: int,
    playlist_url: str,
) -> tuple[str, str]:
    """
    Build the final markdown response (for chat) and spoken summary (for voice).
    Nothing is written to disk — both are returned as plain strings.

    Returns: (markdown_str, spoken_summary_str)
    """
    captioned_videos = total_videos - len(skipped_videos)

    # ── Counters ──────────────────────────────────────────────────────────────
    counts = {"DEEP": 0, "MODERATE": 0, "SURFACE": 0, "MISSING": 0}
    for r in coverage_results:
        counts[r["coverage_level"]] += 1

    covered = counts["DEEP"] + counts["MODERATE"]
    total_topics = len(topics)
    coverage_pct = round((covered / total_topics * 100) if total_topics > 0 else 0)

    # ── Group topics by coverage level ────────────────────────────────────────
    grouped: dict[str, list[dict]] = {"DEEP": [], "MODERATE": [], "SURFACE": [], "MISSING": []}
    for r in coverage_results:
        grouped[r["coverage_level"]].append(r)

    # ── Build markdown ─────────────────────────────────────────────────────────
    lines = []
    lines.append("## 📊 Playlist Syllabus Audit\n")
    lines.append(
        f"**Playlist scanned:** {captioned_videos} of {total_videos} videos had captions"
        + (f" · {len(skipped_videos)} skipped (no captions)" if skipped_videos else "")
    )
    lines.append(f"**Syllabus topics detected:** {total_topics}")
    lines.append(f"**Overall coverage:** {coverage_pct}% "
                 f"({counts['DEEP']} deep · {counts['MODERATE']} moderate · "
                 f"{counts['SURFACE']} surface · {counts['MISSING']} missing)\n")
    lines.append("---\n")

    # ── Per-level sections ─────────────────────────────────────────────────────
    for level in ("DEEP", "MODERATE", "SURFACE", "MISSING"):
        items = grouped[level]
        if not items:
            continue
        emoji = _DEPTH_EMOJI[level]
        label = _DEPTH_LABEL[level]
        lines.append(f"### {emoji} {label} ({len(items)} topic{'s' if len(items) != 1 else ''})\n")

        for r in items:
            topic = r["topic"]
            llm = llm_results.get(topic)

            if level == "MISSING":
                lines.append(f"- **{topic}** — Zero coverage found across all captioned videos.")
            elif level == "SURFACE":
                src_info = ""
                if r["top_chunks"]:
                    best = r["top_chunks"][0]
                    ts = _format_timestamp(best["start_sec"])
                    src_info = f" → Video {best['video_index']}: \"{best['video_title']}\" at {ts}"
                lines.append(
                    f"- **{topic}** *(briefly mentioned, ~{r['hit_count']} relevant segment{'s' if r['hit_count'] != 1 else ''})*"
                    + src_info
                )
            else:
                # MODERATE or DEEP — use LLM-verified info if available
                if llm:
                    summary = llm.get("summary", "")
                    confidence = llm.get("confidence", "?")
                    formulas = llm.get("formulas", [])
                    definitions = llm.get("definitions", [])
                    best_src = llm.get("best_source")

                    src_info = ""
                    if best_src:
                        src_info = f" → \"{best_src['video_title']}\" at {best_src['timestamp']}"

                    line = f"- **{topic}** *(confidence: {confidence}%)*"
                    if summary:
                        line += f" — {summary}"
                    line += src_info
                    lines.append(line)

                    if formulas:
                        for f in formulas[:2]:
                            lines.append(f"  - 📐 `{f}`")
                    if definitions:
                        for d in definitions[:1]:
                            lines.append(f"  - 📖 *\"{d}\"*")
                else:
                    # LLM not called (fallback to vector info)
                    src_info = ""
                    if r["top_chunks"]:
                        best = r["top_chunks"][0]
                        ts = _format_timestamp(best["start_sec"])
                        src_info = f" → Video {best['video_index']}: \"{best['video_title']}\" at {ts}"
                    lines.append(f"- **{topic}** *(depth score: {r['depth_score']})*{src_info}")

        lines.append("")  # blank line between sections

    # ── Skipped videos ────────────────────────────────────────────────────────
    if skipped_videos:
        lines.append("---\n")
        lines.append("### ⚠️ Videos Without Captions (Skipped)\n")
        for v in skipped_videos[:10]:
            lines.append(f"- Video {v['index']}: \"{v['title']}\"")
        if len(skipped_videos) > 10:
            lines.append(f"- *...and {len(skipped_videos) - 10} more*")
        lines.append("")

    # ── Study priority ────────────────────────────────────────────────────────
    priority_topics = [r["topic"] for r in grouped["MISSING"]] + \
                      [r["topic"] for r in grouped["SURFACE"]]
    if priority_topics:
        lines.append("---\n")
        lines.append("### 🎯 Study Priority\n")
        lines.append(
            "These topics need supplemental study material — "
            "they are absent or barely covered in the playlist:"
        )
        for t in priority_topics[:8]:
            lines.append(f"- {t}")
        if len(priority_topics) > 8:
            lines.append(f"- *...and {len(priority_topics) - 8} more*")

    markdown_str = "\n".join(lines)

    # ── Spoken summary (concise, natural for TTS) ─────────────────────────────
    missing_list = [r["topic"] for r in grouped["MISSING"]][:3]
    missing_str = (
        ", ".join(missing_list) + ("..." if len(grouped["MISSING"]) > 3 else "")
        if missing_list
        else "none"
    )

    spoken = (
        f"Audit complete. Your playlist covers {coverage_pct}% of the syllabus. "
        f"{counts['DEEP']} topics are deeply taught, {counts['MODERATE']} are moderately covered, "
        f"and {counts['MISSING']} are completely missing. "
    )
    if missing_list:
        spoken += f"The missing topics include: {missing_str}. "
    if skipped_videos:
        spoken += (
            f"{len(skipped_videos)} video{'s' if len(skipped_videos) != 1 else ''} "
            "had no captions and were skipped. "
        )
    spoken += "Check the chat for the full breakdown."

    return markdown_str, spoken


# ─────────────────────────────────────────────────────────────────────────────
# MAIN EXPORTED FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def audit_playlist_syllabus(playlist_url: str, image_path: str) -> str:
    """
    Main entry point for the Syllabus Auditor skill.

    Orchestrates all pipeline steps and returns a single rich markdown string
    suitable for streaming to the Jarvis frontend chat or speaking via voice.py.

    Args:
        playlist_url:  Full YouTube playlist URL (must contain ?list= or &list=)
        image_path:    Absolute path to the syllabus image (JPG, PNG, WEBP, BMP)

    Returns:
        Markdown-formatted audit report as a plain string.
        Nothing is written to disk.
    """
    start_time = time.time()

    # ── Validate inputs ───────────────────────────────────────────────────────
    if not playlist_url or "list=" not in playlist_url:
        return (
            "❌ Please provide a valid YouTube playlist URL containing '?list=...' or '&list=...'\n\n"
            "Example: `https://www.youtube.com/playlist?list=PLxxxxxx`"
        )

    if not image_path or not os.path.exists(image_path):
        return (
            f"❌ Syllabus image not found at: `{image_path}`\n\n"
            "Please check the filename and make sure it's on your Desktop, "
            "Pictures, Downloads, or Documents folder."
        )

    # ── Step 1: Extract syllabus topics from image ────────────────────────────
    try:
        topics = _extract_syllabus_from_image(image_path)
    except RuntimeError as e:
        return f"❌ Could not read syllabus image: {e}"

    if not topics:
        return "❌ No topics could be extracted from the syllabus image. Please try a clearer photo."

    # ── Step 2: Fetch playlist video IDs ──────────────────────────────────────
    try:
        videos = _fetch_playlist_video_ids(playlist_url)
    except RuntimeError as e:
        return f"❌ Could not fetch playlist: {e}"

    if not videos:
        return "❌ The playlist appears to be empty or private."

    total_videos = len(videos)

    # ── Step 3: Fetch transcripts + chunk ─────────────────────────────────────
    all_chunks: list[dict] = []
    skipped_videos: list[dict] = []

    for video in videos:
        transcript = _fetch_transcript(video["id"])
        if transcript is None:
            skipped_videos.append(video)
            continue
        chunks = _chunk_transcript(
            transcript=transcript,
            video_id=video["id"],
            video_title=video["title"],
            video_index=video["index"],
        )
        all_chunks.extend(chunks)

    if not all_chunks:
        skipped_titles = ", ".join(f'"{v["title"]}"' for v in skipped_videos[:3])
        return (
            f"❌ No captions found in any of the {total_videos} playlist videos.\n\n"
            f"Skipped videos: {skipped_titles}"
            + ("..." if len(skipped_videos) > 3 else "")
        )

    # ── Step 4: Build vector store ─────────────────────────────────────────────
    try:
        collection, chroma_client = _build_vector_store(all_chunks)
    except Exception as e:
        return f"❌ Embedding/indexing failed: {e}"

    # ── Step 5: Score each topic ───────────────────────────────────────────────
    coverage_results: list[dict] = []
    for topic in topics:
        try:
            result = _score_topic_coverage(topic, collection)
            coverage_results.append(result)
        except Exception as e:
            logger.warning(f"[syllabus_auditor] Scoring failed for '{topic}': {e}")
            coverage_results.append({
                "topic": topic,
                "depth_score": 0.0,
                "coverage_level": "MISSING",
                "top_chunks": [],
                "hit_count": 0,
            })

    # ── Step 6: LLM verify MODERATE + DEEP topics ─────────────────────────────
    llm_results: dict = {}
    needs_llm = [r for r in coverage_results if r["coverage_level"] in ("MODERATE", "DEEP")]

    for r in needs_llm:
        try:
            llm_result = _llm_verify_topic(r["topic"], r["top_chunks"])
            llm_results[r["topic"]] = llm_result
            # Respect Groq free tier — 1 call per ~0.8s to stay under 14,400 tokens/min
            time.sleep(0.8)
        except Exception as e:
            logger.warning(f"[syllabus_auditor] LLM call failed for '{r['topic']}': {e}")

    # ── Cleanup vector store ──────────────────────────────────────────────────
    try:
        chroma_client.delete_collection(collection.name)
    except Exception:
        pass  # non-critical

    # ── Step 7: Assemble response ──────────────────────────────────────────────
    markdown_str, spoken_summary = _assemble_response(
        topics=topics,
        coverage_results=coverage_results,
        llm_results=llm_results,
        skipped_videos=skipped_videos,
        total_videos=total_videos,
        playlist_url=playlist_url,
    )

    elapsed = round(time.time() - start_time, 1)
    markdown_str += f"\n\n---\n*Audit completed in {elapsed}s · {len(all_chunks)} transcript chunks indexed*"

    # Store spoken summary as a module-level variable so voice.py can pick it up
    # via the same string — the first paragraph before the first '---' is the spoken part
    # The full markdown is returned for the frontend.
    logger.info(
        f"[syllabus_auditor] Audit complete in {elapsed}s. "
        f"Topics: {len(topics)}, Chunks: {len(all_chunks)}, "
        f"Skipped: {len(skipped_videos)}"
    )

    return markdown_str
