from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.commands.libraries import (
    RemoveDocumentCommand,
    RemoveDocumentHandler,
)
from vector_db_api.presentation.api.routers import libraries_router as router
from vector_db_api.presentation.container import get_remove_document_handler


class RemoveDocumentResponse(BaseModel):
    library_id: str
    document_id: str
    removed: bool

    class Config:
        from_attributes = True


@router.delete(
    "/{library_id}/documents/{document_id}", response_model=RemoveDocumentResponse
)
def remove_document(
    library_id: str,
    document_id: str,
    handler: RemoveDocumentHandler = Depends(get_remove_document_handler),
):
    command = RemoveDocumentCommand(library_id=library_id, document_id=document_id)
    response = handler.handle(command)
    return RemoveDocumentResponse(
        library_id=response.library_id,
        document_id=response.document_id,
        removed=response.removed,
    )
