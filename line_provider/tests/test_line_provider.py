from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)


def test_create_event():
    response = client.post(
        "/events",
        json={
            "id": "event1",
            "odds": 1.5,
            "deadline": "2024-12-31T23:59:59",
            "status": "ongoing",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Event added successfully"}
