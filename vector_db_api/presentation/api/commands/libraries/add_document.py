from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.application.commands.libraries import (
    AddDocumentCommand,
    AddDocumentHandler,
)
from vector_db_api.api.routers import libraries_router as router
from vector_db_api.container import get_add_document_handler


class AddDocumentResponse(BaseModel):
    library_id: str
    document_id: str

    class Config:
        from_attributes = True


@router.post(
    "/{library_id}/documents/{document_id}", response_model=AddDocumentResponse
)
def add_document(
    library_id: str,
    document_id: str,
    handler: AddDocumentHandler = Depends(get_add_document_handler),
):
    command = AddDocumentCommand(library_id=library_id, document_id=document_id)
    response = handler.handle(command)
    return AddDocumentResponse(
        library_id=response.library_id, document_id=response.document_id
    )
