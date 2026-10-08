"""Reviewer decision and approval workflow integration tests."""

from fastapi.testclient import TestClient

from training_nomination.main import app

client = TestClient(app)


def get_token(email: str, password: str = "password123") -> dict[str, str]:
    """Helper getting Bearer headers for a specific user role."""
    res = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_reviewer_queue_and_approve_workflow():
    """Verify complete review flow from submission to approval."""
    emp_headers = get_token("employee@nominaflow.com")
    rev_headers = get_token("reviewer@nominaflow.com")

    # 1. Employee creates and submits nomination
    create_res = client.post(
        "/api/v1/nominations",
        json={
            "title": "Site Reliability Engineering (SRE) Bootcamp",
            "provider": "Google Cloud",
            "training_date": "2026-11-20",
        },
        headers=emp_headers,
    )
    nom_id = create_res.json()["id"]
    client.post(f"/api/v1/nominations/{nom_id}/submit", headers=emp_headers)

    # 2. Reviewer retrieves queue
    queue_res = client.get("/api/v1/reviewer/nominations", headers=rev_headers)
    assert queue_res.status_code == 200
    queue_ids = [n["id"] for n in queue_res.json()]
    assert nom_id in queue_ids

    # 3. Reviewer starts review
    start_res = client.post(
        f"/api/v1/reviewer/nominations/{nom_id}/start-review",
        headers=rev_headers,
    )
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "UNDER_REVIEW"

    # 4. Reviewer approves
    approve_res = client.post(
        f"/api/v1/reviewer/nominations/{nom_id}/approve",
        headers=rev_headers,
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "APPROVED"


def test_reviewer_reject_with_comment():
    """Verify reviewer rejection requiring mandatory comment."""
    emp_headers = get_token("employee@nominaflow.com")
    rev_headers = get_token("reviewer@nominaflow.com")

    # Create and submit
    create_res = client.post(
        "/api/v1/nominations",
        json={
            "title": "Unaccredited Weekend Workshop",
            "provider": "Unknown Academy",
            "training_date": "2026-10-05",
        },
        headers=emp_headers,
    )
    nom_id = create_res.json()["id"]
    client.post(f"/api/v1/nominations/{nom_id}/submit", headers=emp_headers)
    client.post(f"/api/v1/reviewer/nominations/{nom_id}/start-review", headers=rev_headers)

    # Rejection without comment should fail (Pydantic validation 422)
    empty_reject_res = client.post(
        f"/api/v1/reviewer/nominations/{nom_id}/reject",
        json={"comment": ""},
        headers=rev_headers,
    )
    assert empty_reject_res.status_code == 422

    # Valid rejection
    reject_res = client.post(
        f"/api/v1/reviewer/nominations/{nom_id}/reject",
        json={"comment": "Course provider is not in our accredited vendor list."},
        headers=rev_headers,
    )
    assert reject_res.status_code == 200
    assert reject_res.json()["status"] == "REJECTED"


def test_employee_cannot_access_reviewer_endpoints():
    """Verify that employee role receives HTTP 403 on reviewer routes."""
    emp_headers = get_token("employee@nominaflow.com")
    res = client.get("/api/v1/reviewer/nominations", headers=emp_headers)
    assert res.status_code == 403
