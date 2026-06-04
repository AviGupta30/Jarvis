"""
Download Kokoro TTS model files from GitHub releases.
Run this ONCE to get the model files. They are then cached in the models/ folder.
"""
import os
import urllib.request

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models", "kokoro")
os.makedirs(MODELS_DIR, exist_ok=True)

MODEL_URL  = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.int8.onnx"
VOICES_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
MODEL_PATH  = os.path.join(MODELS_DIR, "kokoro-v1.0.int8.onnx")
VOICES_PATH = os.path.join(MODELS_DIR, "voices-v1.0.bin")

def download(url, path, label):
    if os.path.exists(path):
        print(f"  [skip] {label} already exists at {path}")
        return
    print(f"  Downloading {label}...")
    print(f"  URL: {url}")
    size = 0
    def progress(count, block_size, total_size):
        nonlocal size
        downloaded = count * block_size
        if total_size > 0:
            pct = min(downloaded / total_size * 100, 100)
            mb = downloaded / 1024 / 1024
            print(f"\r  {pct:.1f}% ({mb:.1f} MB)", end="", flush=True)
    urllib.request.urlretrieve(url, path, reporthook=progress)
    print(f"\n  Done: {path}")

print("Downloading Kokoro TTS model files...")
download(MODEL_URL,  MODEL_PATH,  "Kokoro model (int8 quantized, ~85MB)")
download(VOICES_URL, VOICES_PATH, "Voices pack (~2MB)")
print("\nAll files ready. Kokoro TTS is set up.")
print(f"Model:  {MODEL_PATH}")
print(f"Voices: {VOICES_PATH}")
