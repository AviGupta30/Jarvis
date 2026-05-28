import sys
sys.path.insert(0, '.')
from app.services.gmail_tool import check_emails, list_unread
import traceback

print("Testing list_unread():")
try:
    res = list_unread(2)
    print(res)
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

print("\nTesting check_emails('test'):")
try:
    res = check_emails('test', 2)
    print(res)
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
