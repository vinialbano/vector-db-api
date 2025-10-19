from fastapi import Depends

from vector_db_api.application.commands.documents import (
    AddChunkHandler,
    CreateDocumentHandler,
    UpdateDocumentHandler,
)
from vector_db_api.application.commands.documents.delete_chunk import DeleteChunkHandler
from vector_db_api.application.commands.documents.delete_document import (
    DeleteDocumentHandler,
)
from vector_db_api.application.commands.documents.update_chunk import UpdateChunkHandler
from vector_db_api.application.commands.libraries import (
    AddDocumentHandler,
    CreateLibraryHandler,
    DeleteLibraryHandler,
    IndexLibraryHandler,
    RemoveDocumentHandler,
    UpdateLibraryHandler,
)
from vector_db_api.application.queries.documents import (
    GetChunkHandler,
    GetDocumentHandler,
)
from vector_db_api.application.queries.libraries import GetLibraryHandler
from vector_db_api.domain.documents import DocumentRepository
from vector_db_api.domain.libraries import (
    KDTreeIndex,
    LibraryIndexerService,
    LibraryRepository,
)
from vector_db_api.infrastructure.repositories import (
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)

# --------------
# Infrastructure
# --------------

# Singleton instances for in-memory repositories
_document_repository_instance = InMemoryDocumentRepository()
_library_repository_instance = InMemoryLibraryRepository()


def get_document_repository() -> DocumentRepository:
    """DI provider for DocumentRepository"""
    return _document_repository_instance


def get_library_repository() -> LibraryRepository:
    """DI provider for LibraryRepository"""
    return _library_repository_instance


# ---------------
# Domain Services
# ---------------


def get_library_indexer_service(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> LibraryIndexerService:
    """DI provider for LibraryIndexerService"""
    return LibraryIndexerService(document_repo)


# ----------------
# Command Handlers
# ----------------

# ---------
# Documents
# ---------


def get_add_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> AddChunkHandler:
    """DI provider for AddChunkHandler"""
    return AddChunkHandler(document_repo)


def get_create_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> CreateDocumentHandler:
    """DI provider for CreateDocumentHandler"""
    return CreateDocumentHandler(document_repo)


def get_delete_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteChunkHandler:
    """DI provider for DeleteChunkHandler"""
    return DeleteChunkHandler(document_repo)


def get_delete_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> DeleteDocumentHandler:
    """DI provider for DeleteDocumentHandler"""
    return DeleteDocumentHandler(document_repo)


def get_update_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> UpdateChunkHandler:
    """DI provider for UpdateChunkHandler"""
    return UpdateChunkHandler(document_repo)


def get_update_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> UpdateDocumentHandler:
    """DI provider for UpdateDocumentHandler"""
    return UpdateDocumentHandler(document_repo)


# ---------
# Libraries
# ---------


def get_create_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> CreateLibraryHandler:
    """DI provider for CreateLibraryHandler"""
    return CreateLibraryHandler(library_repo, lambda: KDTreeIndex())


def get_delete_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> DeleteLibraryHandler:
    """DI provider for DeleteLibraryHandler"""
    return DeleteLibraryHandler(library_repo)


def get_index_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    indexer_service: LibraryIndexerService = Depends(get_library_indexer_service),
) -> IndexLibraryHandler:
    """DI provider for IndexLibraryHandler"""
    return IndexLibraryHandler(library_repo, indexer_service)


def get_update_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> UpdateLibraryHandler:
    """DI provider for UpdateLibraryHandler"""
    return UpdateLibraryHandler(library_repo)


def get_add_document_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> AddDocumentHandler:
    """DI provider for AddDocumentHandler"""
    return AddDocumentHandler(library_repo, document_repo)


def get_remove_document_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> RemoveDocumentHandler:
    """DI provider for RemoveDocumentHandler"""
    return RemoveDocumentHandler(library_repo, document_repo)


# --------------
# Query Handlers
# --------------


def get_get_document_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetDocumentHandler:
    return GetDocumentHandler(document_repo)


def get_get_chunk_handler(
    document_repo: DocumentRepository = Depends(get_document_repository),
) -> GetChunkHandler:
    return GetChunkHandler(document_repo)


def get_get_library_handler(
    library_repo: LibraryRepository = Depends(get_library_repository),
) -> GetLibraryHandler:
    return GetLibraryHandler(library_repo)
