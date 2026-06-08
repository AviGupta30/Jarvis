import os
import cv2
from app.services.dark_enhancement import get_all_enhancements
from app.services.dark_video_enhancement import process_video_smartly

def enhance_media(file_path: str) -> str:
    """Enhance a dark image or video using the dark enhancement pipeline. 
    It returns a specialized Markdown string that the frontend renders as an image or video with a download button."""
    
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
        
    ext = file_path.lower().split('.')[-1]
    filename = os.path.basename(file_path)
    
    # ensure data/uploads folder exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(current_dir)
    base_dir = os.path.dirname(app_dir)
    uploads_dir = os.path.join(base_dir, "data", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    
    if ext in ['png', 'jpg', 'jpeg', 'webp']:
        try:
            cv2_image = cv2.imread(file_path)
            if cv2_image is None:
                return f"Failed to read image at {file_path}"
            path1, path2, final_img, pipeline = get_all_enhancements(cv2_image)
            
            output_filename = f"enhanced_{filename}"
            output_path = os.path.join(uploads_dir, output_filename)
            cv2.imwrite(output_path, final_img)
            
            # Return specialized markdown for the frontend
            url = f"http://127.0.0.1:8000/media/{output_filename}"
            return f"Here is the enhanced image:\n\n![Enhanced Image]({url})"
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Failed to enhance image: {e}"
            
    elif ext in ['mp4', 'avi', 'mov', 'mkv']:
        try:
            output_filename = f"enhanced_{filename}"
            # Ensure it's mp4 format since reencoding to H.264
            if not output_filename.endswith('.mp4'):
                output_filename = output_filename.rsplit('.', 1)[0] + '.mp4'
                
            output_path = os.path.join(uploads_dir, output_filename)
            
            process_video_smartly(file_path, output_path)
            
            url = f"http://127.0.0.1:8000/media/{output_filename}"
            return f"Here is the enhanced video:\n\n![Enhanced Video]({url})"
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Failed to enhance video: {e}"
    else:
        return f"Unsupported file type: {ext}. Only images and videos are supported."
