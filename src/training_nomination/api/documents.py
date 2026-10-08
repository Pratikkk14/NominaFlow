"""Documents API router for file upload and streaming."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from training_nomination.core.dependencies import get_current_user
from training_nomination.db.session import get_db
from training_nomination.models.nomination import TrainingNomination
from training_nomination.models.user import User
from training_nomination.schemas.document import DocumentResponse
from training_nomination.services.document_service import (
    get_document_file_path,
    save_nomination_document,
)

router = APIRouter(tags=["Documents"])


@router.post(
    "/api/v1/nominations/{nomination_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    nomination_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> DocumentResponse:
    """Upload a supporting file attachment (PDF/PNG/JPEG) for a nomination."""
    doc = save_nomination_document(
        db=db,
        nomination_id=nomination_id,
        user=current_user,
        file=file,
    )
    return DocumentResponse.model_validate(doc)


@router.get(
    "/api/v1/nominations/{nomination_id}/documents",
    response_model=list[DocumentResponse],
)
def list_documents(
    nomination_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[DocumentResponse]:
    """List all documents attached to a nomination."""
    nomination = db.query(TrainingNomination).filter(TrainingNomination.id == nomination_id).first()
    if not nomination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nomination with ID '{nomination_id}' not found.",
        )

    return [DocumentResponse.model_validate(doc) for doc in nomination.documents]


@router.get("/api/v1/documents/{document_id}")
def download_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> FileResponse:
    """Download/view a stored supporting document."""
    file_path, filename, mime_type = get_document_file_path(
        db=db,
        document_id=document_id,
        user=current_user,
    )
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type=mime_type,
    )
