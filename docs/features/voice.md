# Voice: STT, TTS, wake word, clap wake, overlay

## Purpose
Hands-free JARVIS: a separate process (`scripts/voice_agent.py`) that listens all the time, talks to the same `/chat` backend, answers in the language you spoke (English → British English voice, Hindi/Hinglish → Hindi voice) and can run several commands at once. It must never start talking on its own.

## Flow (`scripts/voice_agent.py`)
- **MicListener thread** owns the only PyAudio stream (16 kHz, 512-sample / 32 ms frames) and never pauses. Per frame: Silero VAD (`_SileroStream`, the ONNX model bundled with faster-whisper, run statefully) → noise-floor tracking → double-talk check (`_is_user_frame`) → optional strict clap check (`_ClapDetector`, only with `JARVIS_CLAP_WAKE=1`) → segmenter. The segmenter starts after 2 voiced frames with 0.5 s pre-roll and ends after `JARVIS_END_SILENCE_MS` (700) of silence, max 20 s; while Jarvis talks it cuts rolling 2.5 s windows. Each `utterance` event carries the audio, its 80th-percentile level, the noise floor and `user_share`.
- **Double-talk (Jarvis talking, user talks over him):** `voice._Player.output_level()` records what is being played. The mic thread learns the speaker→mic echo gain (30th percentile of mic/output RMS over every frame while playing). A voiced frame 4× above the expected echo counts as the user. Windows with `user_share < 0.12` are pure echo and are never transcribed; real barge-ins go to the accurate STT (tiny Whisper garbled Hindi).
- **handle_utterance**: STT (`voice.transcribe_pcm`) → stop words (`_is_stop`: stop/ruko/bas/chup/cancel…, act immediately) → echo filter (`Speaker.is_echo`) → wake word anywhere in the sentence (`extract_wake_word_command`; exact variants, fuzzy only for j-words so "Travis"/"harvest" don't count) **or** the follow-up window → `dispatch`.
- **Anti-false-trigger gates** (noise used to wake Jarvis and make it talk): no Whisper prompt (a "Jarvis" prompt made Whisper hear "Jarvis" in noise) · a bare "Jarvis" and every no-wake-word utterance must be confident (`Transcript.confident`: avg logprob ≥ -0.8, no_speech ≤ 0.4) and near-field (level ≥ 4× noise floor and ≥ 60 RMS) · the follow-up window opens only after a greeting ("Yes, sir?", 10 s) or when Jarvis's reply ends with a question (10 s), never after ordinary replies · clap wake is off by default · the backend's own tripwire no longer starts on boot.
- **Reply language = spoken language.** `lang` is "hi" if Whisper's audio language ID says Hindi (a Devanagari transcript that is mostly English loanwords counts as English, `loanword_ratio`) or `detect_language` says hindi/hinglish; else "en". It is sent as `{"prompt", "lang", "voice": true}`. The backend forces it (`llm._reply_language_note`, placed right before the user turn so history can't override it); voice Hindi replies come in Devanagari. Canned English lines from tool flows are translated per sentence (`voice.language_mismatch` → `translate_for_speech`, ~0.6 s, order kept). Backend "issue connecting to my brain" becomes a localized "AI usage limit" line.
- **dispatch** → one asyncio task per command (max 4), each with its own `Speaker` channel, streaming `/chat` (`stream_chat`): text is split by `SentenceSplitter`; DAG SSE events → only `narration`/`aggregate`/`error`/`fallback` spoken; `[STEP n]` lines cleaned. One ack per command: instant if another command is running, otherwise a filler after 1.8 s of silence.
- UI state for `scripts/jarvis_overlay.py` (idle/listening/processing/working/speaking) is recomputed every 150 ms (`_ui_loop`).

## STT (`voice.transcribe_pcm` → `Transcript`)
Groq `JARVIS_STT_MODEL` (`whisper-large-v3-turbo`, verbose_json, auto language; Urdu/other Indic → retry `hi`, other → retry `en`; segments filtered by no_speech_prob/avg_logprob, which also fill `Transcript.logprob/no_speech`) → Devanagari romanized (`devanagari_to_hinglish`, loanwords restored) → ALL-CAPS normalised. Fallback: local faster-whisper `JARVIS_STT_LOCAL` (`base`, 6 threads; Hindi forced to Devanagari with a Hindi initial prompt, else small models write Urdu script). Quota from `x-ratelimit-remaining-requests`; below 150 left, idle-room speech goes local first; 429 → 60 s local-only. `JARVIS_STT_MODE=local` disables Groq.

## TTS (`voice.Speaker`, `start_clip`, `_Player`)
The channel's language comes from the command, so a reply keeps one voice. English → edge-tts `JARVIS_VOICE_EN` (en-GB-RyanNeural, +4%); Hindi → `JARVIS_VOICE_HI` (hi-IN-MadhurNeural, +8%) with romanized Hindi words rewritten to Devanagari (`hinglish_to_devanagari`). MP3 decoded while streaming (PyAV) into a callback-driven 24 kHz `sounddevice` stream (200 ms prebuffer). The next sentence synthesises while the current plays; greetings/acks are pre-cached. edge-tts stall >4 s → one retry → Windows SAPI. `Speaker.stop_all()` cuts audio within ~20 ms.

## Backend pieces that matter for voice
- `ChatRequest.lang/voice` (chat.py) → `generate_chat_response(language=, voice=)` (llm.py).
- Voice requests skip the passive screen capture in chat.py step 5. It measured 44 s (vision model rate-limited + OCR) and ran synchronously, freezing every request; for UI requests it now runs in a thread capped at 3 s.
- `llm.pick_model` / `_track_limits`: each gpt-oss model has its own 8k tokens/min and 200k tokens/day bucket; calls go to the one with room, and a 429 parks that model until Groq's "try again in …" and fails over instantly (the SDK used to sleep ~30 s silently).

## Server-side tripwire
Off by default (`JARVIS_SERVER_TRIPWIRE=1` to start it with the server). It opened a second mic stream and chimed on keyboard/door noise. `/tripwire/{status,enable,disable,calibrate}` still work; enabling from the UI starts it.

## Measured (2026-09-30/10-01, i9-13900H, no GPU)
Groq STT 0.2–0.8 s · local base 1.7 s, tiny 0.75 s · edge-tts first audio ~0.8–1.3 s · `/chat` voice reply 2–3.5 s when Groq has quota (router ~1 s + reply ~0.5–1.3 s) · "Jarvis, stop" → silence ≈ 0.9 s · noise bursts, keyboard clicks, hum, a faint "Jarvis" and room chatter after a reply → no reaction.

## Config (`app/core/config.py` + env)
`JARVIS_VOICE_EN`, `JARVIS_VOICE_HI`, `JARVIS_VOICE_RATE_EN`, `JARVIS_VOICE_RATE_HI`, `JARVIS_STT_MODEL`, `JARVIS_STT_LOCAL`, `JARVIS_STT_MODE` (auto|groq|local), `JARVIS_END_SILENCE_MS`, `JARVIS_CLAP_WAKE` (0), `JARVIS_SERVER_TRIPWIRE` (0).

## Gotchas
- "stop" / "stop it" / "mute" (`_STOP_RE`): if Jarvis is talking (or has speech queued) it silences Jarvis; if Jarvis is silent it is sent to `/chat` as "stop the music" (pauses whatever is playing via `media_control`).
- Don't open two PyAudio streams at different rates on Windows (corrupts audio): keep the server tripwire off while the voice agent runs.
- Jarvis must never say "Jarvis" in stock phrases (it would wake itself).
- `preload_local_stt()` imports faster_whisper on the calling thread first (two-thread import trips Python's module-lock deadlock detection).
- `speak_text()` / `speak_stream()` still work standalone (`tools.set_reminder`).
- Restart BOTH the backend and the voice agent after changing either; an old agent keeps running old code (that caused the "talks by itself" report).
- Tests: `scripts/test_hindi_tts.py` (plays audio). For end-to-end tests without a mic, feed 512-sample int16 frames to `MicListener._process(bytes)`; a mock or real `/chat` on `JARVIS_API_URL`. Heavy test loops burn the Groq daily token budget.

## Graphify
`graphify explain "VoiceAgent"` · `graphify explain "Speaker"` · `graphify explain "MicListener"` · `graphify explain "pick_model"`

<!-- AUTO:BEGIN (scripts/refresh_docs.py) -->
## Files & symbols (auto-generated, line numbers are current)

- `app/services/voice.py` (949 lines): voice.py — Jarvis Voice Engine
  L55 STT_RATE · L56 TTS_RATE · L66 class Transcript · (L74 .confident) · L93 _clean_transcript() · L101 pcm_to_wav_bytes() · L118 _get_groq() · L126 groq_stt_available() · L131 groq_quota_low() · L136 _seg_get() · L140 _groq_once() · L175 _transcribe_groq() · L197 FAST_LOCAL_MODEL · L200 _load_whisper_model() · L221 _transcribe_local_sync() · L251 _transcribe_local() · L257 _finish() · L271 language_mismatch() · L282 translate_for_speech() · L312 transcribe_pcm() · L344 transcribe_audio() · L366 preload_local_stt() · L383 class Clip · (L394 .push, L399 .finish, L403 .iter_chunks, L415 .cancel) · L421 _CACHE_MAX_TEXT · L424 route_language() · L437 _voice_for() · L443 _synth_edge() · L476 _sapi_sync() · L497 _synthesize() · L533 start_clip() · L541 prewarm() · L555 class _Player · (L573 .output_level, L581 ._callback, L601 ._ensure, L613 ._push, L618 .clear, L624 .pending, L627 .play) · L669 get_player() · L683 class SentenceSplitter · (L690 .feed, L721 .flush) · L726 split_sentences() · L735 _norm_words() · L739 class Channel · (L751 .say, L760 .close, L764 .mute) · L770 class Speaker · (L791 .channel, L796 .say_now, L800 .stop_all, L809 .busy, L812 .is_echo, L837 ._wake, L841 ._gc, L844 ._take, L863 .run, L913 .wait_idle) · L922 speak_text() · L932 speak_stream()
- `scripts/voice_agent.py` (849 lines): voice_agent.py — hands-free JARVIS voice loop (separate process → POST /chat)
  L49 set_ui_state() · L59 RATE · L60 CHUNK · L62 PREROLL_S · L64 MIN_SPEECH_S · L65 MAX_UTTERANCE_S · L66 MAX_WHILE_SPEAKING_S · L69 FOLLOWUP_GREET_S · L70 FOLLOWUP_QUESTION_S · L71 MAX_PARALLEL · L77 NO_WAKE_MAX_NO_SPEECH · L78 LEVEL_OVER_NOISE · L79 LEVEL_MIN · L86 WAKE_WORDS · L92 _is_wake_token() · L104 extract_wake_word_command() · L136 _is_stop() · L144 class _SileroStream · (L152 .reset) · L165 class _EnergyVAD · (L171 .reset) · L181 class _ClapDetector · (L200 ._hf_ratio, L206 .feed) · L247 class MicListener · (L269 ._emit, L272 ._open, L275 ._calibrate, L285 ._reset_segmenter, L291 ._process, L355 ._is_user_frame, L373 .run) · L406 _clean_agentic_line() · L417 _speakable() · L424 stream_chat() · L508 PHRASES · L539 _pick() · L543 class VoiceAgent · (L560 ._on_speaker_state, L572 ._open_followup, L578 ._overlaps_speech, L585 ._ui_loop, L604 .dispatch, L622 ._run_command, L653 ._greet_after_pause, L660 .handle_utterance, L756 .on_clap, L762 .run, L799 ._safe_utterance) · L806 run_voice_agent() · L810 _launch_overlay()
- `app/services/acoustic_tripwire.py` (443 lines): acoustic_tripwire.py — Jarvis Acoustic Wake Engine
  L33 CHUNK · L34 FORMAT · L35 CHANNELS · L36 RATE · L40 VOLUME_THRESHOLD · L41 TARGET_FREQ_MIN · L42 TARGET_FREQ_MAX · L43 DOUBLE_CLAP_WINDOW · L44 COOLDOWN_AFTER_WAKE · L48 _generate_chime() · L64 _play_chime() · L75 calibrate_tripwire() · L108 class AcousticWakeEngine · (L139 .start, L151 .stop, L159 .enable, L164 .disable, L169 .recalibrate, L177 .set_volume_threshold, L182 .process_chunk, L250 .get_status, L269 ._rms, L275 ._dominant_freq, L287 ._is_clap, L297 ._run) · L429 get_engine() · L440 get_wake_event()
- `app/services/hinglish_normalizer.py` (385 lines): hinglish_normalizer.py — Devanagari Crash Prevention + Text Normalizer
  L75 normalize_for_tts() · L96 strip_markdown() · L164 _DEV_VOWELS · L168 _DEV_MATRAS · L172 _DEV_CONSONANTS · L179 _NUKTA_FORMS · L185 _translit_dev_word() · L227 loanword_ratio() · L236 devanagari_to_hinglish() · L361 hinglish_to_devanagari()
- `app/services/ssml_processor.py` (101 lines): ssml_processor.py — Human Prosody Pre-processor
  L20 _HINGLISH_PAUSE_WORDS · L27 _EMPHASIS_WORDS · L34 _FAST_PHRASES · L40 add_human_prosody() · L95 strip_ssml()
- `scripts/jarvis_overlay.py` (191 lines): Jarvis Arc Reactor Overlay
  L23 read_state() · L32 generate_arc_reactor() · L86 class JarvisOverlay · (L138 ._drag_start, L142 ._drag_move, L145 ._toggle_minimize, L154 .animate, L185 .run)
<!-- AUTO:END -->
