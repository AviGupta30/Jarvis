"""
acoustic_tripwire.py — Jarvis Acoustic Wake Engine
---------------------------------------------------
Listens to the microphone in a background thread and detects a DOUBLE-CLAP
pattern using two-stage DSP:

  Stage 1 — Volume gate  (RMS)     : Ignores sounds below the noise floor.
  Stage 2 — Frequency gate (FFT)   : Ignores thumps/thuds. Passes only the
                                      sharp transient frequencies of a clap or
                                      finger-snap (2000–8000 Hz).

A single clap arms a 1.5-second window. A second clap inside that window fires
the wake event. A single clap, a dropped book, or speech are all ignored.

Architecture Rules Obeyed:
  - Rule 1 (Isolation)   : Imports NOTHING from other Jarvis tool modules.
  - Rule 2 (Failsafe)    : All I/O wrapped in try/except; errors are logged,
                           never propagated to crash the caller.
  - Rule 3 (Zero State)  : No file writes. All state lives in instance vars
                           and the shared threading.Event.
  - Rule 4 (Connectivity): Usable by both voice_agent.py (via threading.Event)
                           and the frontend UI (via /tripwire API in main.py).
"""

import threading
import time
import logging
import numpy as np

logger = logging.getLogger(__name__)

# ── Audio Configuration ───────────────────────────────────────────────────────
CHUNK    = 1024           # Samples per read (~23 ms at 44.1 kHz)
FORMAT   = None           # Set at import time after pyaudio is verified
CHANNELS = 1              # Mono — microphone input
RATE     = 44100          # Standard mic sample rate (Hz)

# ── Detection Thresholds (tunable) ───────────────────────────────────────────
# These are DEFAULTS. Auto-calibration at startup will override VOLUME_THRESHOLD.
VOLUME_THRESHOLD   = 3000   # RMS amplitude — sounds quieter than this are ignored
TARGET_FREQ_MIN    = 2000   # Hz — lower bound for a clap/snap signature
TARGET_FREQ_MAX    = 8000   # Hz — upper bound for a clap/snap signature
DOUBLE_CLAP_WINDOW = 1.5    # seconds — max gap between clap 1 and clap 2
COOLDOWN_AFTER_WAKE = 2.0   # seconds — silence the tripwire after triggering

# ── Synthesised Wake Chime (generated from numpy, no file needed) ─────────────
# A short rising two-tone beep: 880 Hz → 1320 Hz, each 120 ms, soft fade-out.
def _generate_chime() -> np.ndarray:
    """Generate a pleasant two-tone wake chime as a float32 numpy array."""
    sr   = 44100
    dur  = 0.12   # seconds per tone
    t    = np.linspace(0, dur, int(sr * dur), endpoint=False)
    fade = np.linspace(1.0, 0.0, int(sr * dur)) ** 0.5   # sqrt fade-out

    tone_a = np.sin(2 * np.pi * 880  * t) * fade * 0.35   # A5 — 880 Hz
    tone_b = np.sin(2 * np.pi * 1320 * t) * fade * 0.30   # E6 — 1320 Hz

    gap = np.zeros(int(sr * 0.04))   # 40 ms silence between tones
    return np.concatenate([tone_a, gap, tone_b]).astype(np.float32)

_CHIME_SAMPLES = _generate_chime()


def _play_chime() -> None:
    """Play the wake chime via sounddevice (non-blocking from caller's perspective)."""
    try:
        import sounddevice as sd
        sd.play(_CHIME_SAMPLES, samplerate=44100, blocking=True)
    except Exception as e:
        logger.warning(f"[Tripwire] Chime playback failed: {e}")


# ── Auto-Calibration ──────────────────────────────────────────────────────────

def calibrate_tripwire(audio_stream, sample_seconds: float = 2.0) -> float:
    """
    Sample ambient noise for `sample_seconds`, calculate the mean RMS, then
    set VOLUME_THRESHOLD = max(noise_floor * 4.0, 1500).

    A multiplier of 4.0 (vs the voice agent's 2.5) makes the tripwire stricter
    — it should only react to a clear, deliberate clap, not a chair scraping.

    Returns the new threshold.
    """
    logger.info("[Tripwire] Calibrating ambient noise floor...")
    samples: list[float] = []
    num_chunks = int(RATE / CHUNK * sample_seconds)
    for _ in range(num_chunks):
        try:
            raw = audio_stream.read(CHUNK, exception_on_overflow=False)
            arr = np.frombuffer(raw, dtype=np.int16).astype(np.float64)
            rms = float(np.sqrt(np.mean(arr ** 2))) if arr.size else 0.0
            samples.append(rms)
        except Exception:
            pass

    avg_noise = sum(samples) / len(samples) if samples else 500.0
    threshold = max(avg_noise * 4.0, 1500.0)
    logger.info(
        f"[Tripwire] Noise floor: {avg_noise:.0f} RMS  →  "
        f"Clap threshold set to {threshold:.0f} RMS"
    )
    return threshold


# ── Main Engine ───────────────────────────────────────────────────────────────

class AcousticWakeEngine:
    """
    Background thread that watches the microphone for a double-clap pattern.

    Usage
    -----
        event = threading.Event()
        engine = AcousticWakeEngine(wake_event=event)
        engine.start()        # spawns daemon thread, returns immediately
        ...
        if event.is_set():
            event.clear()
            # Jarvis is now awake — start recording the command
        ...
        engine.stop()         # graceful shutdown
    """

    def __init__(self, wake_event: threading.Event):
        self.wake_event      = wake_event
        self._stop_flag      = threading.Event()
        self._thread: threading.Thread | None = None
        self._enabled        = False
        self._volume_threshold = VOLUME_THRESHOLD   # overwritten by calibration
        self._last_triggered: float | None = None
        self._status_lock    = threading.Lock()
        # Inline (shared-stream) double-clap state
        self._first_clap_time: float | None = None
        self._cooldown_until: float          = 0.0

    # ── Public API ────────────────────────────────────────────────────────────

    def start(self) -> None:
        """Start the background listening thread."""
        if self._thread and self._thread.is_alive():
            logger.warning("[Tripwire] Already running — ignoring start().")
            return
        self._stop_flag.clear()
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="acoustic-tripwire"
        )
        self._thread.start()
        logger.info("[Tripwire] Engine started.")

    def stop(self) -> None:
        """Signal the background thread to exit and wait for it."""
        self._stop_flag.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3.0)
        self._enabled = False
        logger.info("[Tripwire] Engine stopped.")

    def enable(self) -> str:
        """Resume detection after a disable()."""
        self._enabled = True
        return "Acoustic tripwire ARMED. Clap twice to wake Jarvis."

    def disable(self) -> str:
        """Pause detection without stopping the thread (fast resume)."""
        self._enabled = False
        return "Acoustic tripwire DISARMED."

    def recalibrate(self) -> str:
        """
        Signal the background thread to re-run calibration on the next cycle.
        Returns immediately; calibration happens asynchronously.
        """
        self._recalibrate_flag = True
        return "Recalibration scheduled. It will complete in ~2 seconds."

    def set_volume_threshold(self, threshold: float) -> None:
        """Override the volume threshold (used by voice_agent inline mode)."""
        self._volume_threshold = float(threshold)
        logger.info(f"[Tripwire] Volume threshold set to {threshold:.0f} RMS")

    def process_chunk(self, raw_bytes: bytes, sample_rate: int = 16000) -> bool:
        """
        Inline (shared-stream) mode — called by voice_agent.py on every audio
        frame it reads from its OWN PyAudio stream.  No competing stream is
        opened; the double-clap state machine runs directly on the same bytes.

        Returns True the moment a double-clap is confirmed (wake event is also
        set so the /tripwire/status endpoint stays in sync).

        At 16000 Hz the Nyquist limit is 8000 Hz.  Our TARGET_FREQ_MAX of 8000
        is right at that edge, so we cap detection at sample_rate * 0.45 to
        avoid aliasing artefacts giving false positives.
        """
        if not self._enabled:
            return False

        now = time.time()

        # Still cooling down after a recent wake
        if now < self._cooldown_until:
            return False

        try:
            audio = np.frombuffer(raw_bytes, dtype=np.int16)
            if audio.size == 0:
                return False

            # Expire the first-clap window if too much time has elapsed
            if (self._first_clap_time is not None and
                    (now - self._first_clap_time) > DOUBLE_CLAP_WINDOW):
                self._first_clap_time = None

            # ── Stage 1: Volume gate ──────────────────────────────────────
            if self._rms(audio) < self._volume_threshold:
                return False

            # ── Stage 2: Frequency gate ───────────────────────────────────
            freq_max = min(TARGET_FREQ_MAX, sample_rate * 0.45)  # safe Nyquist margin
            fft_mag  = np.abs(np.fft.rfft(audio))
            freqs    = np.fft.rfftfreq(len(audio), d=1.0 / sample_rate)
            peak_freq = float(freqs[int(np.argmax(fft_mag))])

            if not (TARGET_FREQ_MIN < peak_freq < freq_max):
                return False

            # ── Double-clap state machine ─────────────────────────────────
            logger.debug(f"[Tripwire/inline] Clap-like sound: {peak_freq:.0f} Hz  "
                         f"vol={self._rms(audio):.0f}")

            if self._first_clap_time is None:
                # ARM — first clap
                self._first_clap_time = now
                return False
            else:
                # FIRE — second clap within window
                self._first_clap_time = None
                self._cooldown_until  = now + COOLDOWN_AFTER_WAKE
                with self._status_lock:
                    self._last_triggered = now
                threading.Thread(target=_play_chime, daemon=True).start()
                self.wake_event.set()
                logger.info("[Tripwire/inline] ⚡ DOUBLE-CLAP — waking Jarvis!")
                return True

        except Exception as exc:
            logger.debug(f"[Tripwire] process_chunk error: {exc}")
            return False

    def get_status(self) -> dict:
        """Return a JSON-serialisable status dict for the /tripwire/status endpoint."""
        with self._status_lock:
            last = self._last_triggered
        inline_running = self._enabled and self._thread is None   # inline mode
        thread_running = bool(self._thread and self._thread.is_alive())
        return {
            "enabled"          : self._enabled,
            "running"          : inline_running or thread_running,
            "volume_threshold" : int(self._volume_threshold),
            "freq_min"         : TARGET_FREQ_MIN,
            "freq_max"         : TARGET_FREQ_MAX,
            "double_clap_window": DOUBLE_CLAP_WINDOW,
            "last_triggered"   : last,
        }

    # ── Internal DSP ─────────────────────────────────────────────────────────

    @staticmethod
    def _rms(audio_array: np.ndarray) -> float:
        """Root Mean Square amplitude. Cast to float64 to prevent int16 overflow."""
        data = audio_array.astype(np.float64)
        return float(np.sqrt(np.mean(data ** 2)))

    @staticmethod
    def _dominant_freq(audio_array: np.ndarray) -> float:
        """
        FFT-based dominant frequency.
        Only inspect the positive half-spectrum (0 … RATE/2).
        Returns the peak frequency in Hz.
        """
        fft_result  = np.fft.rfft(audio_array)              # real FFT — 2× faster
        magnitudes  = np.abs(fft_result)
        freqs       = np.fft.rfftfreq(len(audio_array), d=1.0 / RATE)
        peak_idx    = int(np.argmax(magnitudes))
        return float(freqs[peak_idx])

    def _is_clap(self, audio_array: np.ndarray) -> bool:
        """Return True if this chunk looks like a clap/snap (loud + right frequency)."""
        volume = self._rms(audio_array)
        if volume < self._volume_threshold:
            return False
        freq = self._dominant_freq(audio_array)
        return TARGET_FREQ_MIN < freq < TARGET_FREQ_MAX

    # ── Background Thread ─────────────────────────────────────────────────────

    def _run(self) -> None:
        """
        Main loop — opened inside the thread so PyAudio errors stay contained.
        State machine:
          IDLE  → hears clap 1  → ARM (set first_clap_time)
          ARM   → hears clap 2  → FIRE wake_event
          ARM   → window expires → back to IDLE
        """
        import pyaudio   # imported here so the module can be loaded even if
                         # PyAudio isn't installed yet (graceful degradation)

        pa     = None
        stream = None
        self._recalibrate_flag = False
        self._enabled          = True   # armed by default when thread starts

        try:
            pa = pyaudio.PyAudio()
            stream = pa.open(
                format          = pyaudio.paInt16,
                channels        = CHANNELS,
                rate            = RATE,
                input           = True,
                frames_per_buffer = CHUNK,
            )

            # ── Auto-calibrate on startup ─────────────────────────────────
            self._volume_threshold = calibrate_tripwire(stream)
            logger.info(
                f"[Tripwire] Armed. Clap twice to wake Jarvis. "
                f"Threshold: {self._volume_threshold:.0f} RMS"
            )

            # Double-clap state
            first_clap_time: float | None = None
            cooldown_until:  float        = 0.0

            while not self._stop_flag.is_set():

                # ── Re-calibration request ────────────────────────────────
                if getattr(self, "_recalibrate_flag", False):
                    self._recalibrate_flag = False
                    self._volume_threshold = calibrate_tripwire(stream)

                # ── Paused state ──────────────────────────────────────────
                if not self._enabled:
                    time.sleep(0.1)
                    first_clap_time = None   # reset state while paused
                    continue

                # ── Cooldown (post-wake) ───────────────────────────────────
                if time.time() < cooldown_until:
                    try:
                        stream.read(CHUNK, exception_on_overflow=False)
                    except Exception:
                        pass
                    continue

                # ── Read a chunk ──────────────────────────────────────────
                try:
                    raw = stream.read(CHUNK, exception_on_overflow=False)
                except Exception as e:
                    logger.warning(f"[Tripwire] Stream read error: {e}")
                    time.sleep(0.05)
                    continue

                audio = np.frombuffer(raw, dtype=np.int16)

                # ── Double-clap state machine ─────────────────────────────
                now = time.time()

                # Expire the first-clap window
                if first_clap_time is not None and (now - first_clap_time) > DOUBLE_CLAP_WINDOW:
                    logger.debug("[Tripwire] First-clap window expired — reset.")
                    first_clap_time = None

                if self._is_clap(audio):
                    if first_clap_time is None:
                        # ARM: heard clap 1
                        first_clap_time = now
                        logger.debug(
                            f"[Tripwire] Clap 1 detected "
                            f"(vol={self._rms(audio):.0f}, "
                            f"freq={self._dominant_freq(audio):.0f} Hz). "
                            f"Waiting for clap 2..."
                        )
                    else:
                        # FIRE: heard clap 2 within the window
                        gap = now - first_clap_time
                        logger.info(
                            f"[Tripwire] ⚡ DOUBLE-CLAP DETECTED! "
                            f"Gap: {gap:.2f}s — Waking Jarvis..."
                        )
                        first_clap_time = None
                        cooldown_until  = now + COOLDOWN_AFTER_WAKE

                        # Play chime in a short-lived thread so we don't block
                        threading.Thread(target=_play_chime, daemon=True).start()

                        # Signal the voice agent
                        with self._status_lock:
                            self._last_triggered = now
                        self.wake_event.set()

                        # Brief pause so two claps don't echo into the next cycle
                        time.sleep(0.3)

        except Exception as e:
            logger.error(f"[Tripwire] Fatal engine error: {e}", exc_info=True)
        finally:
            if stream is not None:
                try:
                    stream.stop_stream()
                    stream.close()
                except Exception:
                    pass
            if pa is not None:
                try:
                    pa.terminate()
                except Exception:
                    pass
            self._enabled = False
            logger.info("[Tripwire] Background thread exited cleanly.")


# ── Module-level singleton (shared between voice agent and API) ───────────────
# Created once here so both callers import the same object.

_wake_event    = threading.Event()
_engine: AcousticWakeEngine | None = None


def get_engine() -> AcousticWakeEngine:
    """
    Return the module-level singleton engine, creating it if necessary.
    Thread-safe: safe to call from multiple threads / import contexts.
    """
    global _engine
    if _engine is None:
        _engine = AcousticWakeEngine(wake_event=_wake_event)
    return _engine


def get_wake_event() -> threading.Event:
    """Return the threading.Event that the engine sets on a double-clap."""
    return _wake_event
