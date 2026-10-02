"""
voice.py — Jarvis Voice Engine
------------------------------
STT  Groq whisper-large-v3-turbo (primary): ~0.3–0.8 s, accurate English + Hindi,
     auto language detection. Local faster-whisper ('base', int8) is the fallback
     and quota saver: ~1.7 s per clip on this CPU and weak at Hindi, so not primary.
     Hindi comes back in Devanagari and is romanized (hinglish_normalizer) so the
     keyword router / LLM see the same Hinglish they get from the UI.

TTS  edge-tts neural voices, streamed and decoded on the fly (PyAV) into one
     sounddevice output stream, so the first word plays before synthesis finishes:
       English        → en-GB-RyanNeural   (British, movie-Jarvis-like)
       Hindi/Hinglish → hi-IN-MadhurNeural, fed Devanagari for Hindi words
                        (romanized "kya hai" is otherwise read with English phonetics)
     Offline fallback → Windows SAPI (instant, robotic, but never silent).
     Kokoro ONNX was removed from the hot path: 13–30 s per sentence on this CPU.

Speaker  Queued, pipelined (next sentence synthesises while the current one plays),
     interruptible, multi-channel: one Channel per concurrent command, so replies
     to parallel commands never talk over each other.

Public API kept for other callers: transcribe_audio(path) -> str,
speak_text(text), speak_stream(async_gen).
"""

import asyncio
import io
import logging
import os
import re
import threading
import time
import wave
from collections import deque, OrderedDict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

import numpy as np

from app.core.config import settings
from app.services.hinglish_normalizer import (
    loanword_ratio,
    devanagari_to_hinglish,
    hinglish_to_devanagari,
    strip_markdown,
    normalize_for_tts,  # noqa: F401  (re-exported for older callers)
)

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
if settings.HF_API_KEY:
    os.environ.setdefault("HF_TOKEN", settings.HF_API_KEY)

logger = logging.getLogger(__name__)

STT_RATE = 16000
TTS_RATE = 24000
_DEVANAGARI_RE = re.compile(r"[ऀ-ॿ]")
_ARABIC_RE = re.compile(r"[؀-ۿ]")


# ═════════════════════════════════════════════════════════════════════════════
#  STT
# ═════════════════════════════════════════════════════════════════════════════

@dataclass
class Transcript:
    text: str        # romanized, ready for /chat
    raw: str         # as recognised (Hindi in Devanagari)
    lang: str        # 'en' | 'hi' | ''
    source: str      # 'groq' | 'local' | ''
    logprob: float = 0.0    # mean avg_logprob of kept segments (closer to 0 = surer)
    no_speech: float = 0.0  # max no_speech_prob of kept segments

    def confident(self, min_logprob: float = -0.8, max_no_speech: float = 0.4) -> bool:
        """Strict check used when there is no wake word to vouch for the audio."""
        return self.logprob >= min_logprob and self.no_speech <= max_no_speech


_EMPTY = Transcript("", "", "", "")

# Whisper's classic "silence" hallucinations (YouTube-subtitle training data).
# Short real answers ("okay", "thanks") are NOT listed: Silero VAD already
# guarantees there was speech, and follow-up answers must get through.
_HALLUCINATIONS = {
    "you", "thank you for watching", "thanks for watching", "please subscribe",
    "subtitles by", "like and subscribe", "see you next time", "thank you for listening",
    "you can find me on twitter", "follow me on instagram", "transcribe in english",
    "silence", "...", ". . .", "amém", "увидимся!",
    "सब्सक्राइब करें", "धन्यवाद देखने के लिए",
}


def _clean_transcript(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    low = text.lower().strip(" .!?,।")
    if len(low) < 2 or low in _HALLUCINATIONS or low.startswith("subtitles by"):
        return ""
    return text


def pcm_to_wav_bytes(pcm: np.ndarray, rate: int = STT_RATE) -> bytes:
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(pcm.astype(np.int16).tobytes())
    return buf.getvalue()


# ── Groq (primary) ────────────────────────────────────────────────────────────
_groq_client = None
_groq_quota = {"remaining": None, "cooldown_until": 0.0}
_HINDI_LIKE = {"hindi", "urdu", "punjabi", "nepali", "marathi", "bengali", "gujarati",
               "sindhi", "hi", "ur", "pa", "ne", "mr", "bn", "gu", "sd"}


def _get_groq():
    global _groq_client
    if _groq_client is None and settings.GROQ_API_KEY:
        from groq import AsyncGroq
        _groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY, max_retries=0)
    return _groq_client


def groq_stt_available() -> bool:
    return (settings.JARVIS_STT_MODE != "local" and bool(settings.GROQ_API_KEY)
            and time.time() >= _groq_quota["cooldown_until"])


def groq_quota_low() -> bool:
    rem = _groq_quota["remaining"]
    return rem is not None and rem < 150


def _seg_get(seg, key, default=None):
    return seg.get(key, default) if isinstance(seg, dict) else getattr(seg, key, default)


async def _groq_once(wav: bytes, language: str | None) -> tuple[str, str, float, float]:
    client = _get_groq()
    kwargs = {"language": language} if language else {}
    raw = await client.audio.transcriptions.with_raw_response.create(
        file=("speech.wav", wav),
        model=settings.JARVIS_STT_MODEL,
        temperature=0.0,
        response_format="verbose_json",
        # No prompt: a "Jarvis" prompt made Whisper output "Jarvis" for pure noise,
        # which woke Jarvis up on its own.
        timeout=6.0,
        **kwargs,
    )
    try:
        rem = raw.headers.get("x-ratelimit-remaining-requests")
        if rem is not None:
            _groq_quota["remaining"] = int(rem)
    except Exception:
        pass
    r = await raw.parse()
    segs = getattr(r, "segments", None) or []
    logprob, no_speech = 0.0, 0.0
    if segs:
        kept = [s for s in segs
                if float(_seg_get(s, "no_speech_prob", 0.0) or 0.0) < 0.6
                and float(_seg_get(s, "avg_logprob", 0.0) or 0.0) > -1.0]
        text = " ".join(str(_seg_get(s, "text", "")).strip() for s in kept).strip()
        if kept:
            logprob = sum(float(_seg_get(s, "avg_logprob", 0.0) or 0.0) for s in kept) / len(kept)
            no_speech = max(float(_seg_get(s, "no_speech_prob", 0.0) or 0.0) for s in kept)
    else:
        text = (r.text or "").strip()
    return text, str(getattr(r, "language", "") or "").lower(), logprob, no_speech


async def _transcribe_groq(wav: bytes) -> tuple[str, str, float, float]:
    """Returns (text, 'en'|'hi', logprob, no_speech). Raises on network/API failure."""
    try:
        text, lang, lp, ns = await _groq_once(wav, None)
        if _ARABIC_RE.search(text) or (lang not in ("english", "en", "hindi", "hi") and lang in _HINDI_LIKE):
            text, lang, lp, ns = await _groq_once(wav, "hi")
        elif lang not in ("english", "en", "hindi", "hi"):
            # e.g. accented English detected as Welsh/Norwegian
            text, lang, lp, ns = await _groq_once(wav, "en")
    except Exception as e:
        name = type(e).__name__
        if "RateLimit" in name or "429" in str(e):
            _groq_quota["cooldown_until"] = time.time() + 60
            logger.warning("[STT] Groq rate-limited — local Whisper for 60 s")
        raise
    code = "hi" if lang in ("hindi", "hi") or _DEVANAGARI_RE.search(text) else "en"
    return text, code, lp, ns


# ── Local faster-whisper (fallback) ───────────────────────────────────────────
_whisper_models: dict[str, object] = {}
_whisper_lock = threading.Lock()
FAST_LOCAL_MODEL = "tiny"   # ~0.75 s: only used to spot "Jarvis …" while Jarvis himself is talking


def _load_whisper_model(name: str | None = None):
    name = name or settings.JARVIS_STT_LOCAL
    with _whisper_lock:
        if name in _whisper_models:
            return _whisper_models[name]
        try:
            from faster_whisper import WhisperModel
            _whisper_models[name] = WhisperModel(
                name,
                device="cpu",
                compute_type="int8",
                cpu_threads=6,   # i9-13900H has 6 P-cores; more threads land on E-cores and get slower
                download_root=os.path.join(os.path.dirname(__file__), "..", "..", "models"),
            )
            logger.info(f"[STT] Local Whisper '{name}' loaded")
        except Exception as e:
            logger.warning(f"[STT] Local Whisper '{name}' load failed: {e}")
            return None   # not cached — next call retries
        return _whisper_models[name]


def _transcribe_local_sync(audio: np.ndarray | str, model_name: str | None = None) -> tuple[str, str, float, float]:
    model = _load_whisper_model(model_name)
    if model is None:
        raise RuntimeError("Local Whisper unavailable")
    if isinstance(audio, np.ndarray) and audio.dtype != np.float32:
        audio = audio.astype(np.float32) / 32768.0

    def _run(language):
        segs, info = model.transcribe(
            audio, language=language, beam_size=1, temperature=0.0,
            condition_on_previous_text=False, without_timestamps=True,
            no_speech_threshold=0.6, log_prob_threshold=-1.0,
            vad_filter=isinstance(audio, str),
            # Small models write Hindi in Urdu script unless shown Devanagari first
            initial_prompt="हाँ, मैं हिंदी में बात कर रहा हूँ।" if language == "hi" else None,
        )
        kept = [s for s in segs if s.no_speech_prob < 0.6]
        lp = sum(s.avg_logprob for s in kept) / len(kept) if kept else -9.0
        ns = max((s.no_speech_prob for s in kept), default=1.0)
        return " ".join(s.text.strip() for s in kept).strip(), info, lp, ns

    text, info, lp, ns = _run(None)
    lang = info.language
    if lang not in ("en", "hi") or _ARABIC_RE.search(text) or (lang == "hi" and not _DEVANAGARI_RE.search(text)):
        probs = dict(info.all_language_probs or [])
        lang = "hi" if probs.get("hi", 0) + probs.get("ur", 0) > probs.get("en", 0) else "en"
        text, _, lp, ns = _run(lang)
    return text, ("hi" if lang == "hi" or _DEVANAGARI_RE.search(text) else "en"), lp, ns


async def _transcribe_local(audio, model_name: str | None = None) -> tuple[str, str, float, float]:
    return await asyncio.get_running_loop().run_in_executor(None, _transcribe_local_sync, audio, model_name)


# ── Public STT ────────────────────────────────────────────────────────────────

def _finish(text: str, lang: str, source: str, logprob: float = 0.0, no_speech: float = 0.0) -> Transcript:
    raw = _clean_transcript(text)
    if not raw:
        return _EMPTY
    letters = [c for c in raw if c.isascii() and c.isalpha()]
    if len(letters) >= 6 and sum(c.isupper() for c in letters) / len(letters) > 0.7:
        raw = raw.lower().capitalize().replace("jarvis", "Jarvis")   # Whisper sometimes SHOUTS
    if lang == "hi" and loanword_ratio(raw) >= 0.6:
        lang = "en"   # English words Whisper wrote in Devanagari: the user spoke English
    return Transcript(devanagari_to_hinglish(raw).strip(), raw, lang, source, logprob, no_speech)


# ── Reply-language guard (voice) ──────────────────────────────────────────────

def language_mismatch(sentence: str, target: str) -> bool:
    """True if a reply sentence is in the other language than the one the user spoke."""
    from app.services.context_classifier import detect_language
    if len(re.findall(r"[A-Za-zऀ-ॿ]{2,}", sentence)) < 3:
        return False            # names, "Done.", numbers — nothing to translate
    has_dev = bool(_DEVANAGARI_RE.search(sentence))
    if target == "hi":
        return not has_dev and detect_language(sentence) == "english"
    return has_dev or detect_language(sentence) in ("hindi", "hinglish")


async def translate_for_speech(sentence: str, target: str) -> str:
    """
    Translate one reply sentence into the user's language (canned tool/flow replies
    in chat.py are English-only). ~0.6 s on Groq; returns the original on failure.
    """
    client = _get_groq()
    if client is None:
        return sentence
    if target == "hi":
        instr = ("Translate this line from a voice assistant into natural spoken Hindi as used in "
                 "India, written in Devanagari. Keep names, app names, numbers and file names in "
                 "Latin letters. Output only the translation.")
    else:
        instr = ("Translate this line from a voice assistant into natural English. "
                 "Output only the translation.")
    for model in ("openai/gpt-oss-20b", "openai/gpt-oss-120b"):   # separate Groq token buckets
        try:
            r = await client.chat.completions.create(
                model=model, reasoning_effort="low", temperature=0.2, max_tokens=300,
                messages=[{"role": "system", "content": instr}, {"role": "user", "content": sentence}],
                timeout=4.0,
            )
            out = (r.choices[0].message.content or "").strip()
            if out:
                return out
        except Exception as e:
            logger.warning(f"[TTS] translate via {model} failed: {str(e)[:120]}")
    return sentence


async def transcribe_pcm(pcm: np.ndarray, prefer_local: bool = False, fast: bool = False) -> Transcript:
    """
    Transcribe one VAD-segmented utterance (int16 mono 16 kHz).
    prefer_local=True uses local Whisper even when Groq is up (quota saver for
    speech that is probably not for us, e.g. while Jarvis is talking).
    fast=True (with prefer_local) uses the tiny model: good enough to spot the wake word.
    Never raises; returns an empty Transcript on failure.
    """
    if pcm is None or len(pcm) < STT_RATE * 0.25:
        return _EMPTY
    use_groq = groq_stt_available() and not prefer_local
    if use_groq:
        try:
            text, lang, lp, ns = await _transcribe_groq(pcm_to_wav_bytes(pcm))
            return _finish(text, lang, "groq", lp, ns)
        except Exception as e:
            logger.warning(f"[STT] Groq failed ({type(e).__name__}: {str(e)[:80]}) — local fallback")
    try:
        name = FAST_LOCAL_MODEL if (fast and prefer_local) else None
        text, lang, lp, ns = await _transcribe_local(pcm, name)
        return _finish(text, lang, "local", lp, ns)
    except Exception as e:
        logger.warning(f"[STT] Local failed: {e}")
        if not use_groq and groq_stt_available():
            try:
                text, lang, lp, ns = await _transcribe_groq(pcm_to_wav_bytes(pcm))
                return _finish(text, lang, "groq", lp, ns)
            except Exception:
                pass
    return _EMPTY


async def transcribe_audio(file_path: str) -> str:
    """Back-compat: transcribe a WAV file path → romanized text ('' on failure)."""
    try:
        with wave.open(file_path, "rb") as wf:
            pcm = np.frombuffer(wf.readframes(wf.getnframes()), np.int16)
            rate = wf.getframerate()
        if rate != STT_RATE:
            raise ValueError("resample")
        return (await transcribe_pcm(pcm)).text
    except Exception:
        try:
            if groq_stt_available():
                with open(file_path, "rb") as f:
                    text, lang, _, _ = await _transcribe_groq(f.read())
            else:
                text, lang, _, _ = await _transcribe_local(file_path)
            return _finish(text, lang, "").text
        except Exception as e:
            logger.warning(f"[STT] transcribe_audio failed: {e}")
            return ""


def preload_local_stt():
    """Load the local Whisper models in the background (voice agent startup)."""
    # Import on the calling thread first: importing faster_whisper from two threads at
    # once (loader + VAD setup) trips Python's module-lock deadlock detection.
    import faster_whisper  # noqa: F401
    import faster_whisper.vad  # noqa: F401

    def _load():
        _load_whisper_model(FAST_LOCAL_MODEL)
        _load_whisper_model()
    threading.Thread(target=_load, daemon=True, name="whisper-loader").start()


# ═════════════════════════════════════════════════════════════════════════════
#  TTS — synthesis
# ═════════════════════════════════════════════════════════════════════════════

class Clip:
    """PCM (int16, 24 kHz) that fills while synthesis streams; playable immediately."""

    def __init__(self, text: str, lang: str):
        self.text, self.lang = text, lang
        self.chunks: list[np.ndarray] = []
        self.done = False
        self.ok = True
        self._evt = asyncio.Event()
        self.task: asyncio.Task | None = None

    def push(self, arr: np.ndarray):
        if arr.size:
            self.chunks.append(arr)
            self._evt.set()

    def finish(self, ok: bool = True):
        self.done, self.ok = True, ok
        self._evt.set()

    async def iter_chunks(self):
        i = 0
        while True:
            if i < len(self.chunks):
                yield self.chunks[i]
                i += 1
                continue
            if self.done:
                return
            self._evt.clear()
            await self._evt.wait()

    def cancel(self):
        if self.task and not self.task.done():
            self.task.cancel()


_clip_cache: "OrderedDict[tuple, list[np.ndarray]]" = OrderedDict()
_CACHE_MAX_TEXT = 60


def route_language(text: str, hint: str | None) -> str:
    """'hi' → Hindi voice, 'en' → English voice, for one sentence."""
    if _DEVANAGARI_RE.search(text):
        return "hi"
    if hint == "hi":
        return "hi"   # one consistent voice per Hindi/Hinglish reply; Madhur reads English fine
    from app.services.context_classifier import detect_language
    lang = detect_language(text)
    if hint == "en":
        return "hi" if lang == "hindi" else "en"
    return "en" if lang == "english" else "hi"


def _voice_for(lang: str) -> tuple[str, str]:
    if lang == "hi":
        return settings.JARVIS_VOICE_HI, settings.JARVIS_VOICE_RATE_HI
    return settings.JARVIS_VOICE_EN, settings.JARVIS_VOICE_RATE_EN


async def _synth_edge(text: str, lang: str, clip: Clip) -> bool:
    import av
    import edge_tts
    voice, rate = _voice_for(lang)
    spoken = hinglish_to_devanagari(text) if lang == "hi" else text
    codec = av.CodecContext.create("mp3", "r")
    resampler = av.AudioResampler(format="s16", layout="mono", rate=TTS_RATE)

    def _decode(packets):
        for pkt in packets:
            for frame in codec.decode(pkt):
                for out in resampler.resample(frame):
                    clip.push(out.to_ndarray().reshape(-1).copy())

    got_audio = False
    stream = edge_tts.Communicate(spoken, voice, rate=rate).stream().__aiter__()
    while True:
        try:
            # edge-tts occasionally stalls mid-stream; don't let one sentence hang the queue
            chunk = await asyncio.wait_for(stream.__anext__(), timeout=4.0)
        except StopAsyncIteration:
            break
        if chunk.get("type") == "audio" and chunk.get("data"):
            got_audio = True
            _decode(codec.parse(chunk["data"]))
    _decode(codec.parse(b""))
    try:
        _decode([None])  # flush decoder
    except Exception:
        pass
    return got_audio


def _sapi_sync(text: str) -> np.ndarray:
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    try:
        voice = win32com.client.Dispatch("SAPI.SpVoice")
        for tok in voice.GetVoices():   # prefer a British voice for the Jarvis feel
            if "Great Britain" in tok.GetDescription():
                voice.Voice = tok
                break
        stream = win32com.client.Dispatch("SAPI.SpMemoryStream")
        fmt = win32com.client.Dispatch("SAPI.SpAudioFormat")
        fmt.Type = 26                     # SAFT24kHz16BitMono
        stream.Format = fmt
        voice.AudioOutputStream = stream
        voice.Speak(text)
        return np.frombuffer(bytes(stream.GetData()), dtype=np.int16).copy()
    finally:
        pythoncom.CoUninitialize()


async def _synthesize(clip: Clip):
    key = (clip.lang, clip.text)
    cached = _clip_cache.get(key)
    if cached is not None:
        _clip_cache.move_to_end(key)
        for arr in cached:
            clip.push(arr)
        clip.finish(True)
        return
    ok = False
    for attempt in range(2):
        try:
            ok = await _synth_edge(clip.text, clip.lang, clip)
        except asyncio.CancelledError:
            clip.finish(False)
            raise
        except Exception as e:
            logger.warning(f"[TTS] edge-tts attempt {attempt + 1} failed ({type(e).__name__}: {str(e)[:80]})")
        if ok or clip.chunks:     # partial audio already queued/playing — don't restart the sentence
            ok = ok or bool(clip.chunks)
            break
    if not ok and not clip.chunks:
        try:
            # SAPI has no Hindi voice here; the romanized text is the best effort
            arr = await asyncio.get_running_loop().run_in_executor(None, _sapi_sync, clip.text)
            clip.push(arr)
            ok = True
        except Exception as e:
            logger.warning(f"[TTS] SAPI failed: {e}")
    if ok and len(clip.text) <= _CACHE_MAX_TEXT:
        _clip_cache[key] = list(clip.chunks)
        while len(_clip_cache) > 64:
            _clip_cache.popitem(last=False)
    clip.finish(ok)


def start_clip(text: str, lang_hint: str | None = None) -> Clip:
    """Begin synthesising `text` now; returns a Clip that can be played while it fills."""
    text = strip_markdown(text)
    clip = Clip(text, route_language(text, lang_hint))
    clip.task = asyncio.get_running_loop().create_task(_synthesize(clip))
    return clip


async def prewarm(texts: list[str], lang_hint: str | None = None):
    """Synthesise short stock phrases (greetings, acks) into the cache for instant replies."""
    for t in texts:
        try:
            clip = start_clip(t, lang_hint)
            await clip.task
        except Exception:
            pass


# ═════════════════════════════════════════════════════════════════════════════
#  TTS — playback
# ═════════════════════════════════════════════════════════════════════════════

class _Player:
    """
    One persistent 24 kHz output stream driven by a callback that pulls from a
    sample queue. Audio stays smooth no matter how busy the event loop is (the
    previous executor-per-block writer under-ran and stretched every sentence).
    """

    PREBUFFER = int(TTS_RATE * 0.2)   # start a streamed clip once 200 ms is ready

    def __init__(self):
        import sounddevice as sd
        self._sd = sd
        self._buf: deque = deque()
        self._pending = 0
        self._lock = threading.Lock()
        self._stream = None
        self._levels: deque = deque(maxlen=256)   # (monotonic time, output RMS) per block

    def output_level(self, window: float = 0.3) -> float:
        """Loudest output RMS in the last `window` s — the voice agent's echo reference."""
        now = time.monotonic()
        try:
            return max((lvl for t, lvl in list(self._levels) if now - t <= window), default=0.0)
        except Exception:
            return 0.0

    def _callback(self, outdata, frames, time_info, status):
        out = outdata[:, 0]
        filled = 0
        with self._lock:
            while filled < frames and self._buf:
                arr = self._buf[0]
                n = min(len(arr), frames - filled)
                out[filled:filled + n] = arr[:n]
                if n == len(arr):
                    self._buf.popleft()
                else:
                    self._buf[0] = arr[n:]
                filled += n
            self._pending -= filled
        if filled < frames:
            out[filled:] = 0
        if filled:
            self._levels.append((time.monotonic(),
                                 float(np.sqrt(np.mean(out[:filled].astype(np.float32) ** 2)))))

    def _ensure(self):
        if self._stream is not None and not self._stream.active:
            try:
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        if self._stream is None:
            self._stream = self._sd.OutputStream(samplerate=TTS_RATE, channels=1, dtype="int16",
                                                 callback=self._callback)
            self._stream.start()

    def _push(self, arr: np.ndarray):
        with self._lock:
            self._buf.append(arr)
            self._pending += len(arr)

    def clear(self):
        with self._lock:
            self._buf.clear()
            self._pending = 0

    @property
    def pending(self) -> int:
        return self._pending

    async def play(self, clip: Clip, should_stop=lambda: False) -> bool:
        """Play a clip as it arrives. Returns False if interrupted."""
        try:
            self._ensure()
        except Exception as e:
            logger.warning(f"[TTS] audio device error: {e}")
            clip.cancel()
            return False
        held: list[np.ndarray] = []
        held_n = 0
        started = False
        async for arr in clip.iter_chunks():
            if should_stop():
                self.clear()
                return False
            if started:
                self._push(arr)
                continue
            held.append(arr)
            held_n += len(arr)
            if held_n >= self.PREBUFFER:
                for h in held:
                    self._push(h)
                started = True
        for h in held if not started else []:
            self._push(h)
        while self._pending > 0:
            if should_stop():
                self.clear()
                return False
            await asyncio.sleep(0.02)
        # Device latency: let the last samples actually leave the speaker
        try:
            await asyncio.sleep(min(float(self._stream.latency or 0.05), 0.3))
        except Exception:
            await asyncio.sleep(0.05)
        return True


_player: _Player | None = None


def get_player() -> _Player:
    global _player
    if _player is None:
        _player = _Player()
    return _player


# ═════════════════════════════════════════════════════════════════════════════
#  Sentence splitting for streamed LLM text
# ═════════════════════════════════════════════════════════════════════════════

_ABBREV = re.compile(r"\b(?:Mr|Mrs|Ms|Dr|St|vs|etc|e\.g|i\.e|No)\.$", re.IGNORECASE)


class SentenceSplitter:
    """Feed streamed tokens; get back speakable sentences as early as possible."""

    def __init__(self):
        self.buf = ""
        self.emitted = 0

    def feed(self, text: str) -> list[str]:
        self.buf += text
        out = []
        while True:
            m = re.search(r"[.!?।](?=[\s\"')\]]|$)|\n", self.buf)
            if m and m.end() < len(self.buf) or (m and self.buf.endswith("\n")):
                cut = m.end()
                piece = self.buf[:cut]
                if _ABBREV.search(piece.strip()) and cut < len(self.buf):
                    # "Dr." — look for the next terminator instead
                    nxt = re.search(r"[.!?।](?=\s)|\n", self.buf[cut:])
                    if not nxt:
                        break
                    cut += nxt.end()
                    piece = self.buf[:cut]
                self.buf = self.buf[cut:]
                if piece.strip():
                    out.append(piece.strip())
                continue
            # First sentence running long with no full stop: break at a comma so
            # speech starts sooner.
            if self.emitted == 0 and not out and len(self.buf) > 90:
                c = max(self.buf.rfind(", ", 30), self.buf.rfind("; ", 30), self.buf.rfind(": ", 30))
                if c > 0:
                    out.append(self.buf[:c + 1].strip())
                    self.buf = self.buf[c + 1:]
                    continue
            break
        self.emitted += len(out)
        return [s for s in out if re.search(r"\w", s)]

    def flush(self) -> list[str]:
        rest, self.buf = self.buf.strip(), ""
        return [rest] if rest and re.search(r"\w", rest) else []


def split_sentences(text: str) -> list[str]:
    sp = SentenceSplitter()
    return sp.feed(text + "\n") + sp.flush()


# ═════════════════════════════════════════════════════════════════════════════
#  Speaker — multi-channel speech queue
# ═════════════════════════════════════════════════════════════════════════════

def _norm_words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", devanagari_to_hinglish(text).lower())


class Channel:
    """The speech stream of one command's reply."""

    def __init__(self, speaker: "Speaker", lang: str | None):
        self.speaker = speaker
        self.lang = lang
        self.q: deque[str] = deque()
        self.closed = False
        self.muted = False
        self.spoke = False
        self.last_push = time.monotonic()

    def say(self, text: str):
        if self.muted:
            return
        text = strip_markdown(text)
        if text and re.search(r"\w", text):
            self.q.append(text)
            self.last_push = time.monotonic()
            self.speaker._wake()

    def close(self):
        self.closed = True
        self.speaker._wake()

    def mute(self):
        self.muted = True
        self.q.clear()
        self.speaker._wake()


class Speaker:
    """
    Plays sentences from many Channels without overlap:
      - urgent phrases (acks, greetings) go first, between sentences
      - sticks with the channel it is speaking until that reply is done or stalls
        for >1 s, then serves another command's finished sentences
      - the next sentence is synthesised while the current one plays
    """

    def __init__(self, on_state=None):
        self.channels: list[Channel] = []
        self.urgent: deque[tuple[str, str | None]] = deque()
        self.speaking = False
        self.last_end = 0.0
        self.recent: deque[tuple[list[str], float]] = deque(maxlen=16)
        self._interrupt = False
        self._evt = asyncio.Event()
        self._on_state = on_state or (lambda: None)
        self._player = get_player()

    # ── producers ──
    def channel(self, lang: str | None = None) -> Channel:
        ch = Channel(self, lang)
        self.channels.append(ch)
        return ch

    def say_now(self, text: str, lang: str | None = None):
        self.urgent.append((text, lang))
        self._wake()

    def stop_all(self):
        """Barge-in "stop": silence now and drop everything queued."""
        self.urgent.clear()
        for ch in self.channels:
            ch.mute()
        self._interrupt = True
        self._wake()

    @property
    def busy(self) -> bool:
        return self.speaking or bool(self.urgent) or any(c.q for c in self.channels)

    def is_echo(self, text: str, window: float = 6.0) -> bool:
        """
        Did the mic just hear Jarvis himself (speaker → mic bleed)? Echo comes back
        misheard ("Jarvis online" → "Jarvis on mices"), so besides word overlap we
        count long shared character runs against recent sentences (and pairs of
        consecutive sentences, since a mic window can straddle two).
        """
        import difflib
        words = _norm_words(text)
        if not words:
            return False
        heard, heard_set = " ".join(words), set(words)
        now = time.monotonic()
        recent = [w for w, t in self.recent if w and (self.speaking or now - t <= window)]
        candidates = [" ".join(w) for w in recent]
        candidates += [" ".join(recent[i] + recent[i + 1]) for i in range(len(recent) - 1)]
        for cand in candidates:
            if len(heard_set & set(cand.split())) / len(heard_set) >= 0.6:
                return True
            sm = difflib.SequenceMatcher(None, heard, cand, autojunk=False)
            shared = sum(blk.size for blk in sm.get_matching_blocks() if blk.size >= 3)
            if shared / len(heard) >= 0.6:
                return True
        return False

    def _wake(self):
        self._evt.set()

    # ── consumer ──
    def _gc(self):
        self.channels = [c for c in self.channels if not (c.muted or (c.closed and not c.q))]

    def _take(self, current: Channel | None, blocking_ok: bool):
        """Next (channel, text, lang) or None. Non-blocking."""
        if self.urgent:
            text, lang = self.urgent.popleft()
            return None, text, lang
        self._gc()
        if current is not None and current.q and not current.muted:
            return current, current.q.popleft(), current.lang
        if not blocking_ok:
            return None
        stalled = (current is None or current.muted or (current.closed and not current.q)
                   or current not in self.channels
                   or time.monotonic() - current.last_push > 1.0)
        if stalled:
            for ch in self.channels:
                if ch.q:
                    return ch, ch.q.popleft(), ch.lang
        return None

    async def run(self):
        current: Channel | None = None
        prefetch = None   # (channel, clip)
        while True:
            if prefetch is not None:
                ch, clip = prefetch
                prefetch = None
                if ch is not None and ch.muted:
                    clip.cancel()
                    continue
            else:
                item = self._take(current, True)
                if item is None:
                    if self.speaking:
                        self.speaking = False
                        self.last_end = time.monotonic()
                        self._on_state()
                    self._evt.clear()
                    try:
                        await asyncio.wait_for(self._evt.wait(), timeout=0.25)
                    except asyncio.TimeoutError:
                        pass
                    continue
                ch, text, lang = item
                clip = start_clip(text, lang)

            if ch is not None:
                current = ch
                ch.spoke = True
            if not self.speaking:
                self.speaking = True
                self._on_state()
            self._interrupt = False
            self.recent.append((_norm_words(clip.text), time.monotonic()))
            play = asyncio.create_task(self._player.play(clip, lambda: self._interrupt))
            while not play.done():
                if prefetch is None:
                    nxt = self._take(current, False)
                    if nxt is not None:
                        prefetch = (nxt[0], start_clip(nxt[1], nxt[2]))
                await asyncio.wait({play}, timeout=0.05)
            try:
                play.result()
            except Exception as e:
                logger.warning(f"[TTS] playback error: {e}")
            self.recent.append((_norm_words(clip.text), time.monotonic()))
            if self._interrupt and prefetch is not None:
                prefetch[1].cancel()
                prefetch = None

    async def wait_idle(self):
        while self.busy or any(not c.closed for c in self.channels):
            await asyncio.sleep(0.05)


# ═════════════════════════════════════════════════════════════════════════════
#  Simple public helpers (reminders, scripts)
# ═════════════════════════════════════════════════════════════════════════════

async def speak_text(text: str, lang: str | None = None):
    """Speak a complete text. All sentences synthesise in parallel, play in order."""
    if not text or not text.strip():
        return
    clips = [start_clip(s, lang) for s in split_sentences(text)]
    player = get_player()
    for clip in clips:
        await player.play(clip)


async def speak_stream(text_generator, lang: str | None = None):
    """Speak an async generator of text chunks, sentence by sentence, pipelined."""
    speaker = Speaker()
    runner = asyncio.create_task(speaker.run())
    ch = speaker.channel(lang)
    splitter = SentenceSplitter()
    try:
        async for chunk in text_generator:
            if chunk:
                for s in splitter.feed(chunk):
                    ch.say(s)
        for s in splitter.flush():
            ch.say(s)
        ch.close()
        await speaker.wait_idle()
    finally:
        runner.cancel()
