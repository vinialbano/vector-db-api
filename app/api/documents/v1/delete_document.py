from fastapi import Depends
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
    document_id: str

    model_config = ConfigDict(from_attributes=True)


@router.delete("/{document_id}", response_model=DeleteDocumentResponse)
def delete_document(
    document_id: str,
    handler: DeleteDocumentHandler = Depends(get_delete_document_handler),
):
    """Delete a document."""
    command = DeleteDocumentCommand(document_id=document_id)
    response = handler.handle(command)
    return DeleteDocumentResponse(document_id=response.document_id)
