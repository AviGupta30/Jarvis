import urllib.request
import json
import traceback

try:
    req = urllib.request.Request(
        'http://127.0.0.1:8000/chat',
        data=json.dumps({'prompt': 'make an whatsapp call to mom'}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
        with open('test_api_resp.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Success! Response saved to test_api_resp.txt")
except Exception as e:
    with open('test_api_resp.txt', 'w', encoding='utf-8') as f:
        f.write("Error: " + str(e) + "\n")
        if hasattr(e, 'read'):
            f.write("Server Response: " + e.read().decode('utf-8', errors='ignore') + "\n")
        f.write(traceback.format_exc())
    print("Error occurred, check test_api_resp.txt")
