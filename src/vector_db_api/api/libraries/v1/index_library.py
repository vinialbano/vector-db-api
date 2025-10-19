from fastapi import Depends
from pydantic import BaseModel

from vector_db_api.api.libraries.router import libraries_router as router
from vector_db_api.application.libraries import (
    IndexLibraryCommand,
    IndexLibraryHandler,
)
from vector_db_api.container import get_document_repository, get_library_repository
from vector_db_api.domain.documents.document_repository import DocumentRepository
from vector_db_api.domain.libraries import LibraryIndexerService, LibraryRepository


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
    library_id: str

    class Config:
        from_attributes = True


@router.post("/{library_id}/index", response_model=IndexLibraryResponse)
def index_library(
    library_id: str,
    handler: IndexLibraryHandler = Depends(get_index_library_handler),
):
    command = IndexLibraryCommand(library_id=library_id)
    response = handler.handle(command)
    return IndexLibraryResponse(library_id=response.library_id)
