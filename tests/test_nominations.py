"""Nomination CRUD and submission integration tests."""

from fastapi.testclient import TestClient

from training_nomination.main import app

client = TestClient(app)


def get_auth_header(email="employee@nominaflow.com", password="password123"):
    """Helper to obtain a Bearer authorization header."""
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_nomination_draft():
    """Verify creating a nomination draft."""
    headers = get_auth_header()
    payload = {
        "title": "Kubernetes Administrator Certification (CKA)",
        "provider": "Linux Foundation",
        "description": "Comprehensive container orchestration and cluster management.",
        "training_type": "DevOps & Cloud",
        "training_date": "2026-11-15",
        "duration": "4 Days",
        "cost": 395.00,
        "justification": "Required for upcoming production Kubernetes rollout.",
    }

    response = client.post("/api/v1/nominations", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["status"] == "DRAFT"
    assert data["cost"] == 395.00
    assert len(data["audit_events"]) >= 1
    assert data["audit_events"][0]["event_type"] == "NOMINATION_CREATED"


def test_update_nomination_draft():
    """Verify updating fields of a draft nomination."""
    headers = get_auth_header()
    create_res = client.post(
        "/api/v1/nominations",
        json={
            "title": "Initial Draft Title",
            "provider": "Vendor X",
            "training_date": "2026-12-01",
        },
        headers=headers,
    )
    nomination_id = create_res.json()["id"]

    # Update title and cost
    update_res = client.put(
        f"/api/v1/nominations/{nomination_id}",
        json={"title": "Updated Draft Title", "cost": 150.0},
        headers=headers,
    )
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated Draft Title"
    assert update_res.json()["cost"] == 150.0


def test_submit_nomination_success():
    """Verify submitting a draft nomination transitions status to SUBMITTED."""
    headers = get_auth_header()
    create_res = client.post(
        "/api/v1/nominations",
        json={
            "title": "Terraform Infrastructure as Code",
            "provider": "HashiCorp",
            "training_date": "2026-10-20",
        },
        headers=headers,
    )
    nomination_id = create_res.json()["id"]

    submit_res = client.post(
        f"/api/v1/nominations/{nomination_id}/submit",
        headers=headers,
    )
    assert submit_res.status_code == 200
    data = submit_res.json()
    assert data["status"] == "SUBMITTED"
    assert data["submitted_at"] is not None

    # Verify editing a submitted nomination fails
    edit_res = client.put(
        f"/api/v1/nominations/{nomination_id}",
        json={"title": "Cannot Edit After Submit"},
        headers=headers,
    )
    assert edit_res.status_code == 400


def test_list_my_nominations():
    """Verify listing nominations belonging to the authenticated employee."""
    headers = get_auth_header()
    response = client.get("/api/v1/nominations", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_nomination_status_and_history():
    """Verify status tracking and audit log endpoints."""
    headers = get_auth_header()
    create_res = client.post(
        "/api/v1/nominations",
        json={
            "title": "AWS Solutions Architect",
            "provider": "Amazon Web Services",
            "training_date": "2026-12-10",
        },
        headers=headers,
    )
    nomination_id = create_res.json()["id"]

    status_res = client.get(f"/api/v1/nominations/{nomination_id}/status", headers=headers)
    assert status_res.status_code == 200
    assert status_res.json()["status"] == "DRAFT"

    history_res = client.get(f"/api/v1/nominations/{nomination_id}/history", headers=headers)
    assert history_res.status_code == 200
    assert len(history_res.json()) >= 1
