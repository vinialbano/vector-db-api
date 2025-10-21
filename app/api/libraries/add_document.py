from fastapi import APIRouter, Depends, status

from app.application.libraries import (
    AddDocumentCommand,
    AddDocumentHandler,
)
from app.dependencies import get_document_repository, get_library_repository
from app.domain.documents import DocumentRepository
from app.domain.libraries import LibraryRepository

add_document_router = APIRouter()


def get_add_document_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> AddDocumentHandler:
    """DI provider for AddDocumentHandler"""
    return AddDocumentHandler(library_repo, document_repo)


@add_document_router.post(
    "/{library_id}/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def add_document(
    library_id: str,
    document_id: str,
    handler: AddDocumentHandler = Depends(get_add_document_handler),
):
    command = AddDocumentCommand(library_id=library_id, document_id=document_id)
    handler.handle(command)
    return None
