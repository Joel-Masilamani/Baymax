from fastapi.testclient import TestClient
from orchestrator.main import app

client = TestClient(app)

def test_dummy():
    payload = {
        "agent": "dummy",
        "user_input": "Hello Baymax!",
        "context": {"mood": "happy"}
    }
    r = client.post("/process", json=payload)
    print("Status:", r.status_code, "\nResponse:", r.json())
