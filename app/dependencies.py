from typing import Callable

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.domain.documents import DocumentRepository
from app.domain.libraries import (
    BruteForceIndex,
    KDTreeIndex,
    LibraryRepository,
    VectorIndex,
)
from app.infrastructure import (
    InMemoryDocumentRepository,
    InMemoryLibraryRepository,
)


class Settings(BaseSettings):
    vector_index_type: str = "kd"  # 'kd' (KDTreeIndex) or 'brute' (BruteForceIndex)

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

# --- Singleton repository instances ---
# Create module-level singleton instances so DI providers return the same
# repository objects across the application lifetime.
_document_repository_instance = InMemoryDocumentRepository()
_library_repository_instance = InMemoryLibraryRepository()


def _default_vector_index_factory() -> Callable[[], VectorIndex]:
    """Return a factory that constructs the chosen VectorIndex implementation."""
    print(f"Using vector index type: {settings.vector_index_type}")
    if settings.vector_index_type == "brute":
        return lambda: BruteForceIndex()
    # default to KDTree
    return lambda: KDTreeIndex()


# ---------
# Providers
# ---------


def get_document_repository() -> DocumentRepository:
    """DI provider for DocumentRepository"""
    return _document_repository_instance  # Singleton


def get_library_repository() -> LibraryRepository:
    """DI provider for LibraryRepository"""
    return _library_repository_instance  # Singleton


def get_vector_index_factory() -> Callable[[], VectorIndex]:
    """DI provider for a VectorIndex factory.

    Returns a callable that when called produces a new VectorIndex instance.
    """
    return _default_vector_index_factory()
