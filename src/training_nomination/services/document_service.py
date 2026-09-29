"""Document handling, storage, and validation service."""

import os
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from training_nomination.config import settings
from training_nomination.models.document import Document
from training_nomination.models.nomination import NominationStatus, TrainingNomination
from training_nomination.models.user import User


def save_nomination_document(
    db: Session,
    nomination_id: str,
    user: User,
    file: UploadFile,
) -> Document:
    """Validate, store locally, and link uploaded file to a nomination."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    # Only author can attach documents to DRAFT or SUBMITTED nominations
    if nomination.employee_id != user.id and user.role.name != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload documents for your own nominations.",
        )

    if nomination.status in [NominationStatus.APPROVED.value, NominationStatus.REJECTED.value]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot upload documents for a finalized nomination in '{nomination.status}' state.",
        )

    # 1. MIME type validation
    content_type = file.content_type or "application/octet-stream"
    if content_type not in settings.ALLOWED_MIME_TYPES:
        # Check by file extension fallback
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in [".pdf", ".png", ".jpg", ".jpeg"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type '{content_type}'. Allowed types: PDF, PNG, JPEG.",
            )

    # 2. Read file and validate size
    contents = file.file.read()
    file_size = len(contents)
    if file_size > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_FILE_SIZE_BYTES / (1024*1024):.1f} MB.",
        )

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    # 3. Save to disk with unique sanitized filename
    file_uuid = str(uuid.uuid4())
    safe_ext = os.path.splitext(file.filename or "doc")[1].lower()
    stored_filename = f"{file_uuid}{safe_ext}"
    target_path = settings.UPLOAD_DIR / stored_filename

    with open(target_path, "wb") as f:
        f.write(contents)

    # 4. Save metadata to database
    doc = Document(
        nomination_id=nomination_id,
        file_name=file.filename or "attachment",
        file_path=str(target_path),
        file_type=content_type,
        file_size=file_size,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def get_document_file_path(
    db: Session,
    document_id: str,
    user: User,
) -> tuple[Path, str, str]:
    """Retrieve document disk path and verify access permission."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document with ID '{document_id}' not found.",
        )

    # Check permission: owner, reviewer, or admin
    nomination = doc.nomination
    if nomination.employee_id != user.id and user.role.name not in ["REVIEWER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You are not authorized to view this document.",
        )

    file_path = Path(doc.file_path)
    if not file_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File is missing from disk storage.",
        )

    return file_path, doc.file_name, doc.file_type
