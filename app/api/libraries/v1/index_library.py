from fastapi import Depends, status
from pydantic import BaseModel, ConfigDict

from app.api.libraries.router import libraries_router as router
from app.application.libraries import (
    IndexLibraryCommand,
    IndexLibraryHandler,
)
from app.container import get_document_repository, get_library_repository
from app.domain.documents.document_repository import DocumentRepository
from app.domain.libraries import LibraryIndexerService, LibraryRepository


def get_library_indexer_service(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> LibraryIndexerService:
    """DI provider for LibraryIndexerService"""
    return LibraryIndexerService(document_repo)


def get_index_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    indexer_service: LibraryIndexerService = Depends(get_library_indexer_service),
) -> IndexLibraryHandler:
    """DI provider for IndexLibraryHandler"""
    return IndexLibraryHandler(library_repo, indexer_service)


class IndexLibraryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@router.patch(
    "/{library_id}/index",
    status_code=status.HTTP_204_NO_CONTENT,
)
def index_library(
    library_id: str,
    handler: IndexLibraryHandler = Depends(get_index_library_handler),
):
    command = IndexLibraryCommand(library_id=library_id)
    handler.handle(command)
