from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, List, Tuple

from app.domain.common.decorators import refresh_timestamp_after
from app.domain.common.embedding import Embedding
from app.domain.documents import DocumentId
from app.domain.libraries.indexed_chunk import IndexedChunk
from app.domain.libraries.library_id import LibraryId
from app.domain.libraries.library_metadata import LibraryMetadata
from app.domain.libraries.vector_index import VectorIndex
from app.errors import InvalidEntityError


def invalidate_index_after(fn: Callable) -> Callable:
    def wrapper(self: Library, *args, **kwargs) -> Any:
        result = fn(self, *args, **kwargs)
        # keep behavior: mark index invalid & refresh metadata
        self.invalidate_index()
        return result

    return wrapper


@dataclass
class Library:
    """Library Aggregate Root - stores references to documents (DocumentId).

    Documents themselves are separate aggregates; this Library keeps only
    DocumentId references and manages index state.
    """

    id: LibraryId
    documents: List[DocumentId]
    metadata: LibraryMetadata
    vector_index: VectorIndex
    _is_indexed: bool = field(default=False, init=False, repr=False)

    def __post_init__(self):
        if not self.metadata:
            raise InvalidEntityError("Library metadata cannot be empty")

    @invalidate_index_after
    def add_document(self, document_id: DocumentId) -> None:
        if any(d == document_id for d in self.documents):
            raise InvalidEntityError(
                f"Document {document_id} already exists in library {self.id}"
            )
        self.documents.append(document_id)

    @invalidate_index_after
    def remove_document(self, document_id: DocumentId) -> None:
        self.documents = [d for d in self.documents if d != document_id]

    @refresh_timestamp_after
    def index(self, chunks: List[IndexedChunk]) -> None:
        """Build the vector index from the provided indexed chunks"""
        if not chunks:
            raise InvalidEntityError("No chunks provided for indexing")
        if self.is_indexed:
            self.vector_index.clear()

        self.vector_index.build(chunks)
        self._is_indexed = True

    @refresh_timestamp_after
    def invalidate_index(self) -> None:
        self._is_indexed = False
        self.vector_index.clear()

    @refresh_timestamp_after
    def update_metadata(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        custom_fields: dict | None = None,
    ) -> None:
        """Update library metadata using the value-object updated() factory."""
        self.metadata = self.metadata.updated(
            name=name, description=description, custom_fields=custom_fields
        )

    def _refresh_timestamp(self) -> None:
        """Refresh this library's metadata updated_at timestamp."""
        self.metadata = self.metadata.updated()

    def contains_document(self, document_id: DocumentId) -> bool:
        return any(d == document_id for d in self.documents)

    def find_similar_chunks(
        self,
        query_embedding: Embedding,
        k: int,
        min_similarity: float = 0.0,
    ) -> List[Tuple[IndexedChunk, float]]:
        """Find the k most similar chunks to the given query embedding"""
        if k <= 0:
            raise InvalidEntityError("k must be a positive integer")
        results = self.vector_index.search(query_embedding, k)

        # Compute similarity and filter
        scored: List[Tuple[IndexedChunk, float]] = []
        for chunk in results:
            score = chunk.similarity(query_embedding)
            if score >= min_similarity:
                scored.append((chunk, score))

        return scored

    def get_indexed_chunks(self) -> List[IndexedChunk]:
        """Return all indexed chunks currently indexed for this library."""
        return list(self.vector_index.get_chunks() or [])

    @property
    def is_indexed(self) -> bool:
        return self._is_indexed

    @property
    def document_count(self) -> int:
        return len(self.documents)

    @property
    def total_documents(self) -> int:
        return len(self.documents)
