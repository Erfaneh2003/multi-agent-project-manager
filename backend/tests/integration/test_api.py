from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


REQUEST = {
    "project_id": "p1",
    "project": {
        "title": "Planning system",
        "description": "A small system for planning and tracking software work.",
        "goals": ["Track tasks"],
    },
    "team_members": [],
}


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "mode": "mock"}


def test_workflow_requires_approval_before_allocation() -> None:
    response = client.post("/api/v1/projects/p1/run-workflow", json=REQUEST)

    assert response.status_code == 200
    body = response.json()
    assert body["current_stage"] == "awaiting_human_approval"
    assert body["allocation_proposals"] == []


def test_approved_workflow_returns_schedule() -> None:
    request = {**REQUEST, "approval_status": "approved"}

    response = client.post("/api/v1/projects/p1/run-workflow", json=request)

    assert response.status_code == 200
    body = response.json()
    assert body["current_stage"] == "completed"
    assert len(body["schedule"]["tasks"]) == 1
