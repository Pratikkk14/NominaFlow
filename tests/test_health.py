"""Smoke and skeleton verification tests for NominaFlow."""

from fastapi.testclient import TestClient

from training_nomination.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Verify that root endpoint returns 200 and project metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["project"] == "NominaFlow"
    assert data["status"] == "Repository Initialized"


def test_health_check_endpoint() -> None:
    """Verify that health check endpoint returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "training_nomination"
