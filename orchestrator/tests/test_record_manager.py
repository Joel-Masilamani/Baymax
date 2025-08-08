import pytest
from fastapi.testclient import TestClient
from orchestrator.main import app
from datetime import date

client = TestClient(app)

@pytest.fixture
def sample_record():
    return {
        "user_id": 1,
        "medicine_name": "Paracetamol",
        "dosage": "500mg",
        "timings": ["08:00", "20:00"],
        "start_date": str(date(2025, 8, 8)),
        "end_date": str(date(2025, 8, 15))
    }

def test_create_record(sample_record):
    response = client.post("/records/", json=sample_record)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["medicine_name"] == sample_record["medicine_name"]
    assert "id" in data

def test_get_active_records(sample_record):
    client.post("/records/", json=sample_record)
    response = client.get(f"/records/active/{sample_record['user_id']}")
    assert response.status_code == 200, response.text
    assert isinstance(response.json(), list)

def test_delete_record(sample_record):
    # First create a record
    create_resp = client.post("/records/", json=sample_record)
    record_id = create_resp.json()["id"]

    # Now delete it
    delete_resp = client.delete(f"/records/{record_id}")
    assert delete_resp.status_code == 200, delete_resp.text
    assert delete_resp.json()["message"] == "Deleted successfully"
