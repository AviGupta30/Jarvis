from fastapi.testclient import TestClient
from app.main import app
import traceback

client = TestClient(app)

try:
    print("Testing 'make an whatsapp call to mom'...")
    response1 = client.post("/chat", json={"prompt": "make an whatsapp call to mom"})
    print("Response 1:", response1.status_code, response1.text)
    
    print("\nTesting 'yes'...")
    response2 = client.post("/chat", json={"prompt": "yes"})
    print("Response 2:", response2.status_code, response2.text)
except Exception as e:
    print("CRASHED!")
    traceback.print_exc()
