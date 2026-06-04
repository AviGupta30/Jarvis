import sys
import os

# Add root to sys path so we can import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from app.services.agentic_web import agentic_web_action

if __name__ == "__main__":
    print("Starting agentic web test...")
    # Test with unstop and finding hackathons
    result = agentic_web_action("go to unstop and search for hackathons")
    print("\n--- Final Result ---")
    print(result)
