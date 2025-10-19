from datetime import datetime, timezone

import pytest

from vector_db_api.domain.documents import (
    Chunk,
    ChunkId,
    ChunkMetadata,
    Document,
    DocumentId,
    DocumentMetadata,
    Embedding,
)
from vector_db_api.domain.libraries import (
    BruteForceIndex,
    Library,
    LibraryId,
    LibraryMetadata,
)


@pytest.fixture
def embedding():
    """Simple constant embedding used across tests."""
    return Embedding.from_list([1.0, 0.0])


@pytest.fixture
def chunk_factory(embedding):
    """Factory to build Chunk instances with optional overrides."""

    def _make(
        text: str = "hello", page: int | None = None, created_at: datetime | None = None
    ) -> Chunk:
        if created_at is not None:
            meta = ChunkMetadata(source="test", page_number=page, created_at=created_at)
        else:
            meta = ChunkMetadata(source="test", page_number=page)
        return Chunk(
            id=ChunkId.generate(), text=text, embedding=embedding, metadata=meta
        )

    return _make


@pytest.fixture
def document_factory(chunk_factory):
    """Factory to build Document instances (at least one chunk by default)."""

    def _make(chunks=None, title: str = "Doc") -> Document:
        if chunks is None:
            chunks = [chunk_factory()]
        return Document(
            id=DocumentId.generate(),
            chunks=chunks,
            metadata=DocumentMetadata(title=title),
        )

    return _make


@pytest.fixture
def library_factory(document_factory):
    def _make(documents=None, name: str = "Library") -> Library:
        if documents is None:
            documents = []
        # accept either Document objects or DocumentId values in tests; store only ids
        doc_ids = [d.id if hasattr(d, "id") else d for d in documents]
        return Library(
            id=LibraryId.generate(),
            documents=doc_ids,
            metadata=LibraryMetadata(name=name, description="Test"),
            vector_index=BruteForceIndex(),
        )

    return _make


@pytest.fixture
def now_utc():
    return datetime.now(timezone.utc)
