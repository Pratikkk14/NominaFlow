"""Administrator monitoring, filtering, and audit trail tests."""

from fastapi.testclient import TestClient

from training_nomination.main import app

client = TestClient(app)


def get_token(email: str = "admin@nominaflow.com") -> dict[str, str]:
    """Helper getting Bearer headers."""
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_admin_get_all_nominations_and_filter():
    """Verify administrator retrieving all nominations with status filter."""
    admin_headers = get_token("admin@nominaflow.com")
    emp_headers = get_token("employee@nominaflow.com")

    # Create a draft nomination
    client.post(
        "/api/v1/nominations",
        json={"title": "Admin Test Program", "provider": "Provider D", "training_date": "2026-12-01"},
        headers=emp_headers,
    )

    # 1. Admin gets all
    all_res = client.get("/api/v1/admin/nominations", headers=admin_headers)
    assert all_res.status_code == 200
    assert len(all_res.json()) >= 1

    # 2. Admin filters by DRAFT
    draft_res = client.get("/api/v1/admin/nominations?status=DRAFT", headers=admin_headers)
    assert draft_res.status_code == 200
    for nom in draft_res.json():
        assert nom["status"] == "DRAFT"


def test_admin_get_audit_events():
    """Verify administrator querying global audit event logs."""
    admin_headers = get_token("admin@nominaflow.com")
    audit_res = client.get("/api/v1/admin/audit-events", headers=admin_headers)
    assert audit_res.status_code == 200
    events = audit_res.json()
    assert isinstance(events, list)
    assert len(events) >= 1
    assert "event_type" in events[0]
    assert "timestamp" in events[0]


def test_admin_list_users():
    """Verify administrator listing all registered users."""
    admin_headers = get_token("admin@nominaflow.com")
    users_res = client.get("/api/v1/admin/users", headers=admin_headers)
    assert users_res.status_code == 200
    users = users_res.json()
    assert len(users) >= 3  # Employee, Reviewer, Admin seeded


def test_employee_forbidden_from_admin_routes():
    """Verify employee cannot query admin endpoints."""
    emp_headers = get_token("employee@nominaflow.com")
    res = client.get("/api/v1/admin/nominations", headers=emp_headers)
    assert res.status_code == 403
