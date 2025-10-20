from typing import Any, Dict, Optional

from fastapi import Depends, status
from pydantic import BaseModel, ConfigDict

from app.api.documents.router import documents_router as router
from app.application.documents import (
    UpdateDocumentCommand,
    UpdateDocumentHandler,
)
from app.container import get_document_repository
from app.domain.documents.document_repository import DocumentRepository


def get_update_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> UpdateDocumentHandler:
    """DI provider for UpdateDocumentHandler"""
    return UpdateDocumentHandler(document_repo)


class UpdateDocumentRequest(BaseModel):
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@router.patch(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_document(
    document_id: str,
    request: UpdateDocumentRequest,
    handler: UpdateDocumentHandler = Depends(get_update_document_handler),
):
    """Update a document."""
    command = UpdateDocumentCommand(
        document_id=document_id,
        title=request.title,
        custom_fields=request.metadata,
    )
    handler.handle(command)
