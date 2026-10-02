"""
voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)

    MicListener (thread)  owns the ONLY PyAudio stream and never pauses, not even
                          while Jarvis talks or thinks. Silero VAD per 32 ms frame cuts
                          utterances, with a 0.5 s pre-roll so the "Jar-" of "Jarvis"
                          is never clipped. Optional strict double-clap wake
                          (JARVIS_CLAP_WAKE=1) runs inline.
    utterance loop        STT (Groq turbo, local fallback) → echo filter → stop words
                          → wake word / follow-up window → dispatch.
    command tasks         one asyncio task per command, run CONCURRENTLY: say
                          "Jarvis, play music" and, while it works, "Jarvis, what's
                          the weather" — both run, replies are spoken one after another.
    Speaker               one voice, never overlapping, next sentence synthesised
                          while the current one plays (app/services/voice.py).

Talk to it: "Jarvis, <command>" (wake word anywhere in the sentence), or just
"Jarvis" and then the command. Without the wake word it only listens right after
it greeted you or asked you a question — random room noise can't start it.
"Jarvis, stop" / "Jarvis, bas" / "chup" silences it.
Speak English → English reply (British voice); speak Hindi → Hindi reply (Hindi voice).
"""

import asyncio
import difflib
import json
import os
import random
import re
import subprocess
import sys
import threading
import time
from collections import deque

import httpx
import numpy as np
import pyaudio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.core.config import settings  # noqa: E402
from app.services import voice  # noqa: E402
from app.services.context_classifier import detect_language  # noqa: E402

# ── Shared UI state file (read by jarvis_overlay.py) ────────────────────────
_UI_STATE_FILE = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'jarvis_ui_state.json')


def set_ui_state(state: str):
    """Write Jarvis UI state so the overlay can animate accordingly."""
    try:
        with open(_UI_STATE_FILE, 'w') as f:
            json.dump({'state': state, 'ts': time.time()}, f)
    except Exception:
        pass


# ── Audio / VAD tuning ───────────────────────────────────────────────────────
RATE = 16000
CHUNK = 512                               # 32 ms — Silero's native frame size
FRAME_S = CHUNK / RATE
PREROLL_S = 0.5                           # audio kept from before speech onset
END_SILENCE_S = float(os.getenv("JARVIS_END_SILENCE_MS", "700")) / 1000
MIN_SPEECH_S = 0.25                       # shorter = cough / click
MAX_UTTERANCE_S = 20.0
MAX_WHILE_SPEAKING_S = 2.5                # rolling windows while Jarvis talks → fast barge-in
VAD_START, VAD_END = 0.5, 0.35            # hysteresis on Silero speech probability

FOLLOWUP_GREET_S = 8.0                    # after "Yes, sir?": the command, no wake word needed
FOLLOWUP_QUESTION_S = 10.0                # after Jarvis asked a question: the answer
MAX_PARALLEL = 4
CLAP_WAKE = os.getenv("JARVIS_CLAP_WAKE", "0") == "1"   # off by default: noise woke Jarvis up

# Speech without a wake word must be clearly speech, clearly worded and loud enough
# (room noise / TV / distant voices otherwise became commands).
NO_WAKE_MIN_LOGPROB = -0.8
NO_WAKE_MAX_NO_SPEECH = 0.4
LEVEL_OVER_NOISE = 4.0                    # speech level vs ambient noise floor
LEVEL_MIN = 60.0


# ═════════════════════════════════════════════════════════════════════════════
#  Wake word / stop words
# ═════════════════════════════════════════════════════════════════════════════

WAKE_WORDS = ["jarvis", "jarvish", "jarwis", "jaarvis", "jarbis", "jarvas", "jarves",
              "jervis", "javis", "jarvice", "jarviz"]
_WAKE_PREFIX = {"hey", "ok", "okay", "hi", "hello", "yo", "aye", "arre", "are", "suno", "oye", "listen"}
_WAKE_DEV = ("जार्विस", "जारविस", "जार्वीस", "जरविस")


def _is_wake_token(word: str) -> bool:
    w = re.sub(r"[^a-z]", "", word.lower())
    if w.endswith("s") and w[:-1] in WAKE_WORDS:     # "Jarvis's"
        w = w[:-1]
    if len(w) < 5 or len(w) > 9:
        return False
    if w in WAKE_WORDS:
        return True
    # Fuzzy only for j-words: "Travis", "harvest", "service" must never wake Jarvis
    return w[0] == "j" and difflib.SequenceMatcher(None, w, "jarvis").ratio() >= 0.8


def extract_wake_word_command(text: str) -> str | None:
    """
    None if no wake word; otherwise the command with the wake word (and a
    leading "hey"/"ok") removed. Wake word may be anywhere: "open Chrome, Jarvis".
    Returns "" when the user only said the wake word.
    """
    for dev in _WAKE_DEV:
        text = text.replace(dev, "Jarvis")
    words = text.split()
    for i, word in enumerate(words):
        if _is_wake_token(word):
            before = words[:i]
            if before and re.sub(r"[^a-z]", "", before[-1].lower()) in _WAKE_PREFIX:
                before = before[:-1]
            after = " ".join(words[i + 1:])
            # Words after the wake word are the command; words before only count when
            # nothing follows ("open Chrome, Jarvis") — otherwise they're usually noise
            # or Jarvis's own voice bleeding into the mic.
            rest = after if re.search(r"\w", after) else " ".join(before)
            return re.sub(r"^[\s,!?.।:;-]+|[\s,;:-]+$", "", rest).strip()
    return None


_STOP_RE = re.compile(
    r"^(please\s+)?(stop( it| talking| now)?|ruko|ruk ja(o)?|bas( karo| kar| itna hi)?|chup( ho ja(o)?| raho| karo)?|"
    r"cancel( it)?|shut up|(be )?quiet|enough|that'?s enough|khamosh|silence|never ?mind|rehne do|"
    r"band karo bolna|mute)(\s+(sir|please|yaar|jarvis))?[\s.!]*$",
    re.IGNORECASE,
)
_FILLERS = {"hmm", "hm", "uh", "um", "ah", "oh", "huh", "mm", "mhm", "uh huh", "ahem"}


def _is_stop(cmd: str) -> bool:
    return bool(_STOP_RE.match(cmd.strip(" ,.!?")))


# ═════════════════════════════════════════════════════════════════════════════
#  Microphone + VAD (thread)
# ═════════════════════════════════════════════════════════════════════════════

class _SileroStream:
    """Stateful frame-by-frame Silero VAD using the ONNX model bundled with faster-whisper."""

    def __init__(self):
        from faster_whisper.vad import get_vad_model
        self.session = get_vad_model().session
        self.reset()

    def reset(self):
        self.h = np.zeros((1, 1, 128), np.float32)
        self.c = np.zeros((1, 1, 128), np.float32)
        self.ctx = np.zeros(64, np.float32)

    def __call__(self, pcm: np.ndarray) -> float:
        f = pcm.astype(np.float32) / 32768.0
        out, self.h, self.c = self.session.run(
            None, {"input": np.concatenate([self.ctx, f])[None, :], "h": self.h, "c": self.c})
        self.ctx = f[-64:]
        return float(np.ravel(out)[0])


class _EnergyVAD:
    """Fallback if Silero can't load: adaptive noise floor."""

    def __init__(self):
        self.floor = 300.0

    def reset(self):
        pass

    def __call__(self, pcm: np.ndarray) -> float:
        rms = float(np.sqrt(np.mean(pcm.astype(np.float32) ** 2)))
        if rms < self.floor * 2:
            self.floor = 0.97 * self.floor + 0.03 * max(rms, 50.0)
        return 1.0 if rms > self.floor * 2.5 else 0.0


class _ClapDetector:
    """
    Strict double clap. The old tripwire fired on ANY two loud 2–8 kHz frames within
    1.5 s — keyboard, door, dishes — and woke Jarvis on its own. Now a clap must be:
    a sudden onset (≥6× the previous frame), well above the room's noise, not speech,
    mostly high-frequency energy, decaying within ~100 ms; exactly two of them
    0.15–0.9 s apart, with quiet before the first and after the second.
    """

    def __init__(self):
        self.t = 0.0
        self.noise = None
        self.prev_rms = 0.0
        self.candidate = None          # (peak_rms, t, frames_since)
        self.impulses: deque = deque(maxlen=8)
        self.loud: deque = deque(maxlen=64)   # times of other loud frames
        self.cooldown_until = 0.0

    @staticmethod
    def _hf_ratio(pcm: np.ndarray) -> float:
        spec = np.abs(np.fft.rfft(pcm.astype(np.float32))) ** 2
        freqs = np.fft.rfftfreq(len(pcm), 1.0 / RATE)
        total = float(spec.sum()) or 1.0
        return float(spec[freqs >= 2000].sum()) / total

    def feed(self, pcm: np.ndarray, vad_p: float) -> bool:
        self.t += FRAME_S
        rms = float(np.sqrt(np.mean(pcm.astype(np.float32) ** 2)))
        if self.noise is None:
            self.noise = rms
        if rms < self.noise * 3:
            self.noise = 0.995 * self.noise + 0.005 * rms
        thr = max(self.noise * 30.0, 3000.0)

        if self.candidate is not None:
            peak, t0, n = self.candidate
            if rms < 0.25 * peak:
                self.impulses.append(t0)
                self.candidate = None
            elif n >= 3:                              # sustained: not a clap
                self.candidate = None
                self.loud.append(self.t)
            else:
                self.candidate = (max(peak, rms), t0, n + 1)
        elif (rms >= thr and rms >= 6.0 * max(self.prev_rms, 1.0) and vad_p < 0.3
              and self._hf_ratio(pcm) >= 0.4):
            self.candidate = (rms, self.t, 0)
        elif rms >= thr * 0.3:
            self.loud.append(self.t)
        self.prev_rms = rms

        if not self.impulses or self.candidate is not None or self.t - self.impulses[-1] < 0.5:
            return False
        imps = list(self.impulses)
        self.impulses.clear()
        if self.t < self.cooldown_until or len(imps) != 2:
            return False
        a, b = imps
        if not 0.15 <= b - a <= 0.9:
            return False
        if any(a - 0.6 <= x <= a - 0.05 or b + 0.2 <= x <= b + 0.5 for x in self.loud):
            return False
        self.cooldown_until = self.t + 3.0
        return True


class MicListener(threading.Thread):
    def __init__(self, loop: asyncio.AbstractEventLoop, events: asyncio.Queue, speaking_flag,
                 clap_wake: bool = False, output_level=lambda: 0.0):
        super().__init__(daemon=True, name="jarvis-mic")
        self.loop, self.events = loop, events
        self.speaking_flag = speaking_flag          # callable → bool (is Jarvis talking?)
        self.clap = _ClapDetector() if clap_wake else None
        self.in_speech = False
        self.running = True
        self.noise_floor = 50.0                     # RMS of non-speech frames (EMA)
        # Double-talk detection: while Jarvis talks, mic RMS ≈ echo_gain × output RMS.
        # Frames well above that are the user talking over Jarvis.
        self.output_level = output_level
        self.echo_ratios: deque = deque(maxlen=400)
        self.user_frames = 0
        try:
            self.vad = _SileroStream()
            print("🎚️  Silero VAD active.")
        except Exception as e:
            print(f"[VAD] Silero unavailable ({e}) — using energy VAD.")
            self.vad = _EnergyVAD()

    def _emit(self, *event):
        self.loop.call_soon_threadsafe(self.events.put_nowait, event)

    def _open(self, pa):
        return pa.open(rate=RATE, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=CHUNK)

    def _calibrate(self, stream):
        """Initial ambient noise floor (kept up to date on every non-speech frame)."""
        levels = []
        for _ in range(int(1.0 / FRAME_S)):
            pcm = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), np.int16)
            levels.append(float(np.sqrt(np.mean(pcm.astype(np.float32) ** 2))))
        self.noise_floor = max(float(np.median(levels)) if levels else 50.0, 1.0)
        print(f"🎤 Ambient noise level {self.noise_floor:.0f} RMS."
              + ("  👏 Strict double-clap wake ON." if self.clap else ""))

    def _reset_segmenter(self):
        self.preroll: deque = deque(maxlen=int(PREROLL_S / FRAME_S))
        self.frames: list = []
        self.voiced = self.silence = self.speech_frames = 0
        self.start_t = 0.0

    def _process(self, data: bytes):
        """One 32 ms frame → clap check + VAD state machine → events."""
        pcm = np.frombuffer(data, np.int16)
        try:
            p = self.vad(pcm)
        except Exception:
            p = 0.0
        rms = float(np.sqrt(np.mean(pcm.astype(np.float32) ** 2)))
        speaking = self.speaking_flag()
        if p < 0.2 and not speaking:
            self.noise_floor = 0.98 * self.noise_floor + 0.02 * max(rms, 1.0)
        user_frame = self._is_user_frame(rms, p, speaking)
        if self.clap is not None and not self.speaking_flag():
            try:
                if self.clap.feed(pcm, p):
                    self._emit("clap")
            except Exception:
                pass

        if not self.in_speech:
            self.preroll.append(pcm)
            self.voiced = self.voiced + 1 if p >= VAD_START else 0
            self._pre_user = (getattr(self, "_pre_user", 0) + 1) if user_frame else 0
            if self.voiced >= 2:
                self.in_speech = True
                self.frames = list(self.preroll)
                self.user_frames = min(self._pre_user, len(self.frames))
                self.speech_frames, self.silence = self.voiced, 0
                self.start_t = time.monotonic() - len(self.frames) * FRAME_S
                self._emit("speech_start", self.start_t)
            return

        self.frames.append(pcm)
        if user_frame:
            self.user_frames += 1
        if p >= VAD_END:
            self.silence = 0
            self.speech_frames += 1
        else:
            self.silence += 1

        dur = len(self.frames) * FRAME_S
        limit = MAX_WHILE_SPEAKING_S if self.speaking_flag() else MAX_UTTERANCE_S
        ended = self.silence * FRAME_S >= END_SILENCE_S
        if not (ended or dur >= limit):
            return
        if self.speech_frames * FRAME_S >= MIN_SPEECH_S:
            audio = np.concatenate(self.frames)
            rms = [float(np.sqrt(np.mean(f.astype(np.float32) ** 2))) for f in self.frames]
            level = float(np.percentile(rms, 80))
            share = self.user_frames / max(len(self.frames), 1)
            self._emit("utterance", audio, self.start_t, ended, level, self.noise_floor, share)
        if ended:
            self.in_speech = False
            self.voiced = 0
            self.preroll.clear()
            self._emit("speech_end")
        else:
            # Window cut mid-speech (long talk / Jarvis speaking): keep the last
            # 0.5 s as overlap so a word on the boundary isn't lost.
            self.frames = self.frames[-self.preroll.maxlen:]
            self.speech_frames = self.silence = self.user_frames = 0
            self.start_t = time.monotonic() - len(self.frames) * FRAME_S

    def _is_user_frame(self, rms: float, vad_p: float, speaking: bool) -> bool:
        if not speaking:
            return vad_p >= VAD_END
        out = self.output_level()
        if out >= 30.0:
            # Learn the speaker→mic echo gain from EVERY frame while Jarvis plays (the
            # echo is there whether or not the VAD fires). A low percentile keeps the
            # estimate honest even if the user talks early.
            self.echo_ratios.append(rms / out)
        if vad_p < VAD_END:
            return False
        if out < 30.0:                      # Jarvis between words: anything voiced is the user
            return rms > self.noise_floor * 6
        if len(self.echo_ratios) < 25:      # echo path not learned yet — be conservative
            return False
        echo_gain = float(np.percentile(self.echo_ratios, 30))
        return rms > max(echo_gain * out * 4.0, self.noise_floor * 6)

    def run(self):
        pa = pyaudio.PyAudio()
        stream = None
        self._reset_segmenter()
        while self.running:
            try:
                if stream is None:
                    stream = self._open(pa)
                    self._calibrate(stream)
                data = stream.read(CHUNK, exception_on_overflow=False)
            except Exception as e:
                print(f"[Mic] {e} — reopening in 1 s")
                try:
                    stream and stream.close()
                except Exception:
                    pass
                stream = None
                time.sleep(1.0)
                continue
            self._process(data)
        try:
            stream and stream.close()
        finally:
            pa.terminate()


# ═════════════════════════════════════════════════════════════════════════════
#  Backend streaming → speech
# ═════════════════════════════════════════════════════════════════════════════

_AGENTIC_TAGS = ("[STEP", "[PLAN]", "[DONE]", "[REPLAN]", "[SUMMARY]", "[RESULT]")


def _clean_agentic_line(text: str) -> str:
    """Convert a linear-planner tag line into natural spoken text."""
    text = re.sub(r'^\[STEP (\d+) ✓\]\s*', r'Step \1 done. ', text)
    text = re.sub(r'^\[STEP (\d+) ✗\]\s*', r'Step \1 hit a problem. ', text)
    text = re.sub(r'^\[STEP (\d+)[^\]]*\]\s*', r'Step \1. ', text)
    for tag, rep in (("[PLAN]", ""), ("[DONE]", "All done."), ("[REPLAN]", "Adjusting the plan."),
                     ("[SUMMARY]", ""), ("[RESULT]", "")):
        text = text.replace(tag, rep)
    return text.strip()


def _speakable(sentence: str) -> str:
    s = sentence.strip()
    if s.startswith(_AGENTIC_TAGS):
        s = _clean_agentic_line(s)
    return s


async def stream_chat(http: httpx.AsyncClient, command: str, ch: "voice.Channel") -> str:
    """
    POST /chat with the spoken language, speak the reply into `ch` as it streams.
    LLM replies come back in the user's language; canned English lines from tool
    flows are translated (in order) before they are spoken. Returns the full reply.
    """
    splitter = voice.SentenceSplitter()
    full: list[str] = []
    mode = None
    sse_buf = ""
    target = ch.lang or "en"
    ordered: asyncio.Queue = asyncio.Queue()     # str or Task[str], in reply order

    async def pusher():
        while True:
            item = await ordered.get()
            if item is None:
                return
            text = await item if isinstance(item, asyncio.Task) else item
            if text:
                ch.say(text)

    push_task = asyncio.create_task(pusher())

    def say_text(t: str, flush: bool = False):
        for s in splitter.feed(t) + (splitter.flush() if flush else []):
            s = _speakable(s)
            if not s:
                continue
            if _BACKEND_FAIL_RE.search(s):
                if not getattr(say_text, "failed", False):
                    say_text.failed = True
                    ordered.put_nowait(_pick("quota", target))
                continue
            if voice.language_mismatch(s, target):
                ordered.put_nowait(asyncio.create_task(voice.translate_for_speech(s, target)))
            else:
                ordered.put_nowait(s)

    def on_event(raw: str):
        raw = raw.strip()
        if not raw.startswith("data:"):
            return
        try:
            evt = json.loads(raw[5:].strip())
        except Exception:
            return
        kind, text = evt.get("type"), (evt.get("text") or "").strip()
        # Speak what a person would say; skip per-node bookkeeping.
        if kind in ("narration", "aggregate", "error", "fallback") and text:
            full.append(text)
            say_text(text + "\n", flush=True)

    body = {"prompt": command, "lang": target, "voice": True}
    try:
        async with http.stream("POST", f"{settings.JARVIS_API_URL}/chat", json=body) as resp:
            if resp.status_code != 200:
                raise RuntimeError(f"backend HTTP {resp.status_code}")
            async for chunk in resp.aiter_text():
                if not chunk:
                    continue
                if mode is None:
                    mode = "sse" if chunk.lstrip().startswith("data:") else "text"
                if mode == "sse":
                    sse_buf += chunk
                    while "\n\n" in sse_buf:
                        event, sse_buf = sse_buf.split("\n\n", 1)
                        on_event(event)
                else:
                    full.append(chunk)
                    say_text(chunk)
        if mode == "sse" and sse_buf:
            on_event(sse_buf)
        say_text("", flush=True)
    finally:
        ordered.put_nowait(None)
        await push_task
    return "".join(full) if mode != "sse" else " ".join(full)


# ═════════════════════════════════════════════════════════════════════════════
#  Agent
# ═════════════════════════════════════════════════════════════════════════════

PHRASES = {
    "greet": {
        "en": ["Yes, sir?", "At your service, sir.", "I'm listening, sir.", "Go ahead, sir."],
        "hi": ["Haan sir, boliye?", "Ji sir, bataiye.", "Boliye sir, sun raha hoon."],
    },
    "ack": {
        "en": ["On it, sir.", "Right away, sir.", "Working on it.", "One moment, sir."],
        "hi": ["Ji sir, abhi karta hoon.", "Haan sir, ek second.", "Kar raha hoon, sir."],
    },
    "busy": {
        "en": ["I'm already juggling several tasks, sir. Give me a moment."],
        "hi": ["Sir, abhi kaafi kaam chal raha hai, ek pal dijiye."],
    },
    "offline": {
        "en": ["I can't reach my core systems, sir. Is the Jarvis server running?"],
        "hi": ["Sir, main server se connect nahi ho pa raha. Kya Jarvis server chal raha hai?"],
    },
    "error": {
        "en": ["Sorry sir, something went wrong with that one."],
        "hi": ["Sorry sir, isme kuch gadbad ho gayi."],
    },
    "quota": {
        "en": ["I've hit my AI usage limit for the moment, sir. Give me a minute and ask again."],
        "hi": ["Sir, abhi meri AI limit poori ho gayi hai. Ek minute baad phir se boliye."],
    },
}

# Backend's generic failure line (llm._groq_generate) → an honest, localized sentence
_BACKEND_FAIL_RE = re.compile(r"issue connecting to my brain|please try again in a moment", re.IGNORECASE)


def _pick(kind: str, lang: str) -> str:
    return random.choice(PHRASES[kind]["hi" if lang == "hi" else "en"])


class VoiceAgent:
    def __init__(self):
        self.speaker: voice.Speaker | None = None
        self.mic: MicListener | None = None
        self.events: asyncio.Queue | None = None
        self.http: httpx.AsyncClient | None = None
        self.tasks: set[asyncio.Task] = set()
        self.task_started: dict[asyncio.Task, float] = {}
        self.followup_until = 0.0
        self._followup_pending: float | None = None   # window length to open when speech ends
        self._speak_spans: deque = deque(maxlen=50)    # (start, end) of Jarvis talking
        self._speak_start = None
        self._last_ui = None
        self._pending_greet: asyncio.Task | None = None
        self._last_lang = "en"

    # ── speaker state → follow-up window ──
    def _on_speaker_state(self):
        now = time.monotonic()
        if self.speaker.speaking:
            self._speak_start = now
        else:
            if self._speak_start is not None:
                self._speak_spans.append((self._speak_start, now))
            self._speak_start = None
            if self._followup_pending:
                self.followup_until = now + self._followup_pending
                self._followup_pending = None

    def _open_followup(self, seconds: float):
        if self.speaker.busy:
            self._followup_pending = max(seconds, self._followup_pending or 0)
        else:
            self.followup_until = time.monotonic() + seconds

    def _overlaps_speech(self, t0: float, t1: float) -> bool:
        """Was Jarvis talking (or just finished) during [t0, t1]?"""
        if self.speaker.speaking and (self._speak_start or 0) <= t1:
            return True
        return any(s <= t1 and t0 <= e + 0.35 for s, e in self._speak_spans)

    # ── UI ──
    async def _ui_loop(self):
        while True:
            now = time.monotonic()
            if self.speaker.speaking:
                s = "speaking"
            elif self.mic and self.mic.in_speech:
                s = "listening"
            elif self.tasks:
                s = "working" if any(now - t > 4 for t in self.task_started.values()) else "processing"
            elif now < self.followup_until:
                s = "listening"
            else:
                s = "idle"
            if s != self._last_ui:
                set_ui_state(s)
                self._last_ui = s
            await asyncio.sleep(0.15)

    # ── commands ──
    def dispatch(self, command: str, lang: str):
        if len(self.tasks) >= MAX_PARALLEL:
            self.speaker.say_now(_pick("busy", lang), lang)
            return
        acked = bool(self.tasks)
        if acked:
            # Something is already running — acknowledge instantly so the user knows
            # the second command was heard and is running in parallel.
            self.speaker.say_now(_pick("ack", lang), lang)
        task = asyncio.create_task(self._run_command(command, lang, acked))
        self.tasks.add(task)
        self.task_started[task] = time.monotonic()

        def _done(t):
            self.tasks.discard(t)
            self.task_started.pop(t, None)
        task.add_done_callback(_done)

    async def _run_command(self, command: str, lang: str, acked: bool = False):
        ch = self.speaker.channel(lang)
        t0 = time.monotonic()

        async def filler():
            # Nothing to say after 1.8 s? Acknowledge once, like a person would.
            if acked:
                return
            await asyncio.sleep(1.8)
            if not ch.spoke and not ch.q and not ch.closed and not ch.muted:
                ch.say(_pick("ack", lang))
        filler_task = asyncio.create_task(filler())
        reply = ""
        try:
            reply = await stream_chat(self.http, command, ch)
            print(f"🤖 [{time.monotonic() - t0:.1f}s] {reply.strip()[:200]}")
        except httpx.ConnectError:
            print("[Backend] not reachable")
            ch.say(_pick("offline", lang))
        except Exception as e:
            print(f"[Backend error] {type(e).__name__}: {e}")
            ch.say(_pick("error", lang))
        finally:
            filler_task.cancel()
            ch.close()
        # Listen without the wake word ONLY if Jarvis asked something. (It used to open a
        # window after every reply, so TV / room talk became new commands → it kept talking.)
        if not ch.muted and re.search(r"[?？]\s*[\"')\]]?\s*$", reply.strip()):
            self._open_followup(FOLLOWUP_QUESTION_S)

    # ── utterances ──
    async def _greet_after_pause(self, lang: str):
        # User said just "Jarvis" — if they keep talking, don't talk over them.
        await asyncio.sleep(0.6)
        if not (self.mic and self.mic.in_speech):
            self.speaker.say_now(_pick("greet", lang), lang)
        self.followup_until = time.monotonic() + FOLLOWUP_GREET_S + 2

    async def handle_utterance(self, pcm: np.ndarray, start_t: float, complete: bool = True,
                               level: float = 1e9, noise: float = 0.0, user_share: float = 1.0):
        end_t = time.monotonic()
        overlapped = self._overlaps_speech(start_t, end_t)
        if overlapped and user_share < 0.12:
            return          # only Jarvis's own voice in the mic — nothing to transcribe
        # Follow-up window: after a reply it only opens once Jarvis is silent; after
        # a greeting it is open at once. Echo of Jarvis himself is filtered below.
        in_followup = start_t <= self.followup_until
        # Quota: speech that is probably not for us (Jarvis's own echo, idle-room
        # chatter when Groq quota is low) goes through local Whisper first.
        # Quota saver: idle-room speech goes to local Whisper first only when Groq
        # quota runs low. The user talking over Jarvis (double-talk detected) gets
        # the accurate Groq model — tiny Whisper garbled Hindi barge-ins.
        prefer_local = not in_followup and voice.groq_quota_low()
        tr = await voice.transcribe_pcm(pcm, prefer_local=prefer_local)
        text = tr.text.strip()
        if not text:
            return
        command = extract_wake_word_command(text)

        if overlapped and command is not None and not _is_stop(command) and self.speaker.is_echo(text):
            print(f"   (echo ignored: '{text}')")
            return
        if (prefer_local and command is not None and not _is_stop(command)
                and voice.groq_stt_available()):
            better = await voice.transcribe_pcm(pcm)      # wake word found — get the accurate version
            better_cmd = extract_wake_word_command(better.text) if better.text else None
            if better_cmd is not None:                    # keep local's result if Groq lost the wake word
                tr, text, command = better, better.text.strip(), better_cmd

        tag = f"{tr.source}/{tr.lang} lp={tr.logprob:.2f} ns={tr.no_speech:.2f} lvl={level:.0f}/{noise:.0f}"
        loud_enough = level >= max(noise * LEVEL_OVER_NOISE, LEVEL_MIN)
        sure = tr.confident(NO_WAKE_MIN_LOGPROB, NO_WAKE_MAX_NO_SPEECH)
        if command is not None and _is_stop(command):
            if not (self.speaker.speaking or self.speaker.busy):
                # Jarvis is silent, so "stop" / "stop it" / "mute" is about the music/video
                print(f"⏸️  Stop → media pause.  ('{text}')")
                self.followup_until = 0
                self.dispatch("stop the music", self._last_lang)
                return
            print(f"🤫 Stop.  ('{text}')")
            self.speaker.stop_all()
            self.followup_until = 0
            self._followup_pending = None
            return
        if overlapped and self.speaker.is_echo(command if command else text):
            print(f"   (echo ignored: '{text}')")
            return
        if command is None:
            if not in_followup:
                print(f"   [no wake word] '{text}'  ({tag})")
                return
            # No wake word to vouch for it: must be clear, confident, near-field speech.
            if not (sure and loud_enough) or len(re.findall(r"\w{2,}", text)) == 0:
                print(f"   [ignored: unclear/quiet] '{text}'  ({tag})")
                return
            command = text
            if command.lower().strip(" .!?") in _FILLERS:
                return
            if self.speaker.is_echo(command):
                return
        elif not command and not (sure and loud_enough):
            # A bare "Jarvis" from noise (Whisper hallucination / distant sound) — ignore.
            print(f"   [ignored: weak wake] '{text}'  ({tag})")
            return
        print(f"\n🗣️  '{text}'  ({tag})")

        # Reply language = spoken language. Whisper's audio language ID decides; romanized
        # Hindi that Whisper labelled English is caught by the word check.
        lang = "hi" if tr.lang == "hi" or detect_language(command or text) in ("hindi", "hinglish") else "en"
        self._last_lang = lang

        if _is_stop(command):              # plain "stop" in the follow-up window
            if not (self.speaker.speaking or self.speaker.busy):
                print("⏸️  Stop → media pause.")
                self.followup_until = 0
                self.dispatch("stop the music", lang)
                return
            print("🤫 Stop.")
            self.speaker.stop_all()
            self.followup_until = 0
            self._followup_pending = None
            return
        if not command:
            if self._pending_greet and not self._pending_greet.done():
                return
            self._pending_greet = asyncio.create_task(self._greet_after_pause(lang))
            return
        if self._pending_greet and not self._pending_greet.done():
            self._pending_greet.cancel()   # they kept talking — no greeting needed

        self.followup_until = 0          # this utterance consumed the follow-up window
        print(f"🧠 → /chat: {command}")
        self.dispatch(command, lang)

    async def on_clap(self):
        print("\n👏 Double clap — awake.")
        self.speaker.say_now(_pick("greet", self._last_lang), self._last_lang)
        self.followup_until = time.monotonic() + FOLLOWUP_GREET_S + 2

    # ── main ──
    async def run(self):
        loop = asyncio.get_running_loop()
        self.events = asyncio.Queue()
        self.speaker = voice.Speaker(on_state=self._on_speaker_state)
        speaker_task = asyncio.create_task(self.speaker.run())

        voice.preload_local_stt()
        prewarm = [p for kind in ("greet", "ack") for lang in ("en", "hi") for p in PHRASES[kind][lang]]
        asyncio.create_task(voice.prewarm(prewarm))

        self.mic = MicListener(loop, self.events, lambda: self.speaker.speaking, CLAP_WAKE,
                               voice.get_player().output_level)
        self.mic.start()
        ui_task = asyncio.create_task(self._ui_loop())

        timeout = httpx.Timeout(300.0, connect=5.0)
        async with httpx.AsyncClient(timeout=timeout) as self.http:
            print("🤖 Jarvis is online. Say 'Jarvis …'" + (" or clap twice" if CLAP_WAKE else "")
                  + ". (Ctrl+C to exit)")
            self.speaker.say_now("Online and ready, sir.", "en")   # never say "Jarvis": it would wake itself
            stt_jobs: set[asyncio.Task] = set()
            try:
                while True:
                    event = await self.events.get()
                    kind = event[0]
                    if kind == "utterance":
                        # Transcribe concurrently so a slow STT call never blocks the next utterance
                        job = asyncio.create_task(self._safe_utterance(*event[1:]))
                        stt_jobs.add(job)
                        job.add_done_callback(stt_jobs.discard)
                    elif kind == "clap":
                        await self.on_clap()
            finally:
                self.mic.running = False
                for t in list(self.tasks) + list(stt_jobs) + [ui_task, speaker_task]:
                    t.cancel()

    async def _safe_utterance(self, pcm, start_t, complete, level=1e9, noise=0.0, user_share=1.0):
        try:
            await self.handle_utterance(pcm, start_t, complete, level, noise, user_share)
        except Exception as e:
            print(f"[Utterance error] {type(e).__name__}: {e}")


async def run_voice_agent():
    await VoiceAgent().run()


def _launch_overlay():
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')
            if cmdline and 'jarvis_overlay.py' in ' '.join(cmdline):
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, TypeError):
            pass
    path = os.path.join(os.path.dirname(__file__), 'jarvis_overlay.py')
    if not os.path.exists(path):
        return None
    try:
        proc = subprocess.Popen(
            [sys.executable, path],
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        )
        print("🎨 Jarvis overlay started.")
        return proc
    except Exception as e:
        print(f"[Overlay] Could not start: {e}")
        return None


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    overlay = _launch_overlay()
    set_ui_state('idle')
    try:
        asyncio.run(run_voice_agent())
    except KeyboardInterrupt:
        print("\nStopping Jarvis voice agent...")
    finally:
        set_ui_state('idle')
        if overlay:
            overlay.terminate()
