import sys
import os

# Add the project root to sys.path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.content_humanizer import humanize_text_sync

def test():
    ai_text = (
        "Furthermore, it is crucial to recognize that the rapid advancement of technology "
        "has significantly impacted various sectors of the economy. In conclusion, we must "
        "utilize these robust tools to delve into comprehensive data analysis and optimize "
        "our operational efficiency. It is important to note that without proper integration, "
        "the potential benefits will remain unrealized."
    )
    print("=== Original AI Text ===")
    print(ai_text)
    print("\n=== Running 7-Step Humanizer Pipeline (Please wait...) ===")
    
    humanized_text = humanize_text_sync(ai_text)
    
    print("\n=== Final Humanized Text ===")
    print(humanized_text)

if __name__ == "__main__":
    test()
