"""Document upload, validation, and retrieval tests."""

import io
import pytest
from fastapi.testclient import TestClient
from training_nomination.main import app

client = TestClient(app)


def get_token(email: str = "employee@nominaflow.com") -> dict[str, str]:
    """Helper getting auth headers."""
    res = client.post("/api/v1/auth/login", json={"email": email, "password": "password123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_upload_and_download_document():
    """Verify uploading a valid PDF document and retrieving it."""
    headers = get_token()

    # 1. Create nomination
    create_res = client.post(
        "/api/v1/nominations",
        json={"title": "Doc Test Course", "provider": "Provider A", "training_date": "2026-11-01"},
        headers=headers,
    )
    nom_id = create_res.json()["id"]

    # 2. Upload sample PDF
    fake_pdf = io.BytesIO(b"%PDF-1.4 sample syllabus content for testing")
    upload_res = client.post(
        f"/api/v1/nominations/{nom_id}/documents",
        files={"file": ("syllabus.pdf", fake_pdf, "application/pdf")},
        headers=headers,
    )
    assert upload_res.status_code == 201
    doc_data = upload_res.json()
    doc_id = doc_data["id"]
    assert doc_data["file_name"] == "syllabus.pdf"

    # 3. List documents
    list_res = client.get(f"/api/v1/nominations/{nom_id}/documents", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) >= 1

    # 4. Download document
    download_res = client.get(f"/api/v1/documents/{doc_id}", headers=headers)
    assert download_res.status_code == 200
    assert b"sample syllabus content" in download_res.content


def test_upload_invalid_mime_type():
    """Verify that disallowed file types (e.g. .exe) are rejected."""
    headers = get_token()
    create_res = client.post(
        "/api/v1/nominations",
        json={"title": "Mime Test", "provider": "Provider B", "training_date": "2026-11-01"},
        headers=headers,
    )
    nom_id = create_res.json()["id"]

    bad_file = io.BytesIO(b"executable binaries")
    upload_res = client.post(
        f"/api/v1/nominations/{nom_id}/documents",
        files={"file": ("malware.exe", bad_file, "application/x-msdownload")},
        headers=headers,
    )
    assert upload_res.status_code == 400
    assert "Invalid file type" in upload_res.json()["detail"]


def test_upload_oversize_file():
    """Verify that files exceeding size limit are rejected."""
    headers = get_token()
    create_res = client.post(
        "/api/v1/nominations",
        json={"title": "Size Test", "provider": "Provider C", "training_date": "2026-11-01"},
        headers=headers,
    )
    nom_id = create_res.json()["id"]

    # Generate 6MB file (limit is 5MB)
    large_file = io.BytesIO(b"0" * (6 * 1024 * 1024))
    upload_res = client.post(
        f"/api/v1/nominations/{nom_id}/documents",
        files={"file": ("large.pdf", large_file, "application/pdf")},
        headers=headers,
    )
    assert upload_res.status_code == 400
    assert "exceeds maximum allowed size" in upload_res.json()["detail"]
