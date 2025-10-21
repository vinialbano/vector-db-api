from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from app.application.documents import (
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from app.dependencies import get_document_repository
from app.domain.documents import DocumentRepository

delete_document_router = APIRouter()


def get_delete_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteDocumentHandler:
    """DI provider for DeleteDocumentHandler"""
    return DeleteDocumentHandler(document_repo)


class DeleteDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@delete_document_router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: str,
    handler: DeleteDocumentHandler = Depends(get_delete_document_handler),
):
    """Delete a document."""
    command = DeleteDocumentCommand(document_id=document_id)
    handler.handle(command)
