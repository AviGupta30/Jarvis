import sys
sys.path.append('.')
from app.api.chat import detect_whatsapp_call, detect_whatsapp_send

try:
    print("Testing detect_whatsapp_call...")
    res = detect_whatsapp_call("make an whatsapp call to mom")
    print("Call result:", res)
    
    print("\nTesting detect_whatsapp_send...")
    res2 = detect_whatsapp_send("send a whatsapp message to mom")
    print("Send result:", res2)
except Exception as e:
    import traceback
    traceback.print_exc()
