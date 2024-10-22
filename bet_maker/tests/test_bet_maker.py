from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_place_bet():
    response = client.post("/bet", json={"event_id": "event1", "amount": 100.0})
    assert response.status_code == 200
    assert "bet_id" in response.json()
