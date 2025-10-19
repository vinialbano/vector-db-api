from fastapi import Depends
from pydantic import BaseModel

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    AddDocumentCommand,
    AddDocumentHandler,
)
from app.container import get_document_repository, get_library_repository
from app.domain.documents import DocumentRepository
from app.domain.libraries import LibraryRepository


def get_add_document_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> AddDocumentHandler:
    """DI provider for AddDocumentHandler"""
    return AddDocumentHandler(library_repo, document_repo)


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
