import requests

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    print("\n[1] Testing /health ...")
    r = requests.get(f"{BASE_URL}/health")
    print("Status:", r.status_code, r.json())

def test_agents():
    print("\n[2] Testing /agents ...")
    r = requests.get(f"{BASE_URL}/agents")
    print("Status:", r.status_code, "\nAgents:", r.json())

def test_dummy():
    print("\n[3] Testing dummy agent via /process ...")
    payload = {
        "agent": "dummy",
        "user_input": "Hello Baymax!",
        "context": {"mood": "happy"}
    }
    r = requests.post(f"{BASE_URL}/process", json=payload)
    print("Status:", r.status_code, "\nResponse:", r.json())

def test_symptom_checker():
    print("\n[4] Testing symptom checker agent (OpenRouter) via /process ...")
    payload = {
        "agent": "symptom_checker",
        "user_input": "I have a sore throat, headache, and mild fever.",
        "context": {}
    }
    r = requests.post(f"{BASE_URL}/process", json=payload)
    print("Status:", r.status_code, "\nResponse:", r.json())



print("=== Baymax Orchestrator Test ===")
test_health()
test_agents()
test_dummy()
test_symptom_checker()
