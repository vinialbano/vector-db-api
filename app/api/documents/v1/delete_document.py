from fastapi import Depends, status
from pydantic import BaseModel, ConfigDict

from app.api.documents.router import documents_router as router
from app.application.documents import (
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from app.container import get_document_repository
from app.domain.documents import DocumentRepository


def get_delete_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteDocumentHandler:
    """DI provider for DeleteDocumentHandler"""
    return DeleteDocumentHandler(document_repo)


class DeleteDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    handler: DeleteDocumentHandler = Depends(get_delete_document_handler),
):
    """Delete a document."""
    command = DeleteDocumentCommand(document_id=document_id)
    handler.handle(command)
