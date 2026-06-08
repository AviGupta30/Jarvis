import cv2
import numpy as np
import os
import subprocess
from app.services.dark_enhancement import run_pipeline_a, run_pipeline_b

def _enhance_frame(frame, pipeline_type):
    if pipeline_type == "A":
        return run_pipeline_a(frame)
    else:
        _, _, final = run_pipeline_b(frame)
        return final

def _get_ffmpeg_binary():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None

def _reencode_to_h264(input_path, output_path, ffmpeg_bin):
    """Re-encode a video to H.264 MP4 so browsers can play it."""
    print(f"--- Re-encoding to H.264 for browser compatibility ---")
    cmd = [
        ffmpeg_bin,
        "-y",
        "-i", input_path,
        "-vcodec", "libx264",
        "-crf", "23",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg stderr: {result.stderr}")
        raise RuntimeError("ffmpeg re-encoding failed.")
    print("--- Re-encoding complete ---")

def process_video_smartly(input_path, output_path, sample_rate=4):
    print(f"--- Starting Smart Video Enhancement (Sample Rate: {sample_rate}) ---")
    
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Original: {width}x{height} @ {fps}fps ({total_frames} frames)")

    ret, first_frame = cap.read()
    if not ret:
        raise ValueError("Video is empty.")
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    lab = cv2.cvtColor(first_frame, cv2.COLOR_BGR2LAB)
    l, _, _ = cv2.split(lab)
    mean_brightness = np.mean(l)
    mean_percent = (mean_brightness / 255) * 100
    
    pipeline_type = "A" if mean_percent > 5.0 else "B"
    print(f"--- Detected Brightness: {mean_percent:.2f}% -> Using Pipeline {pipeline_type} ---")

    # Write to a temp file first with mp4v
    ffmpeg_bin = _get_ffmpeg_binary()
    if ffmpeg_bin:
        temp_path = output_path + ".tmp.mp4"
    else:
        temp_path = output_path  # fallback: write directly

    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    out = cv2.VideoWriter(temp_path, fourcc, fps, (width, height))

    prev_enhanced_frame = None
    processed_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if processed_count % sample_rate == 0:
            print(f"Processing Keyframe {processed_count}/{total_frames}...")
            curr_enhanced_frame = _enhance_frame(frame, pipeline_type)
            
            if prev_enhanced_frame is not None:
                for i in range(1, sample_rate):
                    alpha = i / sample_rate
                    interpolated = cv2.addWeighted(prev_enhanced_frame, 1 - alpha, curr_enhanced_frame, alpha, 0)
                    out.write(interpolated)
            
            out.write(curr_enhanced_frame)
            prev_enhanced_frame = curr_enhanced_frame
            
        processed_count += 1

    cap.release()
    out.release()
    print("--- Frame writing complete ---")

    # Re-encode to H.264 so all browsers can play it
    if ffmpeg_bin and temp_path != output_path:
        _reencode_to_h264(temp_path, output_path, ffmpeg_bin)
        try:
            os.remove(temp_path)
        except Exception:
            pass
    
    print("--- Video Enhancement Complete ---")
    return output_path