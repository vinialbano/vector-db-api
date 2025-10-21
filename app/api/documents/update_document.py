from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from app.application.documents import (
    UpdateDocumentCommand,
    UpdateDocumentHandler,
)
from app.dependencies import get_document_repository
from app.domain.documents.document_repository import DocumentRepository

update_document_router = APIRouter()


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


@update_document_router.patch(
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
