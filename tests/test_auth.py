"""Authentication and authorization unit and integration tests."""

import pytest
from fastapi.testclient import TestClient
from training_nomination.main import app

client = TestClient(app)


def test_login_success_employee():
    """Verify that valid employee credentials return a JWT token and user info."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "employee@nominaflow.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "EMPLOYEE"
    assert data["email"] == "employee@nominaflow.com"


def test_login_success_reviewer():
    """Verify reviewer login and role recognition."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "reviewer@nominaflow.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "REVIEWER"


def test_login_success_admin():
    """Verify admin login and role recognition."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@nominaflow.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "ADMIN"


def test_login_invalid_password():
    """Verify that wrong password returns HTTP 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "employee@nominaflow.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user():
    """Verify that non-existent email returns HTTP 401."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@nominaflow.com", "password": "password123"},
    )
    assert response.status_code == 401


def test_get_current_user_me():
    """Verify /api/v1/auth/me endpoint with Bearer token."""
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "employee@nominaflow.com", "password": "password123"},
    )
    token = login_res.json()["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "employee@nominaflow.com"
    assert data["role"] == "EMPLOYEE"


def test_logout():
    """Verify logout endpoint clears session."""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out."
