from typing import Any, Dict, Optional

from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.documents import (
    UpdateDocumentCommand,
    UpdateDocumentHandler,
)
from vector_db_api.api.routers import documents_router as router
from vector_db_api.container import get_update_document_handler


class UpdateDocumentRequest(BaseModel):
    title: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateDocumentResponse(BaseModel):
    document_id: str

    class Config:
        from_attributes = True


@router.patch("/{document_id}", response_model=UpdateDocumentResponse)
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
    response = handler.handle(command)
    return UpdateDocumentResponse(document_id=response.document_id)
