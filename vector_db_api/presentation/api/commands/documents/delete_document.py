from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.commands.documents import (
    DeleteDocumentCommand,
    DeleteDocumentHandler,
)
from vector_db_api.api.routers import documents_router as router
from vector_db_api.container import get_delete_document_handler


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
