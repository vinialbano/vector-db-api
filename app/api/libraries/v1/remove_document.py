from fastapi import Depends
from pydantic import BaseModel, ConfigDict

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    RemoveDocumentCommand,
    RemoveDocumentHandler,
)
from app.container import get_document_repository, get_library_repository
from app.domain.documents.document_repository import DocumentRepository
from app.domain.libraries.library_repository import LibraryRepository
from fastapi import HTTPException, status


def get_remove_document_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> RemoveDocumentHandler:
    """DI provider for RemoveDocumentHandler"""
    return RemoveDocumentHandler(library_repo, document_repo)


class RemoveDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@router.delete(
    "/{library_id}/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_document(
    library_id: str,
    document_id: str,
    handler: RemoveDocumentHandler = Depends(get_remove_document_handler),
):
    command = RemoveDocumentCommand(library_id=library_id, document_id=document_id)
    response = handler.handle(command)
    if not response.removed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="document not present in library",
        )
    return None
