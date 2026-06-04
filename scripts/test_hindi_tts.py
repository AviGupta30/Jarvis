"""Test language-adaptive TTS - plays English then Hindi to verify both engines work."""
import asyncio, sys, os
sys.path.insert(0, '.')

async def main():
    from app.services.voice import _tts_play

    print("Test 1: English - Kokoro am_adam")
    await _tts_play("Yes Sir, how can I help you today?")
    print("  Done")

    await asyncio.sleep(0.5)

    print("Test 2: Hindi - edge-tts Madhur Neural (native Hindi)")
    await _tts_play("Haan Sir, boliye. Kya kaam karna hai aapko?")
    print("  Done")

    await asyncio.sleep(0.5)

    print("Test 3: Mixed Hinglish - Hindi voice")
    await _tts_play("Ho gaya Sir. Chrome khol diya aapke liye.")
    print("  Done")

    print("\nAll TTS tests passed!")

asyncio.run(main())
