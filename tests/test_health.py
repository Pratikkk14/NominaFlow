"""Smoke and web view rendering tests."""

from fastapi.testclient import TestClient
from training_nomination.main import app

client = TestClient(app)


def test_health_check_endpoint() -> None:
    """Verify that health check endpoint returns 200 and healthy status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "training_nomination"


def test_root_redirect_to_login() -> None:
    """Verify that unauthenticated root request redirects to /login."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code in [302, 307]
    assert response.headers["location"] == "/login"


def test_login_page_renders_html() -> None:
    """Verify login page renders properly."""
    response = client.get("/login")
    assert response.status_code == 200
    assert "System Login" in response.text
    assert "employee@nominaflow.com" in response.text
