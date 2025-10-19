from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.api.documents.router import documents_router as router
from vector_db_api.application.documents import (
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from vector_db_api.container import get_document_repository
from vector_db_api.domain.documents import DocumentRepository


def get_delete_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteDocumentHandler:
    """DI provider for DeleteDocumentHandler"""
    return DeleteDocumentHandler(document_repo)


class DeleteDocumentResponse(BaseModel):
    document_id: str

    class Config:
        from_attributes = True


@router.delete("/{document_id}", response_model=DeleteDocumentResponse)
def delete_document(
    document_id: str,
    handler: DeleteDocumentHandler = Depends(get_delete_document_handler),
):
    """Delete a document."""
    command = DeleteDocumentCommand(document_id=document_id)
    response = handler.handle(command)
    return DeleteDocumentResponse(document_id=response.document_id)
