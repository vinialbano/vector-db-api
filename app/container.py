from app.domain.documents import DocumentRepository
from app.domain.libraries import (
    LibraryRepository,
)
from app.infrastructure import (
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
